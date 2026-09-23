# Primer 07 — From a measurement to a differential equation

A **quantity** is something represented by a number and, where appropriate, a unit. A length of 2 metres and a duration of 2 seconds share a number but not a meaning. A **state** is the collection of quantities a model uses to predict what happens next. Position alone is often not enough: the same position can be reached moving in opposite directions. Position and velocity can be a better state, but only for a model whose other relevant influences are known or represented.

A **function** maps inputs to outputs. Writing q(t) says that position depends on time. An average rate is (q(t+h)-q(t))/h. A derivative is the limit of that rate as the interval tends to zero, when the limit exists. Derivatives have units: metres divided by seconds for velocity, metres divided by seconds squared for acceleration. A finite difference estimates a derivative from samples. It has a chosen step and is not the definition of the derivative itself.

An ordinary differential equation, or **ODE**, relates a time derivative to the state and time: dz/dt=f(t,z). An initial condition gives z at a starting time. Together, under appropriate existence and uniqueness assumptions, they define a local trajectory. A partial differential equation, or **PDE**, involves a function of several independent variables and partial derivatives, such as u_t=nu*u_xx. Boundary conditions describe behavior at the spatial boundary; initial conditions describe the starting field. They are different constraints.

A **residual** is the amount by which a proposed answer fails to satisfy a stated equation. For x'=x, a proposed x(t) has residual x'(t)-x(t). A residual can be small where measured while the answer is wrong elsewhere, especially if initial or boundary information is absent. For x'=x, all curves a*exp(t) have zero residual; without x(0), the amplitude a is undetermined. Physics without adequate observations does not identify every parameter or state.

A **forward problem** starts from a model and parameters and predicts observations. An **inverse problem** uses observations to estimate parameters or hidden states. Identifiability asks whether different parameter choices produce the same observed output. Optimization asks whether an algorithm finds a useful fit. These are not the same question. More optimization cannot distinguish two exactly observationally equivalent parameter values.

A **loss** is a number measuring disagreement. A squared-error loss averages squared residuals. A gradient lists the derivatives of that number with respect to adjustable parameters. A small negative-gradient step often decreases a smooth loss locally; it need not decrease every other objective or work for a large step. Automatic differentiation differentiates a program using the chain rule. It is neither symbolic algebra in general nor a guarantee that the program describes the intended physics.

A **neural network** here is a trainable differentiable function, made by composing matrix operations and nonlinear functions. The weights are its adjustable parameters. An activation such as tanh makes the function nonlinear. Training chooses weights to reduce a loss on selected samples. Evaluation uses different samples under a declared protocol. There is no magic step that turns a network output into a calibrated measurement.

## A worked example

Let q(t)=cos(t), with dimensionless time. Its velocity is -sin(t), its acceleration is -cos(t), and therefore q''=-q. Define p=q'. The second-order equation becomes a pair of first-order equations: q'=p and p'=-q. The state is z=(q,p). At t=0 it is (1,0). A time-stepping algorithm approximates how that state changes. Stage 24 shows that preserving a geometric property of this update does not make the update exact.

## First practice

Calculate an average speed for a measured distance of 3 m over 0.5 s. Explain why that is not necessarily instantaneous speed. Give two different solutions of x'=x and the initial conditions that distinguish them. For q=cos(t), evaluate position, velocity and acceleration at zero. Answers: 6 m/s; within-window changes are unknown; exp(t) and 2 exp(t), with initial values 1 and 2; (1,0,-1).

Read this primer before Stage 21. Revisit Primer 04 for matrix derivatives and Primer 06 for uncertainty. The new course examples explicitly label dimensionless variables rather than assigning invented physical units.
