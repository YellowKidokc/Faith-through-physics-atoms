#!/usr/bin/env python3
"""Create candidate-only canonical-language registries from reviewed packets."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


def load_layer():
    path=Path(__file__).with_name("canonical_language_layer.py"); spec=importlib.util.spec_from_file_location("canonical_language_layer",path); module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module); return module


def source_hash(path: Path) -> str:
    return "sha256:"+hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--candidate-run",required=True); parser.add_argument("--manifest",required=True); parser.add_argument("--ground-ledger",required=True); parser.add_argument("--ground-sample",type=int,default=5); args=parser.parse_args()
    layer=load_layer(); root=Path(args.candidate_run).resolve(); manifest_path=Path(args.manifest).resolve(); ledger_path=Path(args.ground_ledger).resolve(); data=json.loads(manifest_path.read_text(encoding="utf-8")); out=root/"_canonical_language"; registries=out/"registries"; receipts=out/"receipts"; registries.mkdir(parents=True,exist_ok=True); receipts.mkdir(parents=True,exist_ok=True)
    bundle={name:layer.empty_registry(name) for name in layer.REGISTRY_NAMES}; manifest_hash=source_hash(manifest_path); ledger_hash=source_hash(ledger_path)
    definitions={"D-EXISTENCE":"DEF-EXISTENCE","D-DISTINCTION":"DEF-DISTINCTION","D-RELATION":"DEF-RELATION"}
    for row in data["candidates"]:
        cid=row["id"]
        if cid in definitions:
            record={"definition_id":definitions[cid],"canonical_term":row["title"].replace(" Definition",""),"version":"0.1.0","exact_definition":row["statement"],"aliases":[],"forbidden_equivalences":[],"scope":["candidate framework usage"],"dependencies":row["depends_on"],"source_hashes":[manifest_hash],"supersedes":None}
            bundle["DEFINITION_REGISTRY"]=layer.propose_revision(bundle["DEFINITION_REGISTRY"],record)
        if cid=="A0":
            record={"axiom_id":"A0","version":"0.1.0","exact_statement":"The Triune God is.","plain_language":row["plain_language"],"register":"theology","dependencies":[],"declared_or_derived":"DECLARED","negation":"The Triune God is not.","scope":["disclosed theological starting point"],"source_hashes":[manifest_hash],"supersedes":None}
            bundle["AXIOM_REGISTRY"]=layer.propose_revision(bundle["AXIOM_REGISTRY"],record)
        packet_path=root/"_candidate_packets"/f"{cid}.candidate.json"; packet=json.loads(packet_path.read_text(encoding="utf-8")); truth=packet.get("review_card",{}).get("canonical_language",{}).get("truth_kernel")
        if truth: bundle["TRUTH_KERNEL_REGISTRY"]=layer.propose_revision(bundle["TRUTH_KERNEL_REGISTRY"],truth)
        if cid=="CM-LOVE-NOT-EXACTLY-THREE":
            formal={"formal_object_id":"FORMAL-CM-LOVE-2P","version":"0.1.0","object_kind":"COUNTERMODEL","exact_form":row["statement"],"type_signature":None,"domain":"declared mutual-love premise set","codomain":"Boolean satisfaction result","units":None,"premise_set":row["depends_on"],"definitions_used":["DEF-RELATION@0.1.0"],"symbols_used":[],"formal_receipts":[],"source_hashes":[manifest_hash],"supersedes":None}
            bundle["FORMAL_OBJECT_REGISTRY"]=layer.propose_revision(bundle["FORMAL_OBJECT_REGISTRY"],formal)
    # Candidate notation record; missing units remain explicit rather than invented.
    symbol={"symbol_id":"SYM-CHI","version":"0.1.0","glyph":"χ","spoken_name":"chi","meaning":"Candidate coherence-field symbol","type_signature":None,"domain":None,"codomain":None,"units":None,"constraints":[],"allowed_uses":["candidate formal models"],"forbidden_uses":["literal identity with God or Logos without an admitted bridge"],"aliases":[],"dependencies":[],"source_hashes":[manifest_hash],"supersedes":None}
    bundle["SYMBOL_NOTATION_REGISTRY"]=layer.propose_revision(bundle["SYMBOL_NOTATION_REGISTRY"],symbol)
    bridge={"bridge_id":"BR-TRINITY-LOVE","version":"0.1.0","source_object":"A0@0.1.0","target_object":"TRUTH-T-TRINITY-LOVE@0.1.0","direction":"source_to_target","mapping":"Candidate theological entailment mapping; not reverse derivation of Trinity from love.","structure_preserved":["eternal personal relation","love not created by the world"],"structure_lost":["full doctrinal identity and historical warrant"],"boundary_conditions":["Christian Trinitarian premises are declared"],"negative_controls":["two-person mutual-love countermodel blocks reverse exact-three inference"],"countermodels":["CM-LOVE-NOT-EXACTLY-THREE"],"warrant":"T_CONDITIONAL","propagates_proof":False}
    bundle["BRIDGE_REGISTRY"]=layer.propose_revision(bundle["BRIDGE_REGISTRY"],bridge)
    projection=layer.projection_record("PROJ-FUNDAMENTAL-REVIEW",[{"id":"A0","version":"0.1.0","source_hash":manifest_hash}],{name:"0.1.0" for name in layer.REGISTRY_NAMES},"canonical-language-layer/1.0.0",["No active admitted registry versions exist."])
    bundle["PROJECTION_REGISTRY"]=layer.propose_revision(bundle["PROJECTION_REGISTRY"],projection)
    # Ground Trial sample truth kernels retain exact ledger statements without admission.
    ground=[]
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| GT-"): continue
        cells=[x.strip() for x in line.strip("|").split("|")]
        if len(cells)<4: continue
        cid,claim,classification,boundary=cells[:4]; capsule={"claim":claim,"source_object_id":cid,"candidate_version":"0.1.0","open_items":[boundary]}; classified={"register":"unresolved","why_outcome":"WHY_OPEN"}; truth=layer.build_truth_kernel(capsule,classified,[],[]); truth["source_hashes"]=[ledger_hash]
        bundle["TRUTH_KERNEL_REGISTRY"]=layer.propose_revision(bundle["TRUTH_KERNEL_REGISTRY"],truth); ground.append(cid)
        if len(ground)>=args.ground_sample: break
    for name,registry in bundle.items(): (registries/f"{name}.candidate.json").write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"run_version":"canonical-language-bootstrap/1.0.0","status":layer.STATUS,"created_at":datetime.now(timezone.utc).isoformat(),"manifest":{"path":str(manifest_path),"sha256":manifest_hash},"ground_ledger":{"path":str(ledger_path),"sha256":ledger_hash,"sample_ids":ground},"registries":{name:{"path":str(registries/f'{name}.candidate.json'),"proposed_count":len(reg["proposed_objects"]),"admitted_count":len(reg["admitted_objects"]),"active_pointer_count":len(reg["active_versions"])} for name,reg in bundle.items()},"canonical_admission_performed":False,"active_version_pointer_changed":False}
    path=receipts/f"BOOTSTRAP_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"; path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({**receipt,"receipt_path":str(path)},ensure_ascii=False,indent=2)); return 0


if __name__=="__main__": raise SystemExit(main())
