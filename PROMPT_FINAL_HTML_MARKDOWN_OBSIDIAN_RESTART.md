# Final HTML + Markdown Obsidian Restart Prompt

You are working on the Faith Through Physics site consolidation.

## Root Folder

`E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files`

## Base/Keeper Folder

`E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\faiththruphysics-site`

## Comparison Folders

- `E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\faiththruphysics-site-v2`
- `E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\faiththruphysics-site-v2-fresh`
- `E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\faiththruphysics-site_backup_20260604_204547`

## First Read These Files

- `E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\SYNTHESIS_COORDINATION_PLAN.md`
- `E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\faiththruphysics-site\_synthesis-review\FINAL_SYNTHESIS_PLAN.md`
- `E:\exports\FaithThroughPhysics_D_Drive_Consolidation\files\faiththruphysics-site\_synthesis-review\CANONICAL_SITE_DATA_STATUS.md`

## Goal

Finish preparing the canonical HTML and Markdown set for eventual Obsidian restart/import.

Do not start over. Use the existing synthesis reports.

## Current Known State

- 5,904 unique HTML identities were found.
- 806 HTML identities have real version differences.
- 558 best-candidate HTML recommendations exist.
- 248 HTML identities still need human review.
- Markdown coverage is about 92.5%.
- 420 HTML article identities still need Markdown.
- The key missing-Markdown list is:
  `faiththruphysics-site\_synthesis-review\conversion-coverage\HTML_MISSING_MARKDOWN.csv`

## Main Tasks

1. Treat `faiththruphysics-site` as the keeper/base folder.
2. Use the existing HTML reports to understand the best available HTML versions:
   - `_synthesis-review\identity-map\MASTER_HTML_IDENTITY_MAP_DEDUPED.csv`
   - `_synthesis-review\best-candidates\BEST_CANDIDATES.csv`
   - `_synthesis-review\human-review\HUMAN_REVIEW_REQUIRED.csv`
   - `_synthesis-review\staged-best-html\STAGING_CANDIDATES_MANIFEST.csv`
3. Do not overwrite active site files yet.
4. Build or update a staging folder containing the best selected HTML files:
   - `_synthesis-review\staged-best-html\approved\`
5. Preserve traceability. Every staged HTML file must have a manifest row showing:
   - identity
   - selected source folder
   - selected source relative path
   - intended keeper path
   - SHA-256
   - reason selected
   - whether it came from base or a comparison folder
6. For the 248 human-review HTML identities, do not guess blindly. If the winner is uncertain, leave it in human review with a short reason.
7. Next, handle Markdown coverage using:
   - `_synthesis-review\conversion-coverage\HTML_MISSING_MARKDOWN.csv`
   - `_synthesis-review\conversion-coverage\HTML_TO_MARKDOWN_COVERAGE.csv`
   - `_synthesis-review\conversion-coverage\MARKDOWN_INVENTORY.csv`
8. The final Markdown question is:
   Which HTML article identities still do not have Markdown, and can we convert them now from the best selected HTML?
9. For missing Markdown, convert from the best available HTML candidate, not from an arbitrary duplicate.
10. Preserve article content, headings, links, images, metadata/title, and meaningful structure.
11. Strip website chrome/nav/footer if it is not article content.
12. Put converted Markdown into a staging folder first:
    - `_synthesis-review\staged-markdown-from-html\`
13. Create a conversion manifest:
    - `_synthesis-review\staged-markdown-from-html\HTML_TO_MARKDOWN_CONVERSION_MANIFEST.csv`

## Required Final Outputs

- `_synthesis-review\staged-best-html\approved\`
- `_synthesis-review\staged-best-html\APPROVED_BEST_HTML_MANIFEST.csv`
- `_synthesis-review\staged-markdown-from-html\`
- `_synthesis-review\staged-markdown-from-html\HTML_TO_MARKDOWN_CONVERSION_MANIFEST.csv`
- `_synthesis-review\FINAL_OBSIDIAN_RESTART_PLAN.md`

## Rules

- Do not delete anything.
- Do not overwrite the active keeper folder.
- Do not replace whole folders.
- Work article-by-article.
- Do not trust folder name alone as quality.
- Prefer complete, clean, readable HTML with full article body, proper title, intact media references, and fewer broken/template artifacts.
- If two versions are tied, prefer the base folder.
- If a comparison folder has a clearly better article, it can win.
- Keep all uncertain cases in a review file.

## Final Summary Required

At the end, summarize:

- how many HTML identities were staged as approved best versions
- how many still require human review
- how many missing Markdown files were converted
- how many HTML identities still lack Markdown
- where the staged Obsidian-ready Markdown lives
- what must be manually reviewed before final import

## Key Instruction

Do not ask broadly to "organize the site." Finish the staged canonical HTML plus missing Markdown conversion using the reports already produced.
