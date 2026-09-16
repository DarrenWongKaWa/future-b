# Release checklist

- [x] P1 clean path audited (fixture dump/reverse gated; counters independent)
- [x] 0.956 binary == released clean path (`f9518a21…`, gating before compile)
- [x] Existing clean confirmation **not** rerun
- [x] Relative SE / 95% half-width reported for C5 and confirm
- [x] P4/P5 stopped as `FUTURE_WORK_CANDIDATE` (no new data, no fit)
- [x] R1 material consumer stopped; roadmap written
- [x] 1% GS documented, not pursued
- [x] Upstream vs Future B contributions separated (`docs/PROVENANCE.md`)
- [x] HDF5 / Nature PDF / Docker / QE objects excluded from public tarball
- [x] Public tree has no machine-local home paths
- [x] `CITATION.cff` has no fake URL; tag **`v1.0.0`**
- [x] Unit tests for DA, reverse, energy zero, statistics, R1 statement, P1 source
- [x] `project_status = CLOSED`
- [x] `CITATION.cff` `repository-code` = `https://github.com/DarrenWongKaWa/future-b`
- [ ] `git tag v1.0.0` on the **staging** tree (not the 56 GB working copy)
- [ ] Human review of LICENSE_AUDIT.md before first public push

Blockers that must be resolved before **public upload**:

1. Push **`release/github_staging/`** (or the tarball), not the private
   working tree.
2. Do not push `FEP-DMC-Data/`, `closure/**/lif-sp3_epwan.h5`, or
   `references/*natphys*.pdf`.
3. Do not push Docker image tarballs or `perturbo.x` / `.o` / `libpw.a`.
4. Fill `repository-code` after the GitHub remote is created.
