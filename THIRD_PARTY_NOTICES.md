# Scoped third-party and source notices

The exact extracted implementation and schemas are attributed in NOTICE and
SOURCE_MANIFEST.json. MPL-2.0 is preserved at LICENSE. This note is scoped to
the file allowlist, rather than copying the full development inventory.

Upstream records adaptation of bounded evidence, integrity and human-review
patterns from the following authenticated public packages (identities retained
from upstream NOTICE / THIRD_PARTY_NOTICES.md / COMPONENT_REUSE_DECISIONS.json):

- CoherenceLattice CE alpha.3, archive SHA-256
  `008b7ee0ae77360592c6073844f1b0401ffbbb34d520f02aac3c05a5b4ef2b9a`.
- IntegrityLock CE alpha.5, archive SHA-256
  `90c6844f4de8a0d27f584a2adfdc4ebf693ae41b629b10f03a61c04f013fb736`.
- Open Web Steward CE alpha.2, archive SHA-256
  `84e1b46151cade62ad7fe0b34138fafd82929ab3ab9cd0acba910b0f810bff9f`.

These are upstream provenance statements, not a new independent authentication
or legal clearance. No second crawler, vault, signer or entitlement lifecycle is
included. Separate CoherenceLattice/Sophia/Atlas implementations are excluded.

The six upstream Unicode UCD-derived range-table files are excluded. The exact
CoherenceLattice Product Module Contract / TIAIP component copies and CC-BY-4.0
public profile are also excluded; no confidential TIAIP RC4 material is included.
The copied assurance schema registry describes its original commission identities;
those identifiers are provenance, not operational permission.

No third-party Python package is bundled or required for the documented run.
`schema_validation.py` retains an optional explicit jsonschema engine; this demo
uses the built-in standard-library engine. Python itself is supplied by the user's
existing runtime and retains its own license. Reassess notices if the file set or
runtime packaging changes. Formal publication review remains HOLD.
