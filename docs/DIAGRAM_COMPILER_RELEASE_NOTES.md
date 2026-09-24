# Diagram Compiler v0.1.0 — Research Preview

This is an **experimental research preview** of a bounded fixed-order
diagram compiler. It is separate from Future B v1.2.0.

Established within the tested scope:

- explicit, serializable DiagramIR for the admitted fixed-order scalar and
  Hermitian two-band families;
- exact evaluator generation with ordered structural DAG sharing;
- versioned `propagator_only_v1` cheap state-weight evaluation;
- reciprocal cheap transition scores;
- Design-B delayed acceptance for `positive_real_F_v1`;
- typed SSA/CFG NativeKernelIR;
- deterministic Fortran `fortran_v1` emission and `native_kernel_v1` runtime;
- compiled native differential validation;
- LEVEL 2 validation against pinned public FEP-DMC tooling without changing
  `update_swap` or public P1.

Not established:

- arbitrary-order or arbitrary-topology compilation;
- automatic Feynman-rule derivation or generic QFT support;
- production FEP-DMC generated-kernel replacement;
- public P1 replacement;
- speedup or equal-precision Monte Carlo gain;
- finite-temperature or broad multiband generality;
- broad material validation.

The release is a methods artifact and validation record, not a production
solver or a Future B scientific release.
