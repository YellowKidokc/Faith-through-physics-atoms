"""Scan every v12 stage folder, work out its state, set the folder icon.
States: empty / working / done / failed.
  done   = a file named _STATUS.done exists
  failed = a file named _STATUS.failed exists
  working= any content file present
  empty  = nothing but scaffolding
Also prunes empty folders when the domain is locked (--prune-locked).
Usage: python _scripts/set_folder_icons.py [--prune-locked]
"""
import os, sys, ctypes, glob

REPO  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(REPO, "_icons")
IGNORE = {"readme.md", "desktop.ini", ".fisnote", "_status.done",
          "_status.failed", "thumbs.db"}

FILE_ATTRIBUTE_READONLY = 0x01
FILE_ATTRIBUTE_SYSTEM   = 0x04
FILE_ATTRIBUTE_HIDDEN   = 0x02


def state_of(path):
    if os.path.exists(os.path.join(path, "_STATUS.failed")):
        return "failed"
    if os.path.exists(os.path.join(path, "_STATUS.done")):
        return "done"
    for dirpath, dirs, files in os.walk(path):
        for fn in files:
            if fn.lower() not in IGNORE:
                return "working"
    return "empty"


def set_icon(path, stage, state):
    ico = os.path.join(ICONS, f"{stage}__{state}.ico")
    if not os.path.exists(ico):
        return False
    ini = os.path.join(path, "desktop.ini")
    if os.path.exists(ini):
        ctypes.windll.kernel32.SetFileAttributesW(ini, 0x80)  # clear to rewrite
    with open(ini, "w", encoding="utf-8") as f:
        f.write("[.ShellClassInfo]\n")
        f.write(f"IconResource={ico},0\n")
        f.write(f"InfoTip={stage} - {state}\n")
    ctypes.windll.kernel32.SetFileAttributesW(
        ini, FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_HIDDEN)
    ctypes.windll.kernel32.SetFileAttributesW(
        path, FILE_ATTRIBUTE_READONLY)   # required for Windows to read desktop.ini
    return True


def scan(prune_locked=False):
    counts = {"empty": 0, "working": 0, "done": 0, "failed": 0}
    pruned = []
    for domain in sorted(os.listdir(REPO)):
        droot = os.path.join(REPO, domain)
        if not os.path.isdir(droot) or domain.startswith(("_", ".")):
            continue
        locked = os.path.exists(os.path.join(droot, "_STATUS.locked"))
        for stage in sorted(os.listdir(droot)):
            p = os.path.join(droot, stage)
            if not os.path.isdir(p):
                continue
            st = state_of(p)
            counts[st] = counts.get(st, 0) + 1
            if locked and prune_locked and st == "empty":
                # domain is canon-locked and this branch was never used
                for f in glob.glob(os.path.join(p, "*")):
                    os.remove(f)
                os.rmdir(p)
                pruned.append(f"{domain}/{stage}")
                continue
            set_icon(p, stage, st)
    return counts, pruned


if __name__ == "__main__":
    counts, pruned = scan("--prune-locked" in sys.argv)
    total = sum(counts.values())
    print(f"scanned {total} stage folders")
    for k in ("empty", "working", "done", "failed"):
        print(f"  {k:8s} {counts.get(k,0)}")
    if pruned:
        print(f"\npruned {len(pruned)} unused folders from locked domains:")
        for p in pruned:
            print("  -", p)
    print("\nIf icons don't refresh, press F5 in the file manager "
          "or run: ie4uinit.exe -show")
