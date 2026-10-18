"""Local-first foundation for the AI Controls Evidence Platform.

The package records bounded system-generated evidence.  It does not grant
authority, provide assurance, or make a compliance determination.
"""

from __future__ import annotations

PRODUCT_NAME = "Control Anchor"
PRODUCT_CATEGORY = "AI Controls Evidence Platform"
PRODUCT_VENDOR = "Control Anchor by UVLM"
PRODUCT_VERSION = "0.2.0-alpha.1"
BRAND_STATUS = "PROVISIONAL_PENDING_FORMAL_TRADEMARK_DOMAIN_AND_LEGAL_CLEARANCE"
VERSION = "0.2.0a1"
AUTHORITY_EFFECT = "NONE"
NONASSURANCE_HEADLINE = (
    "SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED"
)
NONASSURANCE_NOTICE = (
    "SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED."
)
REPORT_NOTICE = (
    "SYSTEM-GENERATED CONTROL EVIDENCE. NO ASSURANCE OR COMPLIANCE OPINION "
    "IS PROVIDED. Management and qualified professionals must determine "
    "applicable criteria, scope, materiality, evidence sufficiency, control "
    "effectiveness, and any conclusion."
)

__all__ = [
    "AUTHORITY_EFFECT",
    "BRAND_STATUS",
    "NONASSURANCE_HEADLINE",
    "NONASSURANCE_NOTICE",
    "PRODUCT_NAME",
    "PRODUCT_CATEGORY",
    "PRODUCT_VENDOR",
    "PRODUCT_VERSION",
    "REPORT_NOTICE",
    "VERSION",
]
