# COLAB_SINGLE_FILE.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** True single-file deployment — everything in one notebook, no imports

---

## What It Is

The completely self-contained notebook. Where `COLAB_MASTER.ipynb` (v2.0) uses a modular Component class architecture and expects `theophysics_core.py` to be available, `COLAB_SINGLE_FILE.ipynb` includes everything — constants, class definitions, test implementations, and visualization — in a single notebook with no external dependencies.

Upload this one notebook to any Google Colab instance, run all cells, get the full results. No other files needed.

---

## Why This Exists

In an ideal world, you'd always have access to the full file structure. In practice:
- Shared Colab sessions may not persist uploaded files between sessions
- Some users prefer not to upload auxiliary files
- Sharing a single notebook URL is simpler than sharing a repository
- Presentations benefit from a notebook that's entirely self-contained

`COLAB_SINGLE_FILE.ipynb` is the answer to "can I just share one link?" Yes. This is that link.

---

## Tradeoffs

**Advantages:**
- Zero external dependencies
- Share one file, run one file, get all results
- Immune to version drift between files (everything is locked in one document)

**Disadvantages:**
- Very long notebook (all definitions + all tests + all visualization = many cells)
- Harder to modify individual components (changes must be made in multiple places if refactoring)
- Larger file size

The single-file format is optimized for distribution and first-contact, not for ongoing development.

---

## Interpretation

Every serious research project needs a "one-file" version. The paper serves this purpose in traditional science — a single document that contains the claim, the method, and the result. For computational science, the Colab notebook is the equivalent.

`COLAB_SINGLE_FILE.ipynb` is the paper equivalent: self-contained, portable, and complete. You don't need a development environment, you don't need Python installed, you don't need to understand the repository structure. You need Google Colab (free) and this one file.

That accessibility is the point. The proof is not just for people who can clone a repository and configure a Python environment. It's for anyone.
