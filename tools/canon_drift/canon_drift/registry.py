import json
from pathlib import Path


def repository_root(start=None):
    here = Path(start or __file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "canon").is_dir() and (parent / ".git").exists():
            return parent
    raise FileNotFoundError("cannot locate repository canon registry")


class Registry:
    def __init__(self, root=None):
        self.root = Path(root) if root else repository_root()
        self.current = self._read("canon/atoms/equations/master-equation.v3.json")
        self.retired = self._read("canon/retired/master-equation-retired-forms.json")
        self.rules = self._read("canon/drift-rules/master-equation.rules.json")
        self.autolink_terms = self._read("canon/autolink/canon_autolink_terms.json")

    def _read(self, relative):
        with (self.root / relative).open(encoding="utf-8") as handle:
            return json.load(handle)
