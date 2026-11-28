"""Local reviewer presentation and private generated directories; stdlib only."""
from __future__ import annotations

import html
from pathlib import Path
import tempfile

from triadicbrain.assurance.canonical import require_existing_root, require_new_root


def scratch_parent(parent=None):
    # Only the OS-selected scratch location is resolved. Caller-supplied paths
    # must pass custody's unchanged ancestor checks as supplied.
    selected = (Path(tempfile.gettempdir()).resolve(strict=True)
                if parent is None else Path(parent).absolute())
    return require_existing_root(selected)


def private_output(path):
    path = Path(path).absolute()
    if path.exists():
        raise FileExistsError(path)
    path = require_new_root(path)
    path.mkdir(mode=0o700)
    return require_existing_root(path)


def review_questions(verified, originals, decisions):
    """Escaped text/relative links, derived by callers from existing records."""
    sections = []
    for heading, rows in (
        ("What did the software verify?", verified),
        ("Where is the original evidence?", originals),
        ("What still needs a person's decision?", decisions),
    ):
        items = []
        for text, target in rows:
            label = html.escape(str(text))
            if target is not None:
                # Links are generated local members, never supplied input URLs.
                parts = Path(target).parts
                if (not parts or Path(target).is_absolute() or ".." in parts
                        or ":" in target or "\\" in target):
                    raise ValueError("review link must be a local relative member")
                label = f'<a href="{html.escape(target, quote=True)}">{label}</a>'
            items.append(f"<li>{label}</li>")
        sections.append('<section style="background:white;border:1px solid #bcc;padding:1rem;min-width:0;overflow-wrap:anywhere">'
                        f"<h2>{heading}</h2><ul>{''.join(items)}</ul></section>")
    return ('<section aria-label="Review at a glance"><div style="display:grid;'
            'grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem">'
            + ''.join(sections) + '</div><p><strong>A valid hash identifies bytes; it does not establish '
            'source truth, completeness, or authority.</strong></p></section>')
