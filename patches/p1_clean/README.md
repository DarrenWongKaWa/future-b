# Clean P1 patch — historical only

Not a public install step. `apply_p1_clean.py` needs a private
C2_fixture adapter tree that is **not** in the GitHub snapshot.

- Missing `--src` exits non-zero and does **not** delete `--dst`.
- Existing `--dst` is refused unless `--overwrite`.
- Do not apply to historical C2/C5 evidence directories.

Native rebuild from public upstream is **not** one-click; see
`docs/REPRODUCIBILITY.md` and `docs/CAPABILITIES.md`.
