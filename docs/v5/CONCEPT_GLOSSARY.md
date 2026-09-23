# Physics extension glossary

**State:** quantities included in the model's predictive description at a time; it need not equal the complete physical world.

**Vector field:** a tangent direction and rate assigned at each state. A smooth field has a local smooth flow, with domain conditions.

**Flow:** a family of time-evolution maps obtained by solving an equation. A chosen discrete update need not have all exact-flow properties.

**Diffeomorphism:** smooth invertible map with a smooth inverse. A smooth bijection alone does not guarantee this.

**Jacobian:** matrix of first partial derivatives of a vector-valued map. The constraint Jacobian A=DC is distinct from canonical symplectic J.

**Hessian:** matrix of second partial derivatives of a scalar. The velocity Hessian of a Lagrangian controls whether a regular acceleration solve is available.

**Momentum:** in the Lagrangian formulation, derivative of L with respect to velocity. It equals mass times velocity only for the corresponding elementary kinetic term.

**Hamiltonian:** a scalar used to generate canonical phase-space dynamics; identification with physical energy requires the appropriate formulation.

**Lagrangian:** a scalar of coordinates, velocities and possibly time used in a variational formulation. T−V is an important case, not every possible form.

**Legendre transform:** here, H=p·v−L after inverting p=partial L/partial v under regularity conditions.

**Symplectic:** preserving a specified nondegenerate closed two-form; in canonical matrix checks, D(Phi)^T J D(Phi)=J. Not synonymous with exact original-energy conservation.

**Constraint:** a condition defining feasible states. Its satisfaction alone does not establish correct dynamics.

**Retraction:** a locally first-order-correct map from tangent updates back to a manifold. It need not equal the exponential map at finite steps.

**Residual:** discrepancy in a stated equation or condition. Distinguish it from reference-solution error, observed-data error and parameter error.

**Collocation point:** a location where a differential residual is evaluated, not necessarily a measured training label.

**Identifiability:** ability to distinguish parameter/state choices from the available observations under a model. Different from optimization success.

**Gradient conflict:** negative alignment between objective gradients under a declared parameter-space inner product.

**Common descent:** a direction yielding appropriate local decrease for multiple objectives; strict common descent may not exist.

**Domain decomposition:** representing a problem on subdomains with appropriate coupling/interface conditions. Separate interior accuracy is insufficient.

**Separable representation:** sum of products of per-coordinate factors. Compact factors do not remove the cost of materializing every dense output.

**Neural operator:** a learned map between functions/fields. A fixed analytic spectral solver is not a neural operator.

**DeepONet:** branch/trunk operator representation combining input-function sensor features with output-coordinate features.

**FNO:** a Fourier neural operator with learned spectral mixing. Frequency truncation, boundary assumptions and generalization tests remain relevant.

**Neural ODE:** an ODE with a learned parameterized right-hand side. Direct differentiation and adjoint sensitivity are different implementations.

**Equivariance:** the output transforms consistently with a specified input transformation. It does not imply every physical conservation law.

**Manufactured test:** a problem generated from known equations/solutions to verify a numerical implementation. Not empirical validation.

**Constructed observation transform:** an operation applied to real measurements; the transformed outcome is not a newly measured physical event.

**Independent validation:** comparison against observations or reference information not used to fit or choose the method under the stated protocol.
