"""Historical fixed-order R1 *result metadata* only.

This public module is not an R1 evaluator. The compile-once recursive
implementation lived under the private `keldysh4ai.scheme_d` tree and
was not shipped in v1.0.0. Do not import this package expecting graph
build, rebind, or CSE comparison kernels.
"""

from __future__ import annotations

R1_OVER_CSE_OVERALL = 0.9992
R1_OVER_CSE_TIER_MIN = 0.9863
R1_OVER_CSE_TIER_MAX = 1.0034

OBJECTS = ("BOUND_C", "SHARED_X_GROUP", "SUMMED_KERNEL")
PUBLIC_RELEASE = "HISTORICAL_RESULT_METADATA"


def scoped_status() -> dict:
    return {
        "public_release": PUBLIC_RELEASE,
        "evaluator_in_this_package": False,
        "evaluator": "VALIDATED_IN_SCOPE",
        "additional_cse_gain": "NO_ADDITIONAL_CSE_GAIN_ESTABLISHED",
        "r1_over_cse_overall": R1_OVER_CSE_OVERALL,
        "material_grouped_consumer": "FUTURE_WORK",
        "objects": OBJECTS,
    }
