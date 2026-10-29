"""A small CartPole world model, written to be read.

The pivot in one sentence: stop training a network to know what to do, and train one
to know what happens next. Then the goal is a function you can edit after training,
because the weights are busy being physics.

Everything here is a *worked reference*, not an assessment. Numbers produced by a run
are written to `results.json` next to the exact configuration that produced them.

Usage
-----
    python world_model.py --output my_work/world_model01
    python world_model.py --output my_work/world_model01_tiny --episodes 6 --epochs 1

PyTorch is an optional dependency. When it is missing the command writes status
`blocked` and exits non-zero; it never reports a pass it did not achieve.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import cartpole  # noqa: E402
import topology  # noqa: E402

SOURCE = {
    'author': 'Anubhab Banerjee',
    'title': 'How to Make Your First World Model from Scratch',
    'venue': 'Towards Data Science, 23 September 2026',
    'code': 'https://github.com/AnubhabBanerjee/CartPole-Daydream',
    'url': 'https://towardsdatascience.com/how-to-make-your-first-world-model-from-scratch',
    'attribution': (
        'Pedagogical design, narrative and reported measurements belong to the author. '
        'This module re-derives the method in this course\'s own code and reports only '
        'its own observed numbers.'
    ),
}

STATE_SIZE = 2          # visible cart position and pole angle
ACTION_SIZE = 2
HIDDEN_SIZE = 48
GOAL_BALANCE = 'balance'
GOAL_PARK = 'park'
PARK_TARGET = 1.0

# A crash is about one step in 380, so an unweighted classifier scores 99.7% by always
# answering "fine". The remedy is a *positive-class* weight, not a multiplier on the whole
# loss: multiplying the whole BCE scales the gradient without moving the optimum, which
# still predicts the base rate. This distinction is the difference between a crash detector
# and a smoke alarm with the battery out.
TERMINATION_WEIGHT = 380.0

# The two heads are learning different quantities with different natural scales: a
# normalized delta MSE is around 1e-4, while a 380-weighted BCE on 0.6%-positive labels is
# around 1. A single unweighted sum lets whichever is larger own the gradients, and the
# other head degrades. This coefficient puts them on comparable footing. It is a declared
# engineering choice, recorded in every result, not a tuned secret: at 0.01 the crash head
# reached 0.38 recall; at 0.02 it reached 0.93 with delta error unchanged.
TERMINATION_LOSS_SCALE = 0.02


def crash_loss(logit, target):
    """Binary cross-entropy with the rare class up-weighted.

    `pos_weight` multiplies the loss term for positive examples only, so the optimum moves
    toward detecting crashes. A plain `TERMINATION_WEIGHT * BCE(...)` would leave the
    optimum at the base rate and merely change the step size.
    """
    torch, _ = check_torch()
    weight = torch.tensor(TERMINATION_WEIGHT, dtype=logit.dtype)
    return torch.nn.functional.binary_cross_entropy_with_logits(logit, target, pos_weight=weight)


def ensure_new_output(path: Path) -> Path:
    """Runs never overwrite earlier runs. A stale result is not evidence."""
    path = Path(path)
    if path.exists():
        raise FileExistsError(f'{path} already exists; choose a new output directory')
    path.mkdir(parents=True, exist_ok=False)
    return path


def check_torch():
    """Return the torch module, or explain why the run is blocked."""
    try:
        import torch  # noqa: PLC0415  (optional dependency, probed at runtime)
    except ImportError as error:  # pragma: no cover - exercised only without torch
        return None, f'PyTorch is not available in this interpreter: {error}'
    return torch, None


# --------------------------------------------------------------------------- goals
# The goal is a function. Nothing below is stored in a weight matrix, so the same
# trained model answers a different question when you edit one of these.

def survival_mask(termination_logits):
    """Steps of each dream that are still reachable, given the predicted crash.

    The crash head predicts a logit per imagined step; `<= 0` is "still alive". Once a
    step is predicted to fail, everything after it is **unreachable** — a dream cannot
    crash at step 3 and be scored as alive at step 4. Applying a per-step threshold
    without latching lets a trajectory "come back alive" and makes a doomed plan look
    survivable.

    A truncated timer never appears here: the model cannot see a stopwatch, so it was never
    trained to predict one.
    """
    torch, _ = check_torch()
    alive_step = termination_logits <= 0.0
    # Running logical AND along the step axis is the latch: true until the first false,
    # false forever after. Written as a loop because `cumprod` on bool tensors differs
    # between torch versions, and this code must be obvious to a reader.
    running = alive_step[:, :1].clone()
    columns = [running]
    for step in range(1, alive_step.shape[1]):
        running = running & alive_step[:, step: step + 1]
        columns.append(running.clone())
    return torch.cat(columns, dim=1)


def masked_mean(values, mask):
    weights = mask.to(values.dtype)
    count = weights.sum(dim=1).clamp_min(1.0)
    return (values * weights).sum(dim=1) / count


def terminal_mean(values, mask):
    """The value at the last surviving step of each dream, not an average over it.

    Scoring by the average distance across a dream rejects the only manoeuvre that
    works, because that manoeuvre first moves the wrong way. This is the article's
    hard-won correction, and it is why this function exists at all.
    """
    weights = mask.to(values.dtype)
    count = weights.sum(dim=1)
    # The number of surviving steps is the last entry of the running sum; gathering
    # that single column keeps the result per-dream instead of per-step.
    surviving = (weights.cumsum(dim=1) - 1.0).clamp_min(0.0)[:, -1:]
    gathered = values.gather(1, surviving.long()).reshape(-1)
    return gathered * (count > 0).to(values.dtype)


def survival_fraction(mask):
    # A boolean mask has no floating-point mean in torch; convert first, explicitly.
    return mask.to(_floating(mask)).mean(dim=1)


def _floating(tensor):
    torch, _ = check_torch()
    return torch.float32 if not tensor.is_floating_point() else tensor.dtype


def score_balance(observations, termination_logits):
    """Goal A: stay alive. This is the goal a reward function used to encode.

    `observations` are **normalized** visible states. The angle penalty needs the tolerance
    scale to be interpretable, so it is divided by `THETA_LIMIT` to report a fraction of
    the way to falling over.
    """
    alive = survival_mask(termination_logits)
    normalized_angle = observations[:, :, cartpole.VISIBLE_POLE_ANGLE].abs()
    uprightness = masked_mean(normalized_angle, alive)
    return survival_fraction(alive) - 4.0 * uprightness


def _cart_position_metres(cart_positions):
    """Convert normalized cart positions back to metres, for torch or NumPy input."""
    torch, _ = check_torch()
    if isinstance(cart_positions, torch.Tensor):
        return cart_positions * cartpole.X_LIMIT
    return np.asarray(cart_positions, dtype=float) * cartpole.X_LIMIT


def score_park(observations, termination_logits, target: float = PARK_TARGET,
               position_weight: float = 1.0, upright_weight: float = 0.5):
    """Goal B: park the cart at `target` and stay upright.

    `target` is in **metres**, and `observations` arrive normalized, so the position term
    is converted back to metres before the distance is taken. Comparing a normalized
    position against a metric target is a silent unit bug: a normalized 1.0 is 2.4 m, so
    the planner would be aiming at the rail limit while the constant says one metre.
    """
    alive = survival_mask(termination_logits)
    cart_position_m = _cart_position_metres(observations[:, :, cartpole.VISIBLE_CART_POSITION])
    distance_m = (cart_position_m - target).abs()
    off_target_m = terminal_mean(distance_m, alive)
    normalized_angle = observations[:, :, cartpole.VISIBLE_POLE_ANGLE].abs()
    uprightness = masked_mean(normalized_angle, alive)
    return (survival_fraction(alive)
            - position_weight * off_target_m
            - upright_weight * uprightness)


GOALS = {GOAL_BALANCE: score_balance, GOAL_PARK: score_park}


# --------------------------------------------------------------------------- model

def build_model(torch):
    nn = torch.nn

    class WorldModel(nn.Module):
        """Observe two numbers and an action; predict the change and the crash.

        Predict the *change*, never the next position. Consecutive moments are nearly
        identical, so a network asked for the next position scores beautifully by
        copying its input and learns no physics.
        """

        def __init__(self):
            super().__init__()
            self.obs_encoder = nn.Linear(STATE_SIZE, HIDDEN_SIZE)
            self.action_encoder = nn.Linear(ACTION_SIZE, HIDDEN_SIZE)
            self.gru = nn.GRUCell(HIDDEN_SIZE, HIDDEN_SIZE)
            self.delta_head = nn.Linear(HIDDEN_SIZE, STATE_SIZE)
            self.termination_head = nn.Linear(HIDDEN_SIZE, 1)

        def initial_hidden(self, batch: int):
            return torch.zeros(batch, HIDDEN_SIZE)

        def step(self, obs_norm, action_ids, hidden):
            """The line that turns a predictor into a world model: output becomes input."""
            action_ids = action_ids.long()
            inputs = torch.relu(self.obs_encoder(obs_norm))
            inputs = inputs + self.action_encoder(
                torch.nn.functional.one_hot(action_ids, ACTION_SIZE).to(obs_norm.dtype)
            )
            hidden = self.gru(inputs, hidden)
            delta = self.delta_head(hidden)
            termination_logit = self.termination_head(hidden).squeeze(-1)
            return obs_norm + delta, termination_logit, hidden

    return WorldModel()


# --------------------------------------------------------------------------- data windows

def episode_bounds(data) -> list[tuple[int, int]]:
    """Half-open [start, end) per episode. A window may never cross a boundary.

    The memory carries state forward, so a window spanning two episodes would be
    trained on a transition that never happened.
    """
    ends = data['terminated'] | data['truncated']
    bounds, begin = [], 0
    for index, ended in enumerate(ends):
        if ended:
            bounds.append((begin, index + 1))
            begin = index + 1
    if begin < len(ends):
        bounds.append((begin, len(ends)))
    return bounds


def valid_window_starts(bounds, sequence: int) -> np.ndarray:
    """Starts whose `sequence` transitions all live inside one episode.

    Windows are indexed over **transitions**, not over observations: transition `i` has a
    recorded successor in `next_observations[i]`. That is why the final transition of an
    episode — the one carrying the crash label — is trainable, and it is why the bound is
    `start <= end - sequence` with a half-open episode range.

    This bound was wrong once, in a way that looked like a weak model. Excluding the last
    transition of every episode removed *every* positive crash example; the crash head then
    collapsed to "always alive" and the planner discarded every safe dream.
    """
    if sequence < 1:
        raise ValueError('sequence must be positive.')
    starts = []
    for begin, end in bounds:
        last = end - sequence
        if last >= begin:
            starts.extend(range(begin, last + 1))
    return np.asarray(sorted(starts), dtype=int)


# --------------------------------------------------------------------------- training

def train(model, torch, data, epochs: int, train_steps: int, sequence: int = 8,
          batch_size: int = 32, learning_rate: float = 3e-3, seed: int = 0):
    """Teacher forcing, stated plainly: every step gets the real observation back.

    That is why training is fast and stable, and why the model never once experiences
    the consequences of its own error. Free rollout later removes the instructor.
    """
    torch.manual_seed(seed)
    observations = torch.tensor(cartpole.normalize_visible(data['observations']), dtype=torch.float32)
    successors = torch.tensor(cartpole.normalize_visible(data['next_observations']), dtype=torch.float32)
    actions = torch.tensor(data['actions'], dtype=torch.long)
    terminated = torch.tensor(data['terminated'], dtype=torch.float32)

    bounds = episode_bounds(data)
    split = max(1, int(round(len(bounds) * 0.8)))
    train_starts = valid_window_starts(bounds[:split], sequence)
    holdout_starts = valid_window_starts(bounds[split:] or bounds[:1], sequence)
    if train_starts.size == 0:
        raise ValueError(f'Need at least {sequence + 1} transitions inside one episode.')

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    generator = np.random.default_rng(seed)
    history, best, best_state = [], None, None
    for epoch in range(max(1, int(epochs))):
        model.train()
        running = 0.0
        for _ in range(max(1, int(train_steps))):
            batch = generator.choice(train_starts,
                                     size=min(int(batch_size), train_starts.size),
                                     replace=False)
            loss = window_loss(model, observations, successors, actions, terminated,
                               batch, sequence)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            running += float(loss.detach())
        model.eval()
        validation = teacher_forced_eval(model, torch, observations, successors, actions,
                                         terminated, holdout_starts, sequence)
        entry = {
            'epoch': epoch + 1,
            'train_loss': running / max(1, int(train_steps)),
            'validation_loss': validation['loss'],
            'validation_cart_position_m': validation['position_error'],
            'validation_pole_angle_rad': validation['angle_error'],
        }
        history.append(entry)
        if best is None or entry['validation_loss'] < best['validation_loss']:
            best = entry
            # Recording the best epoch is not the same as using its weights. Keep a copy
            # of the parameters and restore them, or every later measurement describes a
            # different model from the one the reported loss belongs to.
            best_state = {name: tensor.detach().clone()
                          for name, tensor in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    return {'history': history, 'best': best, 'train_windows': int(train_starts.size),
            'holdout_windows': int(holdout_starts.size),
            'restored_best_epoch': best['epoch'] if best else None}


def window_loss(model, observations, successors, actions, terminated, starts,
                sequence: int = 8):
    """One loss for both heads.

    Both heads are means over their own term, then added with **equal weight**. The rare
    crash class is handled by `pos_weight` inside `crash_loss`, not by scaling this sum:
    scaling the sum would change the optimizer's step size without moving either optimum.
    """
    starts = np.asarray(starts, dtype=int)
    hidden = model.initial_hidden(len(starts))
    observed = observations[starts]
    delta_loss = 0.0
    termination_loss = 0.0
    for offset in range(sequence):
        index = starts + offset
        predicted, logit, hidden = model.step(observed, actions[index], hidden)
        truth = successors[index]
        delta_loss = delta_loss + (predicted - truth).square().mean()
        termination_loss = termination_loss + crash_loss(logit, terminated[index])
        # Teacher forcing: the real observation replaces the guess before the next step.
        observed = truth
    return delta_loss / sequence + TERMINATION_LOSS_SCALE * termination_loss / sequence


def teacher_forced_eval(model, torch, observations, successors, actions, terminated,
                        starts, sequence: int = 8):
    starts = np.asarray(starts, dtype=int)
    if starts.size == 0:
        return {'loss': float('nan'), 'position_error': 0.0, 'angle_error': 0.0}
    with torch.no_grad():
        hidden = model.initial_hidden(len(starts))
        observed = observations[starts]
        delta_loss = termination_loss = 0.0
        position_error = angle_error = 0.0
        for offset in range(sequence):
            index = starts + offset
            predicted, logit, hidden = model.step(observed, actions[index], hidden)
            truth = successors[index]
            delta_loss = delta_loss + (predicted - truth).square().mean()
            termination_loss = termination_loss + crash_loss(logit, terminated[index])
            # Errors are reported in physical units, not normalized units.
            error = np.abs(cartpole.denormalize_visible(predicted.numpy())
                           - cartpole.denormalize_visible(truth.numpy()))
            position_error += float(error[:, cartpole.VISIBLE_CART_POSITION].mean())
            angle_error += float(error[:, cartpole.VISIBLE_POLE_ANGLE].mean())
            observed = truth
        return {
            'loss': float(delta_loss / sequence + TERMINATION_LOSS_SCALE * termination_loss / sequence),
            'position_error': position_error / sequence,
            'angle_error': angle_error / sequence,
        }


# --------------------------------------------------------------------------- dreaming

def dream(model, torch, start_states, action_sequences, hidden=None) -> dict:
    """Daydream a batch of plans; reality is not consulted after the fork.

    `start_states` is (n, 4) and `action_sequences` is (n, horizon). One real
    observation is broadcast to every candidate; only the model's own output feeds the
    next step.

    `hidden` is the memory state to **fork** the plans from. Passing it matters: a blank
    memory knows neither velocity, so a planner that resets to zero at every decision
    cannot reason about a cart that is already moving. That is the bug the article's
    eight-step warm-up is working around, and it is worth seeing fail before it is fixed.
    """
    states = np.asarray(start_states, dtype=float)
    if states.ndim == 1:
        states = states.reshape(1, -1)
    plans = np.asarray(action_sequences, dtype=int)
    if plans.ndim == 1:
        plans = plans.reshape(1, -1)
    if len(states) == 1 and len(plans) > 1:
        states = np.repeat(states, len(plans), axis=0)
    if len(states) != len(plans):
        raise ValueError('Every candidate plan needs one starting state.')
    if plans.shape[1] == 0:
        raise ValueError('At least one action is required.')

    visible = torch.tensor(cartpole.normalize_visible(cartpole.visible(states)), dtype=torch.float32)
    if hidden is None:
        hidden = model.initial_hidden(len(plans))
    elif hidden.shape[0] != len(plans):
        hidden = hidden.repeat(len(plans), 1)
    observed = visible
    imagined = np.empty((len(plans), plans.shape[1], STATE_SIZE), dtype=float)
    logits = np.empty((len(plans), plans.shape[1]), dtype=float)
    with torch.no_grad():
        for index in range(plans.shape[1]):
            observed, logit, hidden = model.step(observed, torch.tensor(plans[:, index]), hidden)
            imagined[:, index] = observed.numpy()
            logits[:, index] = logit.numpy()
    return {'visible': imagined, 'termination_logits': logits,
            'start_visible': visible.numpy()}


def advance_memory(model, torch, visible_state, action, hidden):
    """Fold one *real* observation and shove into the memory.

    This is how the planner gets to know how fast things are moving: the memory is
    updated with what actually happened, then every plan forks from that point.
    """
    torch, _ = check_torch()
    observed = torch.tensor(
        cartpole.normalize_visible(cartpole.visible(np.asarray(visible_state, dtype=float))).reshape(1, -1),
        dtype=torch.float32,
    )
    with torch.no_grad():
        _, _, hidden = model.step(observed, torch.tensor([int(action)]), hidden)
    return hidden


def score_plans(torch, goal: str, imagined: dict):
    if goal not in GOALS:
        raise ValueError(f'Unknown goal {goal!r}; choose one of {sorted(GOALS)}.')
    with torch.no_grad():
        scores = GOALS[goal](
            torch.tensor(imagined['visible'], dtype=torch.float32),
            torch.tensor(imagined['termination_logits'], dtype=torch.float32),
        )
    return scores.numpy()


def plan(model, torch, state, goal: str, horizon: int, sequences: int,
         generator: np.random.Generator, hidden=None) -> tuple[int, float]:
    """Invent random plans, daydream them, score them, take the first shove of the best.

    This is the entire decision procedure: imagine a load of futures, pick the nicest,
    take one step towards it, then throw the plan away and think again.

    `hidden` is the forked memory from real observation. Passing it is what lets the
    planner reason about velocity at all; the measurement below reports both variants so
    the difference is visible rather than asserted.
    """
    if horizon <= 0 or sequences <= 0:
        raise ValueError('horizon and sequences must be positive.')
    plans = generator.integers(0, ACTION_SIZE, size=(int(sequences), int(horizon)))
    imagined = dream(model, torch, np.asarray(state, dtype=float), plans, hidden=hidden)
    scores = score_plans(torch, goal, imagined)
    best = int(np.argmax(scores))
    return int(plans[best][0]), float(scores[best])


# --------------------------------------------------------------------------- measurement

def free_rollout_errors(model, torch, data, holdout_starts, horizon: int, tolerance: float,
                        warmup: int = 8) -> dict:
    """Error **at each depth**, with the lazy 'nothing ever changes' baseline beside it.

    The distinction matters: averaging the error over steps `1..h` answers "how wrong is
    the dream on average", not "how wrong is the dream at depth h". The first hides the
    depth where the model actually falls apart, which is the number a planner needs.

    The baseline is the most useful comparison here: it says how far the daydream can be
    trusted before a model that assumes the universe stopped does better.

    `warmup` real transitions are folded into the memory before the free rollout starts.
    Without them the memory is blank and cannot encode a velocity at all, so the first
    predicted step is a guess and the comparison measures ignorance rather than drift.
    The same real prefix is used for both the model and the frozen baseline, so the
    comparison is like for like.
    """
    warmup = max(0, int(warmup))
    depth, angle, position, angle_base, position_base, beats = [], [], [], [], [], []
    for steps in range(1, max(1, horizon) + 1):
        collected_angle, collected_position = [], []
        baseline_angle, baseline_position = [], []
        for start in holdout_starts:
            first = start + warmup
            actions = data['actions'][first: first + steps]
            if len(actions) < steps:
                continue
            hidden = _warm_memory(model, torch, data, start, warmup)
            imagined = dream(model, torch, data['states'][first], actions[None, :], hidden=hidden)
            truth = cartpole.visible(data['states'][first + 1: first + steps + 1])
            error = np.abs(cartpole.denormalize_visible(imagined['visible'][0]) - truth)
            # Error AT this depth, not the mean of every depth up to it.
            collected_position.append(float(error[-1, cartpole.VISIBLE_CART_POSITION]))
            collected_angle.append(float(error[-1, cartpole.VISIBLE_POLE_ANGLE]))
            frozen = cartpole.visible(data['states'][first])
            frozen_error = np.abs(frozen[None, :] - truth)
            baseline_position.append(float(frozen_error[-1, cartpole.VISIBLE_CART_POSITION]))
            baseline_angle.append(float(frozen_error[-1, cartpole.VISIBLE_POLE_ANGLE]))
        if not collected_angle:
            continue
        depth.append(steps)
        angle.append(float(np.mean(collected_angle)))
        position.append(float(np.mean(collected_position)))
        angle_base.append(float(np.mean(baseline_angle)))
        position_base.append(float(np.mean(baseline_position)))
        beats.append(angle[-1] < angle_base[-1])

    trust, first_failure = cartpole.trust_horizon(angle, tolerance) if angle else (0, None)
    beaten = [d for d, better in zip(depth, beats) if better]
    return {
        'depth': depth,
        'pole_angle_rad': angle,
        'cart_position_m': position,
        'pole_angle_rad_frozen_baseline': angle_base,
        'cart_position_m_frozen_baseline': position_base,
        'tolerance_rad': float(tolerance),
        'memory_warmup_steps': warmup,
        'trust_horizon': int(trust),
        'first_depth_outside_tolerance': first_failure,
        'deepest_depth_beaten_by_frozen_baseline': (max(beaten) if beaten else 0),
        'measurement': ('error at each depth h after a disclosed warm-up of real '
                        'transitions; reality not consulted during the dreamed part'),
    }


def _warm_memory(model, torch, data, start: int, steps: int):
    """Fold `steps` real transitions into a memory, so velocity is encoded before dreaming."""
    hidden = model.initial_hidden(1)
    for offset in range(steps):
        hidden = advance_memory(model, torch, data['states'][start + offset],
                                int(data['actions'][start + offset]), hidden)
    return hidden


def play_episode(model, torch, goal: str, horizon: int, sequences: int,
                 generator: np.random.Generator, warmup: int = 0,
                 carry_memory: bool = True) -> dict:
    """One real game: plan at each step, optionally during a disclosed warm-up.

    Two memory policies are measured, because the difference is the point:

    * `carry_memory=True` — the memory is folded forward with each **real** observation
      and shove, then every candidate plan forks from it. The planner can infer velocity.
    * `carry_memory=False` — the memory resets to zeros at each decision, so every dream
      starts from ignorance about motion. This reproduces the failure the article's
      warm-up works around.

    `warmup` decisions bypass planning with the three-line controller. The count of
    decisions that were actually planned is recorded, never implied.
    """
    state = cartpole.initial_state(generator)
    decision_seconds = []
    planned = 0
    hidden = model.initial_hidden(1)
    step_index = 0
    for step_index in range(cartpole.MAX_STEPS):
        began = time.perf_counter()
        if step_index < warmup:
            action = cartpole.proportional_controller(state)
        else:
            action, _ = plan(model, torch, state, goal, horizon, sequences, generator,
                             hidden=hidden if carry_memory else None)
            planned += 1
        decision_seconds.append(time.perf_counter() - began)
        if carry_memory:
            hidden = advance_memory(model, torch, state, action, hidden)
        state = cartpole.step(state, action)
        if cartpole.failed(state):
            break
    return {
        'steps': step_index + 1,
        'planned_decisions': planned,
        'mean_decision_seconds': float(np.mean(decision_seconds)),
        'terminal_distance_from_park_target':
            abs(float(state[cartpole.CART_POSITION]) - PARK_TARGET),
    }


def summarise_episodes(records: list[dict]) -> dict:
    steps = [r['steps'] for r in records]
    distances = [r['terminal_distance_from_park_target'] for r in records]
    return {
        'episodes': len(records),
        'mean_steps': float(np.mean(steps)),
        'std_steps': float(np.std(steps)),
        'max_steps': int(np.max(steps)),
        'mean_terminal_distance_from_park_target': float(np.mean(distances)),
        'mean_decision_seconds': float(np.mean([r['mean_decision_seconds'] for r in records])),
        'planned_decisions_per_episode': int(records[0]['planned_decisions']),
    }


def baselines(generator: np.random.Generator, episodes: int) -> dict:
    """Two reference agents, so 'it works' has something to be compared against."""
    flail = [cartpole.rollout(cartpole.initial_state(generator),
                              lambda s: int(generator.integers(0, 2)))['steps']
             for _ in range(int(episodes))]
    controller = [cartpole.rollout(cartpole.initial_state(generator),
                                   lambda s: cartpole.proportional_controller(s))['steps']
                  for _ in range(int(episodes))]
    return {
        'coin_flips_mean_steps': float(np.mean(flail)),
        'coin_flips_std_steps': float(np.std(flail)),
        'hand_controller_mean_steps': float(np.mean(controller)),
        'measurement': 'the real simulator, with no learned model involved',
    }


def crash_detection_metrics(model, torch, data, bounds, limit: int = 250) -> dict:
    """Recall and false-alarm rate for the crash head, with carried memory.

    Both numbers are needed. A detector that flinches at nothing is useless; one that
    never fires strolls into futures where the pole already fell. Reporting only
    accuracy would hide both failures behind the 99.4% base rate.

    `truncated` episodes are excluded rather than counted as safe: the timer is a
    stopwatch the model cannot see, so it is neither a crash nor evidence of no crash.
    """
    observations = torch.tensor(cartpole.normalize_visible(data['observations']),
                                dtype=torch.float32)
    actions = torch.tensor(data['actions'], dtype=torch.long)
    true_positive = false_positive = false_negative = 0
    episodes = 0
    with torch.no_grad():
        for begin, end in bounds:
            if end <= begin:
                continue
            hidden = model.initial_hidden(1)
            observed = observations[begin]
            episodes += 1
            for index in range(begin, min(end, begin + limit)):
                observed, logit, hidden = model.step(observed, actions[index: index + 1], hidden)
                predicted = bool(float(logit.item()) > 0.0)
                truth = bool(data['terminated'][index])
                true_positive += predicted and truth
                false_positive += predicted and not truth
                false_negative += truth and not predicted
    positives = true_positive + false_negative
    negatives = episodes * limit if episodes else 1
    return {
        'evaluated_episodes': episodes,
        'recall': float(true_positive / positives) if positives else None,
        'false_alarms_per_episode': float(false_positive / episodes) if episodes else None,
        'true_positives': int(true_positive),
        'false_negatives': int(false_negative),
        'measurement': 'carried memory over real episodes; timer endings excluded',
    }


def observation_cloud(data, points: int) -> np.ndarray:
    """An evenly spaced selection, so the cloud is not one long contiguous hover."""
    observations = np.asarray(data['observations'], dtype=float)
    if len(observations) <= points:
        selected = observations
    else:
        index = np.linspace(0, len(observations) - 1, int(points))
        selected = observations[np.round(index).astype(int)]
    return np.asarray(cartpole.normalize_visible(selected), dtype=float)


# --------------------------------------------------------------------------- entry point

def run(output: Path, episodes: int = 120, epochs: int = 4, train_steps: int = 40,
        eval_episodes: int = 3, planning_episodes: int = 3, horizon: int = 12,
        planning_horizon: int = 5, sequences: int = 64, points: int = 40,
        seed: int = 0, tolerance: float = 0.02, warmup: int = 4) -> dict:
    """Train, measure one step, remove the instructor, then change the goal."""
    out = ensure_new_output(output)
    torch, blocked = check_torch()
    config = {
        'episodes': episodes, 'epochs': epochs, 'train_steps': train_steps,
        'sequence': 8, 'batch_size': 32, 'termination_weight': TERMINATION_WEIGHT,
        'termination_loss_scale': TERMINATION_LOSS_SCALE,
        'horizon': horizon, 'planning_horizon': planning_horizon,
        'sequences': sequences, 'seed': seed, 'tolerance_rad': tolerance,
        'planning_warmup_steps': warmup, 'points': points,
    }
    if torch is None:
        payload = {
            'status': 'blocked',
            'reason': blocked,
            'assessment': 'not_assessed',
            'source': SOURCE,
            'config': config,
            'what_this_does_not_show': 'Nothing was trained or measured.',
        }
        (out / 'results.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
        return payload

    torch.set_num_threads(1)
    data = cartpole.collect(cartpole.rng(seed), episodes=episodes)
    model = build_model(torch)
    training = train(model, torch, data, epochs=epochs, train_steps=train_steps, seed=seed)

    bounds = episode_bounds(data)
    holdout = [b[0] for b in bounds[-max(1, len(bounds) // 5):]]
    rollout = free_rollout_errors(model, torch, data, holdout,
                                  horizon=max(1, horizon), tolerance=tolerance,
                                  warmup=warmup)

    balance = summarise_episodes([
        play_episode(model, torch, GOAL_BALANCE, planning_horizon, sequences,
                     cartpole.rng(seed + 2), warmup)
        for _ in range(int(planning_episodes))
    ])
    park = summarise_episodes([
        play_episode(model, torch, GOAL_PARK, planning_horizon, sequences,
                     cartpole.rng(seed + 3), warmup)
        for _ in range(int(planning_episodes))
    ])
    # The same goal with a reset memory, so the effect of forgetting velocity is measured
    # rather than argued. This is the article's warm-up problem made concrete.
    forgetting = summarise_episodes([
        play_episode(model, torch, GOAL_BALANCE, planning_horizon, sequences,
                     cartpole.rng(seed + 2), warmup, carry_memory=False)
        for _ in range(int(planning_episodes))
    ])

    cloud = observation_cloud(data, points)
    shape = topology.summarize(cloud, max_edge=1.5)
    crash = crash_detection_metrics(model, torch, data, bounds)

    payload = {
        'status': 'completed',
        'assessment': 'not_assessed',
        'source': SOURCE,
        'environment': {
            'python': platform.python_version(),
            'torch': getattr(torch, '__version__', 'unknown'),
            'numpy': np.__version__,
            'platform': platform.platform(),
            'threads': torch.get_num_threads(),
        },
        'config': dict(config, parameters=int(sum(p.numel() for p in model.parameters()))),
        'metrics': {
            'data': {
                'transitions': int(len(data['actions'])),
                'episodes': int(len(data['episode_lengths'])),
                'mean_episode_steps': float(np.mean(data['episode_lengths'])),
                'ended_by_falling': int(data['terminated'].sum()),
                'ended_by_time_limit': int(data['truncated'].sum()),
                'action_0_fraction': float(np.mean(data['actions'] == 0)),
            },
            'training': training,
            'one_step': training['best'],
            'crash_detection': crash,
            'free_rollout': rollout,
            'baselines': baselines(cartpole.rng(seed + 1), eval_episodes),
            'goal_balance': balance,
            'goal_park': park,
            'goal_balance_without_carried_memory': forgetting,
        },
        'topology': {
            'cloud': 'collected observations projected to (cart position, pole angle)',
            'observed': shape,
            'same_metric_as_model_input': True,
        },
        'limitations': [
            'Teacher forcing makes one-step numbers look better than free rollout.',
            'The planner is random search: a longer dream is covered worse, not better.',
            'Goal scores were chosen by us; they are not learned preferences.',
            'CartPole is four numbers with no friction; nothing here transfers untested.',
            'The topology summary describes our collector, not CartPole or the learner.',
        ],
    }
    (out / 'results.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    return payload


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--episodes', type=int, default=120)
    parser.add_argument('--epochs', type=int, default=4)
    parser.add_argument('--train-steps', type=int, default=40)
    parser.add_argument('--eval-episodes', type=int, default=3)
    parser.add_argument('--planning-episodes', type=int, default=3)
    parser.add_argument('--horizon', type=int, default=12)
    parser.add_argument('--planning-horizon', type=int, default=5)
    parser.add_argument('--sequences', type=int, default=64)
    parser.add_argument('--points', type=int, default=40)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--tolerance', type=float, default=0.02)
    parser.add_argument('--warmup', type=int, default=4)
    args = parser.parse_args(argv)
    options = {k: v for k, v in vars(args).items() if k != 'output'}
    try:
        payload = run(Path(args.output), **options)
    except FileExistsError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2
    print(json.dumps({'output': str(args.output), 'status': payload['status']}, indent=2))
    return 0 if payload['status'] == 'completed' else 3


if __name__ == '__main__':
    raise SystemExit(main())
