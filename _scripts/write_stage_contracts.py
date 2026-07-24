"""Generate the CONTRACT README in every stage folder of every domain.
READMEs are GENERATED - never hand-edit them. Change the contract in
_vocab/stage_contracts*.json and rerun.
Usage: python _scripts/write_stage_contracts.py
"""
import os, json

REPO  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB = os.path.join(REPO, "_vocab")

C = {}
for fn in ("stage_contracts.json", "stage_contracts_technical.json",
           "stage_contracts_public.json"):
    with open(os.path.join(VOCAB, fn), encoding="utf-8") as f:
        C.update(json.load(f)["stages"])

TPL = """# {stage}
> {question}

**Branch:** {branch}  ·  **Glyph:** `{glyph}`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
{nodeTypes}

## Required fields
{required}

## Allowed incoming edges
{edgesIn}

## Allowed outgoing edges
{edgesOut}

## Completion condition
{completion}

## Propagation behavior
{propagation}

## NLP / classifier operations
{nlp}

## Validation rules
{validation}

## Public rendering
{rendering}

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
"""


def bullets(v):
    if not v:
        return "_none_"
    if isinstance(v, list):
        return "\n".join(f"- `{x}`" for x in v)
    return v


def write_all():
    n_dom = n_readme = 0
    for domain in sorted(os.listdir(REPO)):
        droot = os.path.join(REPO, domain)
        if not os.path.isdir(droot) or domain.startswith((".", "_")):
            continue
        n_dom += 1
        for stage in sorted(os.listdir(droot)):
            p = os.path.join(droot, stage)
            if not os.path.isdir(p) or stage not in C:
                continue
            c = C[stage]
            body = TPL.format(
                stage=stage, question=c["question"], branch=c["branch"],
                glyph=c["glyph"],
                nodeTypes=bullets(c["nodeTypes"]),
                required=bullets(c["required"]),
                edgesIn=bullets(c["edgesIn"]),
                edgesOut=bullets(c["edgesOut"]),
                completion=c["completion"], propagation=c["propagation"],
                nlp=c["nlp"], validation=c["validation"],
                rendering=c["rendering"])
            with open(os.path.join(p, "README.md"), "w", encoding="utf-8") as f:
                f.write(body)
            n_readme += 1
    return n_dom, n_readme


if __name__ == "__main__":
    d, r = write_all()
    print(f"wrote {r} contract READMEs across {d} domains")
    missing = [s for s in C if s not in
               {x for dom in os.listdir(REPO)
                if os.path.isdir(os.path.join(REPO, dom))
                and not dom.startswith(("_", "."))
                for x in os.listdir(os.path.join(REPO, dom))}]
    if missing:
        print("stages in contract but not on disk:", missing)
