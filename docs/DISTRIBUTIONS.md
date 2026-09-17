# Distribution boundaries

Three different objects share this project name. They are not the same.

| object | what it is | how you get it |
|---|---|---|
| **GitHub research artifact** | Frozen LiF records, provenance, docs, native excerpts, historical patches | `git clone` / tagged source tree |
| **Python sdist** | Buildable source + tests + the canonical frozen files those tests open | `future_b-*.tar.gz` |
| **Python wheel** | Installable reference library (`future_b`) | `future_b-*-py3-none-any.whl` |

The wheel is **not** the methods archive. It does not ship benchmarks,
docs, patches, or historical tooling.

The sdist is **not** a dump of the GitHub tree. It includes only what
is required to install and run `pytest` from the unpacked tarball.

Historical native adapters (`patches/`, `historical/c2_oracle.py`) are
repository artifacts. They are not a supported runtime API and are not
a public FEP-DMC plugin.

See [CAPABILITIES.md](CAPABILITIES.md) for what the snapshot can and
cannot do.
