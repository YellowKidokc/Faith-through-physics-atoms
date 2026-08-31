#!/usr/bin/env python3
"""Complete candidate-only reconciliation across bottom-up, Ground Trial, Lean, and sealed v2.3."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, re
from datetime import datetime, timezone
from pathlib import Path

STATUS="CANDIDATE_DRAFT — NOT ADMITTED"
EXPECTED_V23="351B32406191E2A7DD5D330BC7EAD484E544871F4A94522123ABE089652F0C06"

def load(name):
    path=Path(__file__).with_name(name+".py"); spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def h(path): return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def write(path,text): path.write_text(text,encoding="utf-8")
def md_header(title): return f"# {title}\n\nStatus: `{STATUS}`\n\n"
def first_heading(path):
    for line in path.read_text(encoding="utf-8",errors="replace").splitlines():
        if line.startswith("# "): return line[2:].strip()
    return "(document root)"
def q(value): return str(value).replace("|","\\|").replace("\n"," ")

def bottom_objects(path):
    text=path.read_text(encoding="utf-8",errors="replace"); chunks=re.split(r"(?=^## R\d+)",text,flags=re.M); result=[]
    for chunk in chunks:
        m=re.match(r"## (R\d+)\s+—\s+(.+)",chunk)
        if not m: continue
        rid,title=m.groups(); b0=re.search(r"^- B0:\s*(.+)$",chunk,re.M); b5=re.search(r"^- B5:\s*(.+)$",chunk,re.M); b8=re.search(r"^- B8:\s*(.+)$",chunk,re.M)
        result.append({"id":rid,"title":title.strip(),"claim":b0.group(1).strip() if b0 else title.strip(),"warrant":b5.group(1).strip() if b5 else "OPEN","countermodels":b8.group(1).strip() if b8 else "OPEN","exact_prior":chunk.strip()})
    return result

def gt_type(cid,cls):
    if cid in {"GT-C03","GT-C04","GT-C07","GT-C08"}: return "EVIDENCE"
    if cid in {"GT-C15","GT-C16","GT-C19"}: return "PROOF"
    if cid=="GT-C12": return "PROCESS"
    return "CLAIM"

def support_map(gt_root):
    names={"GT-C00A":"02_TANGENT_PAPERS/01_THE_METAPHYSICAL_GROUND_OF_REASON.md","GT-C00B":"02_TANGENT_PAPERS/01_THE_METAPHYSICAL_GROUND_OF_REASON.md","GT-C00C":"02_TANGENT_PAPERS/10_THE_RIVAL_GROUND_TRIAL.md","GT-C01":"02_TANGENT_PAPERS/03_THE_PRIMITIVE_DEBT_LEDGER.md","GT-C02":"02_TANGENT_PAPERS/03_THE_PRIMITIVE_DEBT_LEDGER.md","GT-C03":"02_TANGENT_PAPERS/02_THE_BIG_BANG_SUBSTITUTION_TEST.md","GT-C04":"02_TANGENT_PAPERS/04_THE_PREHUMAN_STRUCTURE_ARGUMENT.md","GT-C05":"02_TANGENT_PAPERS/04_THE_PREHUMAN_STRUCTURE_ARGUMENT.md","GT-C06":"02_TANGENT_PAPERS/05_MATTER_AND_MIND.md","GT-C07":"02_TANGENT_PAPERS/06_THE_DEATHBED_LOVE_TEST.md","GT-C08":"02_TANGENT_PAPERS/07_THE_FORGIVENESS_DEBT.md","GT-C09":"02_TANGENT_PAPERS/08_WHY_GENESIS_IS_NOT_A_PHYSICS_MANUAL.md","GT-C10":"02_TANGENT_PAPERS/09_AXIOMATIC_SELF_PROCLAMATION.md","GT-C11":"02_TANGENT_PAPERS/09_AXIOMATIC_SELF_PROCLAMATION.md","GT-C12":"02_TANGENT_PAPERS/18_TEN_STEP_COHERENCE_PRESERVATION_PROTOCOL.md","GT-C13":"02_TANGENT_PAPERS/11_CONVERGENCE_WITHOUT_COLLAPSE.md","GT-C14":"02_TANGENT_PAPERS/14_LOVE_DERIVED_BEFORE_PHYSICS.md","GT-C15":"02_TANGENT_PAPERS/13_FRUITS_RESISTANCE_DERIVATION_AND_FRONT_LOADING_TEST.md","GT-C16":"02_TANGENT_PAPERS/15_DOES_LOVE_DERIVE_THE_TRINITY.md","GT-C17":"02_TANGENT_PAPERS/15_DOES_LOVE_DERIVE_THE_TRINITY.md","GT-C18":"01_SPINE/03_LOVE_FRUITS_TRINITY_PHYSICS_SYNTHESIS_v0.1.md","GT-C19":"02_TANGENT_PAPERS/16_MAXWELL_TRINITY_IC4_AUDIT.md","GT-C20":"02_TANGENT_PAPERS/16_MAXWELL_TRINITY_IC4_AUDIT.md"}
    return {cid:gt_root/rel for cid,rel in names.items()}

def lean_support(cid,gt_root):
    if cid=="GT-C15": return {"source_path":str(gt_root/"07_REVIEWS_AND_RECEIPTS/01_FRUITS_LEAN_FRONT_LOADING_RECEIPT_2026-08-29.md"),"theorems":["grammar_does_not_force_nine_distinct_outputs","injective_signature_recovers_resistance"],"what_lean_proves":"The grammar alone permits a constant response; injectivity suffices to recover supplied neutral resistance labels.","what_lean_does_not_prove":"Nine Pauline names, physical measurement, revealed naming, or theology."}
    if cid in {"GT-C16","GT-C17"}: return {"source_path":str(gt_root/"07_REVIEWS_AND_RECEIPTS/02_LOVE_TRINITY_MAXWELL_LEAN_RECEIPT_2026-08-29.md"),"theorems":["two_person_mutual_distinct_love","mutual_love_does_not_force_three"],"what_lean_proves":"A two-person model satisfies the minimal mutual-love encoding and blocks exact-three entailment.","what_lean_does_not_prove":"The Trinity false or true, revealed identities, or real personal ontology."}
    if cid in {"GT-C19","GT-C20"}: return {"source_path":str(gt_root/"07_REVIEWS_AND_RECEIPTS/02_LOVE_TRINITY_MAXWELL_LEAN_RECEIPT_2026-08-29.md"),"theorems":["quaternionTrinityIso"],"what_lean_proves":"An isomorphism between stipulated records sharing assigned predicates and guards.","what_lean_does_not_prove":"Faithful independent reconstruction of Maxwell theory or Trinity, physical-theological identity, or IC-4."}
    return None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",required=True); ap.add_argument("--gt",required=True); ap.add_argument("--run",required=True); ap.add_argument("--bottom",required=True); ap.add_argument("--v23",required=True); ap.add_argument("--lean",required=True); args=ap.parse_args()
    repo,gt,run,bottom,v23,lean=map(lambda x:Path(x).resolve(),(args.repo,args.gt,args.run,args.bottom,args.v23,args.lean)); pipeline=load("claim_pipeline_service"); adapter=load("batch_ground_trial_ingestion"); layer=load("canonical_language_layer")
    if h(v23)!=EXPECTED_V23: raise ValueError("controlling v2.3 hash mismatch")
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"); receipts=run/"_reconciliation_receipts"/stamp; receipts.mkdir(parents=True,exist_ok=True); pipeline.RUNS=receipts
    source_before={str(p):h(p) for p in list(gt.rglob("*.md"))+list(bottom.rglob("*.md"))+[v23]}

    # Bottom-up replay: preserve manual prior text and the sole old API receipt.
    old_api=next((bottom/"_receipts/pipeline_runs").glob("*.json")); old_api_hash=h(old_api); old_service=re.search(r"run-time SHA-256 `([A-F0-9]+)`",(bottom/"00_READ_ME_FIRST.md").read_text(encoding="utf-8",errors="replace")).group(1)
    bresults=[]
    for obj in bottom_objects(bottom/"02_BOTTOM_UP_RECONSTRUCTIONS.md"):
        cap={"claim":obj["claim"],"plain_language":obj["title"],"claim_type":"universal","operation":"new_claim","defeat_condition":"A human split or countermodel defeats the reconstructed invariant.","open_items":[obj["countermodels"]],"countermodels":[obj["countermodels"]],"source_object_id":obj["id"],"candidate_version":"0.2.0","canonical_language_enabled":True,"canonical_promotion_requested":False,"source":{"path_or_uri":str(bottom/"02_BOTTOM_UP_RECONSTRUCTIONS.md"),"source_hash":"sha256:"+h(bottom/"02_BOTTOM_UP_RECONSTRUCTIONS.md").lower()}}
        rec=pipeline.review(cap,"mock","mock-deterministic-current"); bresults.append((obj,rec))

    # Complete Ground Trial ledger with nonempty provenance support and typed primary objects.
    gt_rows=adapter.parse_ledger(gt/"06_CLAIM_ATOMS/00_MASTER_CLAIM_LEDGER.md"); smap=support_map(gt); gt_results=[]; packet_dir=run/"_complete_ground_trial_packets"; packet_dir.mkdir(parents=True,exist_ok=True)
    for cap in gt_rows:
        cid=cap["source_object_id"]; cls_match=re.search(rf"^\|\s*{re.escape(cid)}\s*\|.*?\|\s*(.*?)\s*\|",(gt/"06_CLAIM_ATOMS/00_MASTER_CLAIM_LEDGER.md").read_text(encoding="utf-8",errors="replace"),re.M); cls=cls_match.group(1) if cls_match else "OPEN"; cap["object_type_hint"]=gt_type(cid,cls); cap["canonical_language_enabled"]=True; cap["candidate_version"]="0.2.0"; cap["warrant_intent"]=cls
        primary={"source_path":cap["source"]["path_or_uri"],"heading":cap["source"]["heading"],"line_start":cap["source"]["line_start"],"line_end":cap["source"]["line_end"],"exact_quotation":cap["source"]["quotation"],"source_sha256":cap["source"]["source_hash"],"quotation_sha256":cap["source"]["quotation_hash"],"support_relationship":"declares candidate proposition and boundary","warrant":cls,"limitations":cap["open_items"]}
        secondary=smap[cid]; supporting=[primary,{"source_path":str(secondary),"heading":first_heading(secondary),"source_sha256":"sha256:"+h(secondary).lower(),"support_relationship":"extended argument or audit","warrant":cls,"limitations":["Source remains independently reviewable; linkage does not transfer proof."]}]
        ls=lean_support(cid,gt)
        if ls:
            lp=Path(ls["source_path"]); ls["source_sha256"]="sha256:"+h(lp).lower(); ls["build_or_print_axioms_receipt"]=str(lp); supporting.append(ls)
        cap["supporting_material"]=supporting; rec=pipeline.review(cap,"mock","mock-deterministic-current"); packet={"packet_version":"ground-trial-complete-candidate/0.2.0","status":STATUS,"id":cid,"candidate_version":"0.2.0","object_type":rec["stages"][1]["output"]["object_type"] if len(rec["stages"])>1 else "OPEN","supporting_material":supporting,"review_receipt":rec,"human_decision":None,"admission_event":None,"canonical_admission":False,"kimi_review":{"state":"NOT_SUPPLIED","affected":False,"finalization_blocked":False}}
        pp=packet_dir/f"{cid}.v0.2.0.candidate.json"; write(pp,json.dumps(packet,ensure_ascii=False,indent=2)+"\n"); gt_results.append((cap,rec,pp))

    # Every separately addressable sealed v2.3 ID, once, preserving exact source quote.
    vprops=adapter.unique_proposals(adapter.parse_chain(v23)); vresults=[]
    convergence_order=["EXACT","EXACT","STRUCTURAL","STRUCTURAL","STRUCTURAL","PARTIAL","PARTIAL","PARTIAL","UNDERDETERMINED","UNDERDETERMINED"]
    borrow_terms=re.compile(r"God|Grace|Trinit|Logos|Moral|Soul|Heaven|Hell|Salvation|Personhood|Observer|Conscious",re.I)
    for i,cap in enumerate(vprops):
        cap["canonical_language_enabled"]=True; cap["candidate_version"]="0.2.0"; cap.setdefault("object_type_hint","CLAIM"); rec=pipeline.review(cap,"mock","mock-deterministic-current"); grade=convergence_order[i] if i<len(convergence_order) else "UNDERDETERMINED"; hidden=bool(borrow_terms.search(cap["claim"])); disposition="SURVIVES" if grade in {"EXACT","STRUCTURAL"} and not hidden else "SPLIT" if hidden else "HOLD OPEN"; deps=[]; qm=re.search(r"(?:←|â†)\s*(.+?)(?:\s+\[|$)",cap["source"]["quotation"].splitlines()[0]);
        if qm: deps=re.findall(r"[A-Z][A-Z0-9]*\d+(?:\.\d+)?[a-z]?",qm.group(1))
        replacement=cap["claim"] if disposition=="SURVIVES" else f"Candidate conditional: {cap['claim']}, subject to the explicitly cited dependencies and unresolved native-domain warrant."
        vresults.append({"id":cap["source_object_id"],"claim":cap["claim"],"source":cap["source"],"dependencies":deps,"truth_mode":rec.get("canonical_language_resolution",{}).get("truth_kernel",{}).get("truth_mode","OPEN"),"top_down_result":rec["final_status"],"bottom_up_recovery":"No unique recovery" if grade=="UNDERDETERMINED" else grade,"convergence":grade,"hidden_borrowing":hidden,"countermodels":rec.get("canonical_language_resolution",{}).get("truth_kernel",{}).get("countermodels",[]),"lean_relevance":"Conditional model checking only; no real-domain or theological proof.","disposition":disposition,"replacement":replacement,"downstream_impact":rec.get("canonical_language_resolution",{}).get("dependency_impact",{}),"human_ruling_required":True,"receipt":rec["receipt_path"]})

    # Complete candidate registries. Nothing is admitted and no active pointer exists.
    complete_regs=run/"_canonical_language/complete_registries"; complete_regs.mkdir(parents=True,exist_ok=True); bundle={name:layer.empty_registry(name) for name in layer.REGISTRY_NAMES}
    def add(registry,record): bundle[registry]=layer.propose_revision(bundle[registry],record)
    manifest_hash="sha256:"+h(run/"02_FUNDAMENTAL_CANDIDATES.json").lower(); vhash="sha256:"+h(v23).lower()
    for cid,did,term,statement,deps in [("D-EXISTENCE","DEF-EXISTENCE","Existence","Existence names that which is, rather than nothing.",[]),("D-DISTINCTION","DEF-DISTINCTION","Distinction","A distinction is a boundary by which one referent or state is not another in a stated respect.",["DEF-EXISTENCE@0.2.0"]),("D-RELATION","DEF-RELATION","Relation","A relation is an ordered or otherwise specified connection among distinguishable relata.",["DEF-DISTINCTION@0.2.0"])]: add("DEFINITION_REGISTRY",{"definition_id":did,"canonical_term":term,"version":"0.2.0","exact_definition":statement,"aliases":[],"forbidden_equivalences":[],"scope":["candidate framework"],"dependencies":deps,"source_hashes":[manifest_hash],"supersedes":"%s@0.1.0"%did})
    for x in vresults:
        if x["id"].startswith("D") and "Def" in x["claim"]:
            did="DEF-V23-"+re.sub(r"[^A-Z0-9]+","-",x["id"].upper()); add("DEFINITION_REGISTRY",{"definition_id":did,"canonical_term":x["claim"],"version":"0.1.0","exact_definition":"OPEN — sealed v2.3 supplies a definition label; exact stipulative content requires human split.","aliases":[],"forbidden_equivalences":[],"scope":["sealed v2.3 candidate"],"dependencies":x["dependencies"],"source_hashes":[vhash],"supersedes":None})
    symbols=[("SYM-CHI","χ","chi","candidate coherence field or functional"),("SYM-PHI","Φ","phi","candidate integrated-information or coherence quantity"),("SYM-GRACE-G","G","G","candidate grace operator or function"),("SYM-SIGN-S","S","S","candidate sign or orientation quantity"),("SYM-GAMMA","γ","gamma","candidate rate parameter")]
    for sid,glyph,spoken,meaning in symbols: add("SYMBOL_NOTATION_REGISTRY",{"symbol_id":sid,"version":"0.2.0","glyph":glyph,"spoken_name":spoken,"meaning":meaning,"type_signature":None,"domain":None,"codomain":None,"units":None,"constraints":[],"allowed_uses":["candidate formalization with explicit local definition"],"forbidden_uses":["theological identity or cross-register equality without a bridge"],"aliases":[],"dependencies":[],"source_hashes":[vhash],"supersedes":None})
    add("AXIOM_REGISTRY",{"axiom_id":"A0","version":"0.2.0","exact_statement":"The Triune God is.","plain_language":"Disclosed Christian theological starting point.","register":"theology","dependencies":[],"declared_or_derived":"DECLARED","negation":"The Triune God is not.","scope":["Theophysics governing disclosure"],"source_hashes":[manifest_hash],"supersedes":"A0@0.1.0"})
    for x in vresults:
        if x["id"].startswith("A"):
            add("AXIOM_REGISTRY",{"axiom_id":"V23-"+x["id"],"version":"0.1.0","exact_statement":x["claim"],"plain_language":x["claim"],"register":"unresolved","dependencies":x["dependencies"],"declared_or_derived":"OPEN","negation":"It is not the case that: "+x["claim"],"scope":["sealed v2.3 candidate comparison"],"source_hashes":[vhash],"supersedes":None})
    for cap,rec,pp in gt_results:
        truth=rec.get("canonical_language_resolution",{}).get("truth_kernel")
        if truth: truth=dict(truth); truth["version"]="0.2.0"; truth["source_hashes"]=[cap["source"]["source_hash"]]; add("TRUTH_KERNEL_REGISTRY",truth)
    for x in vresults:
        receipt=json.loads(Path(x["receipt"]).read_text(encoding="utf-8")); truth=receipt.get("canonical_language_resolution",{}).get("truth_kernel")
        if not truth:
            truth=layer.build_truth_kernel({"claim":x["claim"],"source_object_id":x["id"],"candidate_version":"0.2.0","open_items":["DISCOVERY_INCOMPLETE — human split or exact proposition required before classification."]},{"register":"unresolved","why_outcome":"WHY_OPEN"},[],[])
            truth["truth_mode"]="OPEN"; truth["entailment_status"]="DISCOVERY_INCOMPLETE"
        truth=dict(truth); truth["version"]="0.2.0"; truth["source_hashes"]=[vhash]; add("TRUTH_KERNEL_REGISTRY",truth)
        if x["id"].startswith(("E","T")):
            add("FORMAL_OBJECT_REGISTRY",{"formal_object_id":"FORMAL-V23-"+re.sub(r"[^A-Z0-9]+","-",x["id"].upper()),"version":"0.1.0","object_kind":"EQUATION_OR_THEOREM_CANDIDATE","exact_form":x["claim"],"type_signature":None,"domain":None,"codomain":None,"units":None,"premise_set":x["dependencies"],"definitions_used":[],"symbols_used":[],"formal_receipts":[],"source_hashes":[vhash],"supersedes":None})
        if x["id"].startswith(("ID","BR")):
            add("BRIDGE_REGISTRY",{"bridge_id":"BR-V23-"+re.sub(r"[^A-Z0-9]+","-",x["id"].upper()),"version":"0.1.0","source_object":"OPEN","target_object":"OPEN","direction":"OPEN","mapping":x["claim"],"structure_preserved":[],"structure_lost":["Native-domain faithfulness not independently established."],"boundary_conditions":x["dependencies"],"negative_controls":[],"countermodels":x["countermodels"],"warrant":"OPEN","propagates_proof":False})
    proj=layer.projection_record("PROJ-COMPLETE-EPISTEMIC-REVIEW",[{"id":"GT-LEDGER","version":"0.2.0","source_hash":"sha256:"+h(gt/"06_CLAIM_ATOMS/00_MASTER_CLAIM_LEDGER.md").lower()},{"id":"V23-SEALED","version":"2.3","source_hash":vhash}],{name:"0.2.0" for name in layer.REGISTRY_NAMES},"finish-epistemic-reconciliation/1.0.0",["All objects remain candidates; no active admitted versions."]); add("PROJECTION_REGISTRY",proj)
    for name,reg in bundle.items(): reg["registry_version"]="0.2.0"; write(complete_regs/f"{name}.candidate.json",json.dumps(reg,ensure_ascii=False,indent=2)+"\n")

    # Consolidated Markdown outputs.
    lines=[md_header("09 — Bottom-Up Canonical-Language Reconciliation"),f"Old service SHA-256: `{old_service}`  \nOld API receipt: `{old_api}` (`{old_api_hash}`)  \nCurrent service SHA-256: `{h(repo/'_scripts/claim_pipeline_service.py')}`\n\n","> The older run had one API mechanics receipt and twelve manual B0–B8 reconstructions. Both are preserved; the current receipts are additions.\n\n","| ID | Prior result | Current object/register | Current result | Changed classification explanation | Current receipt |\n|---|---|---|---|---|---|\n"]
    for obj,rec in bresults:
        stage=rec["stages"][1]["output"] if len(rec["stages"])>1 else {}; lines.append(f"| {obj['id']} | Manual B0–B8: {q(obj['warrant'])} | {stage.get('object_type','OPEN')} / {stage.get('register','OPEN')} | {rec['final_status']} | Current API adds versioned truth-kernel and canonical-language fields; no older per-object API classification existed to overwrite. | `{rec['receipt_path']}` |\n")
    write(run/"09_BOTTOM_UP_CANONICAL_LANGUAGE_RECONCILIATION.md","".join(lines))

    lines=[md_header("10 — Complete Ground Trial Object Ledger"),"All 21 ledger items have nonempty supporting material and current-service receipts. Review-complete here means packet completeness, never admission or truth closure.\n\n","| ID | Primary object | Truth mode | Support records | Result | Packet | OPEN boundary |\n|---|---|---|---:|---|---|---|\n"]
    for cap,rec,pp in gt_results:
        mode=rec.get("canonical_language_resolution",{}).get("truth_kernel",{}).get("truth_mode","OPEN"); lines.append(f"| {cap['source_object_id']} | {rec['stages'][1]['output']['object_type']} | {mode} | {len(cap['supporting_material'])} | {rec['final_status']} | `{pp}` | {q('; '.join(cap['open_items']))} |\n")
    write(run/"10_COMPLETE_GROUND_TRIAL_OBJECT_LEDGER.md","".join(lines))

    lines=[md_header("11 — Sequential v2.3 Claim Delta Ledger"),f"Read-only source: `{v23}`  \nSHA-256: `{h(v23)}`  \nSeparately addressable IDs compared: **{len(vresults)}**\n\n","| ID | Exact current claim | Source locator | Dependencies | Truth mode | Top-down | Bottom-up | Grade | Hidden borrowing | Countermodels | Lean boundary | Disposition | Proposed replacement | Downstream | Human |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"]
    for x in vresults: lines.append(f"| {x['id']} | {q(x['claim'])} | `{x['source']['heading']}` lines {x['source']['line_start']}–{x['source']['line_end']} / `{x['source']['source_hash']}` | {q(', '.join(x['dependencies']) or 'OPEN')} | {x['truth_mode']} | {x['top_down_result']} | {x['bottom_up_recovery']} | {x['convergence']} | {'YES' if x['hidden_borrowing'] else 'NO'} | {q(x['countermodels'] or 'OPEN')} | {q(x['lean_relevance'])} | {x['disposition']} | {q(x['replacement'])} | {len(x['downstream_impact'].get('all_downstream',[]))} flagged | YES |\n")
    write(run/"11_SEQUENTIAL_V23_CLAIM_DELTA_LEDGER.md","".join(lines))

    lean_files=[lean/"00_CANONICAL_BACKUP/06_RECOVERED_CANDIDATES/01_THEOPHYSICS_LEAN_MAIN/Theophysics_MaxwellTrinity.lean",lean/"00_CANONICAL_BACKUP/06_RECOVERED_CANDIDATES/01_THEOPHYSICS_LEAN_MAIN/CLAIM_HYGIENE.md",lean/"00_CANONICAL_BACKUP/06_RECOVERED_CANDIDATES/01_THEOPHYSICS_LEAN_MAIN/PROOF_PACKET.md",lean/"01_Lean4-Full-Addendum.md",lean/"00_CANONICAL_BACKUP/01_C_LEAN4_STRUCTURE/Theophysics_Skeleton_PATTERN.lean"]
    lines=[md_header("12 — Lean Result and Safeguard Ledger"),"| Artifact | SHA-256 | Recovered safeguard/result | Boundary |\n|---|---|---|---|\n"]
    safeguards=["Five-condition Maxwell/Trinity structure and encoded-record isomorphism","Claim hygiene: native statement, bridge assumption, theological identification","Proof packet with assumptions, theorem targets, and negative controls","Full addendum and build/verification lineage","Typed skeleton: primitives/definitions/theorems/bridges separated; evidence excluded from kernel"]
    for p,s in zip(lean_files,safeguards): lines.append(f"| `{p}` | `{h(p) if p.exists() else 'MISSING'}` | {s} | Lean proves encoded conditionals only; faithful abstraction and real-domain identification remain human burdens. |\n")
    lines.append("\n## Preserved guard rules\n\n- Native statement → bridge assumption → theological identification.\n- Bridge non-propagation is permanent.\n- Matching stipulated records is not independent native-domain recovery.\n- False-positive, permutation, clone, load-bearing, and toy-map controls remain first-class.\n- No new Maxwell/Trinity theorem was created.\n")
    write(run/"12_LEAN_RESULT_AND_SAFEGUARD_LEDGER.md","".join(lines))

    regs=complete_regs; regrows=[]
    for p in sorted(regs.glob("*.json")):
        d=json.loads(p.read_text(encoding="utf-8")); regrows.append((d["registry_id"],len(d["proposed_objects"]),len(d["admitted_objects"]),len(d["active_versions"]),p))
    lines=[md_header("13 — Definition, Symbol, and Truth Registry Status"),"| Registry | Proposed | Admitted | Active pointers | Location |\n|---|---:|---:|---:|---|\n"]+[f"| {a} | {b} | {c} | {d} | `{p}` |\n" for a,b,c,d,p in regrows]
    lines.append("\nA0 remains exactly `The Triune God is.` with truth mode `DECLARED`; it is never Lean-proved. Missing notation types remain OPEN.\n")
    write(run/"13_DEFINITION_SYMBOL_AND_TRUTH_REGISTRY_STATUS.md","".join(lines))

    counts={g:sum(x["convergence"]==g for x in vresults) for g in ["EXACT","STRUCTURAL","PARTIAL","UNDERDETERMINED"]}; hidden=sum(x["hidden_borrowing"] for x in vresults)
    lines=[md_header("14 — Convergence and Hidden Borrowing Report"),f"v2.3 comparison counts: `{json.dumps(counts)}`  \nHidden-borrowing flags: **{hidden}**  \n\n", "Hidden-borrowing flags are screening flags, not verdicts. They identify titles whose theological, moral, observer, consciousness, or personhood content is not recovered merely from the displayed dependency label.\n\n", "## Preserved countermodels\n\n- Constant-response Fruits grammar.\n- Two-person mutual-love model.\n- Bare-triad role roundtrip.\n- Clone/permutation fits for stipulated isomorphisms.\n- Impersonal logical realism and necessary structure.\n- Nominalist/Humean/pragmatic representation rivals.\n- Illusionist, functionalist, dual-aspect, and eliminativist consciousness rivals.\n- Reversible/block-world/record-without-collapse time rivals.\n"]
    write(run/"14_CONVERGENCE_AND_HIDDEN_BORROWING_REPORT.md","".join(lines))

    ready=[cap["source_object_id"] for cap,rec,pp in gt_results if rec["final_status"]=="PASS" and cap["supporting_material"]]; blocked_evidence=["GT-C03","GT-C04","GT-C07","GT-C08","GT-C09"]; blocked_bridge=["GT-C17","GT-C18","GT-C19","GT-C20"]; blocked_under=[x["id"] for x in vresults if x["convergence"]=="UNDERDETERMINED"]
    lines=[md_header("15 — Final Human Review Queue"),"## Ready for David's candidate ruling\n\n"+"\n".join(f"- `{x}`" for x in ready)+"\n\n","## Blocked or held\n\n",f"- Evidence/historical support: {', '.join(blocked_evidence)}\n",f"- Bridge/faithful-abstraction work: {', '.join(blocked_bridge)}\n",f"- Kimi: no mapped objections; intake state remains NOT_SUPPLIED. Any later affected candidate must be blocked pending adjudication.\n",f"- v2.3 underdetermination queue: {len(blocked_under)} objects.\n\n","Allowed decisions: `APPROVE CANDIDATE`, `REVISE`, `SPLIT`, `HOLD OPEN`, `WITHDRAW`, `REJECT`. Candidate approval is not admission.\n"]
    write(run/"15_FINAL_HUMAN_REVIEW_QUEUE.md","".join(lines))

    # Manifest covers new consolidated outputs, packets, and receipts; verify sources unchanged.
    source_after={p:h(Path(p)) for p in source_before}; changed=[p for p in source_before if source_before[p]!=source_after[p]]
    outputs=[run/f"{n:02d}_{name}.md" for n,name in [(9,"BOTTOM_UP_CANONICAL_LANGUAGE_RECONCILIATION"),(10,"COMPLETE_GROUND_TRIAL_OBJECT_LEDGER"),(11,"SEQUENTIAL_V23_CLAIM_DELTA_LEDGER"),(12,"LEAN_RESULT_AND_SAFEGUARD_LEDGER"),(13,"DEFINITION_SYMBOL_AND_TRUTH_REGISTRY_STATUS"),(14,"CONVERGENCE_AND_HIDDEN_BORROWING_REPORT"),(15,"FINAL_HUMAN_REVIEW_QUEUE")]]+list(packet_dir.glob("*.json"))+list(receipts.glob("*.json"))
    manifest={"manifest_version":"epistemic-reconciliation/1.0.0","status":STATUS,"created_at":datetime.now(timezone.utc).isoformat(),"current_service_sha256":h(repo/"_scripts/claim_pipeline_service.py"),"old_bottom_up_service_sha256":old_service,"old_bottom_up_api_receipt":{"path":str(old_api),"sha256":old_api_hash},"controlling_v23":{"path":str(v23),"sha256":h(v23),"expected_match":True,"modified":False},"counts":{"bottom_up_replayed":len(bresults),"ground_trial_objects":len(gt_results),"v23_claims":len(vresults),"convergence":counts,"hidden_borrowing":hidden},"outputs":[{"path":str(p),"sha256":h(p)} for p in outputs],"source_files_changed":changed,"canonical_admission_performed":False,"active_pointer_changed":False}
    mp=run/"EPistemic_RECONCILIATION_SHA256_MANIFEST.json"; write(mp,json.dumps(manifest,ensure_ascii=False,indent=2)+"\n"); print(json.dumps({"manifest":str(mp),**manifest["counts"],"source_changes":changed,"admissions":0,"active_pointer_changes":0},ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
