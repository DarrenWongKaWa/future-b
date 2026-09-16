"""Scoped R1 vs CSE statement for the tested fixed-order domain.

This module does not implement a real-material grouped consumer.
The material connection is documented as future work.
"""

from __future__ import annotations

# M3-D campaign overall R1/CSE total-time ratio (same compiled measure).
R1_OVER_CSE_OVERALL = 0.9992
R1_OVER_CSE_TIER_MIN = 0.9863
R1_OVER_CSE_TIER_MAX = 1.0034

OBJECTS = ("BOUND_C", "SHARED_X_GROUP", "SUMMED_KERNEL")


def scoped_status() -> dict:
    return {
        "evaluator": "VALIDATED_IN_SCOPE",
        "additional_cse_gain": "NO_ADDITIONAL_CSE_GAIN_ESTABLISHED",
        "r1_over_cse_overall": R1_OVER_CSE_OVERALL,
        "material_grouped_consumer": "FUTURE_WORK",
        "objects": OBJECTS,
    }
