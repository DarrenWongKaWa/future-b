"""``future-b-fepdmc``: command-line entry point of the FEP-DMC toolkit.

  future-b-fepdmc prepare  <tree> [--profile fixes|research] [--dry-run]
  future-b-fepdmc run      {prepare-tables,ez} <material> [n_chains] [options]
  future-b-fepdmc compare  <runs_A> <runs_C> <material> <E_bare> <tau_max> [...]
  future-b-fepdmc validate [--build TREE] [--kernels native,pure,mixed] [...]

Run ``future-b-fepdmc <command> --help`` for the options of each command.
"""

from __future__ import annotations

import sys

COMMANDS = {
    "prepare": "future_b.fepdmc.prepare",
    "run": "future_b.fepdmc.runner",
    "compare": "future_b.fepdmc.pooled",
    "validate": "future_b.fepdmc.validate",
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help") or argv[0] not in COMMANDS:
        print(__doc__)
        return 0 if argv and argv[0] in ("-h", "--help") else 2
    from importlib import import_module
    return int(import_module(COMMANDS[argv[0]]).main(argv[1:]) or 0)


if __name__ == "__main__":
    sys.exit(main())
