"""Offline manifest consistency and local Markdown-link checks; stdlib only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


def repository_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or '..' in path.parts or '\\' in relative:
        raise ValueError(f'unsafe repository path: {relative}')
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f'path outside repository: {relative}')
    return target


def check_manifest(root: Path, tracked: set[str]) -> list[str]:
    errors = []
    manifest = json.loads((root / 'SOURCE_MANIFEST.json').read_bytes())
    seen = set()
    for group in ('copied_files', 'new_or_adapted_files'):
        for row in manifest[group]:
            relative = row['path']
            if relative in seen:
                errors.append(f'duplicate manifest path: {relative}')
            seen.add(relative)
            try:
                raw = repository_path(root, relative).read_bytes()
            except (OSError, ValueError) as exc:
                errors.append(f'{relative}: {exc}')
                continue
            digest = hashlib.sha256(raw).hexdigest()
            if digest != row['candidate_sha256']:
                errors.append(f'SHA256 mismatch: {relative}')
            if 'bytes' in row and len(raw) != row['bytes']:
                errors.append(f'byte count mismatch: {relative}')
            if group == 'copied_files':
                blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                if digest != row['original_sha256'] or blob != row['original_git_blob']:
                    errors.append(f'extracted source identity mismatch: {relative}')
    # The commit binds the manifest itself; a self-hash would be circular.
    expected = tracked - {'SOURCE_MANIFEST.json'}
    for relative in sorted(expected - seen):
        errors.append(f'tracked file missing from manifest: {relative}')
    for relative in sorted(seen - expected):
        errors.append(f'manifest path is not a tracked file: {relative}')
    return errors


def prose_lines(text: str) -> list[tuple[int, str]]:
    result = []
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if marker:
            token, rest = marker.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


def markdown_anchors(text: str) -> set[str]:
    anchors = set()
    for _, line in prose_lines(text):
        for match in re.finditer(r'<[^>]+\b(?:id|name)=["\']([^"\']+)["\']', line):
            anchors.add(match.group(1))
        heading = re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?$', line)
        if not heading:
            continue
        label = re.sub(r'<[^>]+>', '', heading.group(1)).lower()
        base = re.sub(r'[^\w\- ]', '', label).replace(' ', '-')
        slug, suffix = base, 0
        while slug in anchors:
            suffix += 1
            slug = f'{base}-{suffix}'
        anchors.add(slug)
    return anchors


def check_links(root: Path, tracked: set[str]) -> list[str]:
    errors = []
    # Inline destinations and reference definitions, excluding fenced/inline code.
    inline = re.compile(r'!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+["\'][^)]*)?\)')
    definition = re.compile(r'^ {0,3}\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))')
    for relative in sorted(p for p in tracked if p.endswith('.md')):
        path = repository_path(root, relative)
        for number, original in prose_lines(path.read_text(encoding='utf-8')):
            line = re.sub(r'(`+).*?\1', '', original)
            targets = [next(g for g in match.groups() if g is not None)
                       for pattern in (inline, definition) for match in pattern.finditer(line)]
            for target in targets:
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    continue  # External/private URLs are intentionally not fetched.
                destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                if not destination.is_relative_to(root.resolve()):
                    errors.append(f'{relative}:{number}: link outside repository: {target}')
                    continue
                if not destination.exists():
                    errors.append(f'{relative}:{number}: missing local target: {target}')
                elif parsed.fragment and destination.suffix == '.md':
                    if unquote(parsed.fragment) not in markdown_anchors(destination.read_text(encoding='utf-8')):
                        errors.append(f'{relative}:{number}: missing local anchor: {target}')
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    tracked = set(subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=root, timeout=10).decode('utf-8').strip('\0').split('\0'))
    errors = check_manifest(root, tracked) + check_links(root, tracked)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(tracked) - 1} manifest-bound files; extracted identities; local Markdown destinations/anchors.')
    print('External links, rendering, security, source truth and production readiness are not certified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
