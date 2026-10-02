"""R1 grouped-measure toy (Stage F1-F3), the finite signed model behind research/r1_grouped.

  grouped_toy   toy model, grouped measures w_A / w_B, partitions and window operators
  kernels       exact transition kernels and stationarity residuals
  dense_oracle  independent dense enumeration oracle
  run_f1_f3     the F1-F3 checks (``python -m future_b.r1_grouped.run_f1_f3 --out DIR``)

One function of grouped_toy uses keldysh4ai.diagram_compiler (imported lazily).
Derivation and report: research/r1_grouped/DERIVATION.md and REPORT.md.
"""
