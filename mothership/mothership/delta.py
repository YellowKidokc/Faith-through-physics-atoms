"""Delta fast path: which addresses are touched by a text diff.

Computes character-level changed ranges with difflib.SequenceMatcher and returns
addresses whose anchor region (exact text expanded by its prefix/suffix bounds)
intersects any changed range.  Runs in microseconds without re-reading papers.
"""

from __future__ import annotations

import difflib
from typing import Any

from mothership.address import Address


def _changed_ranges(old_text: str, new_text: str) -> list[tuple[int, int]]:
    """Return sorted, non-overlapping (start, end) character ranges that changed."""
    sm = difflib.SequenceMatcher(None, old_text, new_text)
    ranges: list[tuple[int, int]] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            # Map changes back into the *old* text coordinate space.  Addresses
            # were minted against the old version, so we test against old ranges.
            ranges.append((i1, i2))
    return ranges


def _anchor_range(address: Address, text: str) -> tuple[int, int]:
    """Return the inclusive character range covered by exact +/- prefix/suffix.

    The locator offsets are authoritative for the exact span; prefix/suffix
    define the surrounding fingerprint window.  For delta purposes we expand
    the exact span by the prefix and suffix lengths, clamped to document bounds.
    """
    start, end = address.offsets
    if not (0 <= start < end <= len(text)):
        start = max(0, start)
        end = min(len(text), end)
    window_start = max(0, start - len(address.prefix))
    window_end = min(len(text), end + len(address.suffix))
    return window_start, window_end


def _ranges_intersect(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] < b[1] and b[0] < a[1]


def compute_touched_addresses(
    old_text: str,
    new_text: str,
    addresses: list[Address],
) -> list[Address]:
    """Return addresses whose anchor region intersects changed character ranges."""
    changed = _changed_ranges(old_text, new_text)
    touched: list[Address] = []
    for address in addresses:
        anchor = _anchor_range(address, old_text)
        if any(_ranges_intersect(anchor, cr) for cr in changed):
            touched.append(address)
    return touched
