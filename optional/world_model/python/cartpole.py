"""CartPole, written out so nothing is hidden behind an environment package.

The equations are the standard ones used by the classic CartPole task (Barto, Sutton
and Anderson 1983). They are quoted here rather than imported because the point of
this worked reference is to read the physics, not to call it.

Two design choices are deliberate and are explained in `../README.md`:

1. `terminated` and `truncated` are separate. A pole falling is a consequence of the
   state; the step limit is a stopwatch the model cannot see.
2. `visible()` returns only cart position and pole angle. The velocities are hidden so
   that a memoryless model cannot be correct, which is what forces a recurrent state.
"""
from __future__ import annotations

import numpy as np

DT = 0.02
GRAVITY = 9.8
MASS_CART = 1.0
MASS_POLE = 0.1
HALF_LENGTH = 0.5
FORCE_MAG = 10.0
X_LIMIT = 2.4
THETA_LIMIT = 12.0 * 2.0 * np.pi / 360.0  # 0.20943951023931953 rad
MAX_STEPS = 500

# Indices into the complete four-number state.
CART_POSITION = 0
CART_VELOCITY = 1
POLE_ANGLE = 2
POLE_ANGULAR_VELOCITY = 3

# Indices into the two-number visible observation.
VISIBLE_CART_POSITION = 0
VISIBLE_POLE_ANGLE = 1

ANGULAR_VELOCITY_GAIN = 0.5


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def initial_state(generator: np.random.Generator | None = None) -> np.ndarray:
    """The usual small random offset; the seed decides, not the wall clock."""
    g = generator if generator is not None else rng(0)
    return np.asarray(g.uniform(-0.05, 0.05, size=4), dtype=float)


def step(state: np.ndarray, action: int) -> np.ndarray:
    """One Euler step of the documented CartPole equations."""
    s = np.asarray(state, dtype=float)
    if s.shape != (4,):
        raise ValueError('A CartPole state is four numbers.')
    if action not in (0, 1):
        raise ValueError('Action must be 0 (push left) or 1 (push right).')
    x, x_dot, theta, theta_dot = s
    force = FORCE_MAG if action == 1 else -FORCE_MAG
    total_mass = MASS_CART + MASS_POLE
    cos, sin = np.cos(theta), np.sin(theta)
    temp = (force + MASS_POLE * HALF_LENGTH * theta_dot ** 2 * sin) / total_mass
    theta_acc = (GRAVITY * sin - cos * temp) / (
        HALF_LENGTH * (4.0 / 3.0 - MASS_POLE * cos ** 2 / total_mass)
    )
    x_acc = temp - MASS_POLE * HALF_LENGTH * theta_acc * cos / total_mass
    return np.array(
        [x + DT * x_dot, x_dot + DT * x_acc, theta + DT * theta_dot, theta_dot + DT * theta_acc],
        dtype=float,
    )


def visible(state) -> np.ndarray:
    """What a camera at the rail would report: where things are, not how fast.

    Accepts one state `(4,)` or a batch `(n, 4)` so the planner can reuse it.
    """
    s = np.asarray(state, dtype=float)
    if s.ndim == 1:
        if s.shape != (4,):
            raise ValueError('A CartPole state is four numbers.')
        return np.array([s[CART_POSITION], s[POLE_ANGLE]], dtype=float)
    if s.ndim == 2 and s.shape[1] == 4:
        return np.stack([s[:, CART_POSITION], s[:, POLE_ANGLE]], axis=1)
    raise ValueError('Provide one state (4,) or a batch (n, 4).')


def states_are_complete(observation) -> bool:
    """Does the supplied observation determine the next state?

    Four numbers do: the physics is first order in the four. Two do not, because the
    velocities are missing. This is why the world model needs memory.
    """
    o = np.asarray(observation, dtype=float)
    return o.shape == (4,) and bool(np.isfinite(o).all())


def failed(state: np.ndarray) -> bool:
    s = np.asarray(state, dtype=float)
    return bool(abs(s[CART_POSITION]) > X_LIMIT or abs(s[POLE_ANGLE]) > THETA_LIMIT)


def proportional_controller(state: np.ndarray, bias: float = 0.0) -> int:
    """The three lines from the article: put the cart under the falling pole.

    `bias` is not part of the controller's job. It tilts each episode slightly so the
    collected data contains journeys as well as immaculate balancing; a dataset of
    perfect hovering contains no examples of moving somewhere, and a planner will ask
    for exactly those.
    """
    s = np.asarray(state, dtype=float)
    lean = s[POLE_ANGLE] + ANGULAR_VELOCITY_GAIN * s[POLE_ANGULAR_VELOCITY] + bias
    return 1 if lean > 0 else 0


def rollout(start: np.ndarray, policy, max_steps: int = MAX_STEPS) -> dict:
    """Play one game. `policy(state) -> action`, and the two endings stay distinct."""
    if max_steps <= 0:
        raise ValueError('max_steps must be positive.')
    state = np.asarray(start, dtype=float)
    states = [state]
    actions = []
    terminated = truncated = False
    for _ in range(max_steps):
        action = int(policy(state))
        actions.append(action)
        state = step(state, action)
        states.append(state)
        if failed(state):
            terminated = True
            break
    else:
        truncated = True
    return {
        'states': np.asarray(states, dtype=float),
        'actions': np.asarray(actions, dtype=int),
        'steps': len(actions),
        'terminated': terminated,
        'truncated': truncated,
    }


def collect(
    generator: np.random.Generator,
    episodes: int = 200,
    exploration: float = 0.25,
    max_steps: int = MAX_STEPS,
    bias_scale: float = 0.15,
) -> dict:
    """Gather transitions from a controller that recovers, plus random shoves.

    The dataset has to cover the *actions* a planner will query, not only the
    situations it will start from. `exploration` injects unhelpful shoves that the
    controller then has to dig itself out of, and `bias_scale` moves the games along
    the rail instead of leaving every journey unobserved.
    """
    if episodes <= 0:
        raise ValueError('episodes must be positive.')
    if max_steps <= 0:
        raise ValueError('max_steps must be positive.')
    if not 0.0 <= exploration <= 1.0:
        raise ValueError('exploration is a probability in [0, 1].')
    if not np.isfinite(bias_scale) or bias_scale < 0:
        raise ValueError('bias_scale must be finite and nonnegative.')
    observations, next_observations, states, actions = [], [], [], []
    terminated, truncated = [], []
    lengths = []
    for _ in range(episodes):
        bias = float(generator.uniform(-bias_scale, bias_scale))
        state = initial_state(generator)
        played = 0
        for _ in range(max_steps):
            if generator.random() < exploration:
                action = int(generator.integers(0, 2))
            else:
                action = proportional_controller(state, bias=bias)
            next_state = step(state, action)
            observations.append(visible(state))
            # The successor is recorded explicitly. Without it the final transition of an
            # episode — the only one that carries a crash label — has no prediction target
            # and is silently dropped from training.
            next_observations.append(visible(next_state))
            states.append(state)
            actions.append(action)
            played += 1
            failed_now = failed(next_state)
            ended = failed_now or played == max_steps
            terminated.append(failed_now)
            truncated.append(ended and not failed_now)
            state = next_state
            if ended:
                break
        lengths.append(played)
    return {
        'observations': np.asarray(observations, dtype=float),
        'next_observations': np.asarray(next_observations, dtype=float),
        'states': np.asarray(states, dtype=float),
        'actions': np.asarray(actions, dtype=int),
        'terminated': np.asarray(terminated, dtype=bool),
        'truncated': np.asarray(truncated, dtype=bool),
        'episode_lengths': np.asarray(lengths, dtype=int),
    }


def normalize_visible(observation) -> np.ndarray:
    """Put cart position and pole angle on the same scale.

    Without this the network decides that position errors matter about ten times more
    than angle errors, because position roams over about 2 and angle over about 0.2.
    The angle is the one that ends the game.
    """
    o = np.asarray(observation, dtype=float)
    return o / np.array([X_LIMIT, THETA_LIMIT], dtype=float)


def denormalize_visible(observation) -> np.ndarray:
    o = np.asarray(observation, dtype=float)
    return o * np.array([X_LIMIT, THETA_LIMIT], dtype=float)


def trust_horizon(errors, tolerance: float) -> tuple[int, int | None]:
    """How many steps ahead the daydream stays inside `tolerance`.

    Returns `(horizon, first_failure)` where `horizon` counts leading errors within
    tolerance and `first_failure` is the index of the first error outside it, or
    `None` when every supplied depth passed. This is a ceiling, not a recommendation:
    how far the model stays accurate and how far ahead it is useful to plan are two
    different numbers.
    """
    values = np.asarray(errors, dtype=float).ravel()
    if values.size == 0:
        raise ValueError('At least one depth is required.')
    if not np.isfinite(values).all():
        raise ValueError('Errors must be finite.')
    if not tolerance > 0:
        raise ValueError('tolerance must be positive.')
    outside = np.flatnonzero(values > tolerance)
    horizon = int(outside[0]) if outside.size else int(values.size)
    return horizon, (int(outside[0]) if outside.size else None)
