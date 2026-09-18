"""Experimental diagram compiler over the R1 fixed-order family (Task 1).

Research subsystem; see docs/DIAGRAM_COMPILER_TASK1.md. Not part of the
Future B v1.x release surface and not used by C0/P1.
"""

from .canonical import (
    IrError,
    build_scalar_diagram,
    build_scalar_ir,
    build_twoband_diagram,
    build_twoband_ir,
    chord_slots,
    diagram_id,
    enumerate_pairings,
    open_chord_slots,
    validate_ir,
)
from .evaluator import (
    Binding,
    BindingError,
    compile_evaluator,
    evaluate_dag,
    evaluate_diagramwise,
    factor_value,
    numeric_close,
    validate_binding,
)
from .graph import DagNode, DagStats, EvalDag, leaf_key, lower_diagramwise, lower_grouped
from .ir import (
    MODEL_SCALAR,
    MODEL_TWOBAND,
    OBJECT_SHARED_X_GROUP,
    RULE_VERSION,
    SCHEMA_VERSION,
    SERIES_FULL,
    Diagram,
    DiagramIR,
    Factor,
    Family,
    MomentumForm,
    Variables,
)
from .r1_import import ImportRejected, import_r1_binding, import_r1_spec

__all__ = [
    "Binding",
    "BindingError",
    "DagNode",
    "DagStats",
    "Diagram",
    "DiagramIR",
    "EvalDag",
    "Factor",
    "Family",
    "ImportRejected",
    "IrError",
    "MODEL_SCALAR",
    "MODEL_TWOBAND",
    "MomentumForm",
    "OBJECT_SHARED_X_GROUP",
    "RULE_VERSION",
    "SCHEMA_VERSION",
    "SERIES_FULL",
    "Variables",
    "build_scalar_diagram",
    "build_scalar_ir",
    "build_twoband_diagram",
    "build_twoband_ir",
    "chord_slots",
    "compile_evaluator",
    "diagram_id",
    "enumerate_pairings",
    "evaluate_dag",
    "evaluate_diagramwise",
    "factor_value",
    "import_r1_binding",
    "import_r1_spec",
    "leaf_key",
    "lower_diagramwise",
    "lower_grouped",
    "numeric_close",
    "open_chord_slots",
    "validate_binding",
    "validate_ir",
]
