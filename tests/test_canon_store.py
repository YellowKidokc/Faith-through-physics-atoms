from pathlib import Path


def test_canon_store_directories_exist():
    base = Path("canon-store")
    for sub in [
        "sources",
        "papers",
        "runs",
        "atoms/candidate",
        "atoms/admitted",
        "atoms/rejected",
        "atoms/predicate",
        "predicates",
        "prompts",
        "templates",
    ]:
        assert (base / sub).is_dir(), f"missing {sub}"
