# Future B live prototype (`prototypes/future_b_neural_poc`)

This folder holds the periodic \(L=2\) teacher map and the same-origin
Born/SCBA pole extractor. Start from repo-root `FUTURE_B.md`.

## Live (use these)

- `teacher_map_l2.csv` — 12-cell \(E_0^{\mathrm{ED}}\), \(E_0^{\mathrm{Born}}\), \(E_0^{\mathrm{SCBA}}\)
- `week2_born_scba_vs_ed.csv` — Week 2 analysis of that map
- `ed_cutoff_table.csv` — Week 0 cutoff scan, one strong-corner cell
- `l2_periodic_pole.py` — \(k\in\{0,\pi\}\) pole extractor
- `build_teacher_map_l2.py`, `build_week2_table.py`, `atomic_limit_audit.py`

ED Hamiltonian: `src/keldysh4ai/future_b/teacher/holstein_ed.py`.

Do **not** fill the \(L=2\) table from `crossing_block_poc.py` (\(n_k\ge 4\))
or from `src/keldysh4ai/future_b/hopping/chain_scba.py` (open chain).

## Archive-in-folder (POC, not teacher evidence)

`architecture_audit_poc.py`, `physics_routing_poc.py`, `typed_poc.py`,
`real_physics_poc.py`, `run_overnight.py`, and `GENERIC_MODEL_SUFFICIENT`
are proxy/POC records. They do not falsify Future B and do not admit a
router. Leave them here; they were not copied into
`/Users/kawawong/Research/future-b`.
