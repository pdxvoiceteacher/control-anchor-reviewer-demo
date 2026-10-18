# Scoped third-party and source notices

The exact extracted implementation and schemas are attributed in NOTICE and
SOURCE_MANIFEST.json. MPL-2.0 is preserved at LICENSE. This note is scoped to
the file allowlist, rather than copying the full development inventory.

The following are upstream historical records, retained for attribution context.
COMPONENT_REUSE_DECISIONS.json at source commit
139932846cb1b6bf1571158464d89513d4e381f8 places their adaptations in the excluded
src/triadicbrain/workbench/ tree, not the assurance extraction:

- CoherenceLattice CE alpha.3, archive SHA-256
  `008b7ee0ae77360592c6073844f1b0401ffbbb34d520f02aac3c05a5b4ef2b9a`.
- IntegrityLock CE alpha.5, archive SHA-256
  `90c6844f4de8a0d27f584a2adfdc4ebf693ae41b629b10f03a61c04f013fb736`.
- Open Web Steward CE alpha.2, archive SHA-256
  `84e1b46151cade62ad7fe0b34138fafd82929ab3ab9cd0acba910b0f810bff9f`.

CoherenceLattice CE maps to workbench/pipeline.py and contracts.py; IntegrityLock
maps to workbench/dossier.py and verify.py; Open Web Steward maps to
workbench/templates.py and web.py. None is included. In particular, Open Web
Steward's upstream MPL-2.0 AND CC-BY-4.0 entry does not establish a CC-BY obligation
for this demo's different assurance/web.py. These are source-history statements,
not evidence of a hidden component inclusion or a new legal clearance.
Separate CoherenceLattice/Sophia/Atlas implementations are also excluded.

The six upstream Unicode UCD-derived range-table files are excluded. The exact
CoherenceLattice Product Module Contract / TIAIP component copies and CC-BY-4.0
public profile are also excluded; no confidential TIAIP RC4 material is included.
The copied assurance schema registry describes the 12 commission-supplied
schemas included here. Inspection found no embedded third-party license exception,
attribution requirement, proprietary criteria text or external schema reference
in that set. Their JSON Schema dialect URLs identify a format; they do not import
another component. Commission identities remain provenance, not operational
permission. See the scoped rights note in PUBLICATION_REVIEW.md.

No third-party Python package is bundled or required for the documented run.
`schema_validation.py` retains an optional explicit jsonschema engine; this demo
uses the built-in standard-library engine. Python itself is supplied by the user's
existing runtime and retains its own license. Reassess notices if the file set or
runtime packaging changes. The methods appendix cites two additional pedagogy
documents; their source/permission scope is recorded separately in the manifest
and publication checklist. Publication permission remains a final-content decision.
