"""PARVIS L2 Phase - Requirement Normalization and ID Assignment"""

__version__ = "1.0.0"
__author__ = "foxBMS Team"

from .reqid import (
    generate_requirement_id,
    create_id_registry,
    validate_requirement_id,
    load_extracted_requirements,
    assign_ids_to_requirements,
)

from .transformer import (
    normalize_content,
    normalize_terminology,
    classify_requirement,
    calculate_quality_score,
    transform_requirements,
)

__all__ = [
    "generate_requirement_id",
    "create_id_registry",
    "validate_requirement_id",
    "load_extracted_requirements",
    "assign_ids_to_requirements",
    "normalize_content",
    "normalize_terminology",
    "classify_requirement",
    "calculate_quality_score",
    "transform_requirements",
]
