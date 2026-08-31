#!/usr/bin/env python3
"""Validate final reconciliation manifest, packet support, and receipt chains."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from pathlib import Path

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def load_service():
    path=Path(__file__).with_name("claim_pipeline_service.py"); spec=importlib.util.spec_from_file_location("claim_pipeline_service",path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--run",required=True); args=ap.parse_args(); root=Path(args.run).resolve(); service=load_service(); manifest=json.loads((root/"EPistemic_RECONCILIATION_SHA256_MANIFEST.json").read_text(encoding="utf-8")); errors=[]
    for item in manifest["outputs"]:
        path=Path(item["path"])
        if not path.is_file() or digest(path)!=item["sha256"]: errors.append(f"output hash mismatch: {path}")
    packets=list((root/"_complete_ground_trial_packets").glob("*.candidate.json"))
    if len(packets)!=23: errors.append(f"expected 23 Ground Trial packets, found {len(packets)}")
    for path in packets:
        packet=json.loads(path.read_text(encoding="utf-8"))
        if not packet.get("supporting_material"): errors.append(f"empty supporting material: {path.name}")
        if packet.get("canonical_admission") is not False or packet.get("admission_event") is not None: errors.append(f"admission-state violation: {path.name}")
        receipt=packet.get("review_receipt",{})
        for stage in receipt.get("stages",[]):
            if stage.get("hash")!=service.sha(stage.get("output")): errors.append(f"stage hash mismatch: {path.name}/{stage.get('name')}")
        if len(receipt.get("stages",[]))==3:
            if receipt["stages"][1]["output"].get("discovery_receipt_hash")!=receipt["stages"][0]["hash"]: errors.append(f"discovery chain mismatch: {path.name}")
            if receipt["stages"][2]["output"].get("classification_receipt_hash")!=receipt["stages"][1]["hash"]: errors.append(f"classification chain mismatch: {path.name}")
    if manifest.get("source_files_changed"): errors.append("manifest reports source changes")
    if manifest.get("canonical_admission_performed") or manifest.get("active_pointer_changed"): errors.append("manifest reports admission or active pointer change")
    result={"status":"PASS" if not errors else "BLOCKED","errors":errors,"ground_trial_packets":len(packets),"packets_with_support":sum(bool(json.loads(p.read_text(encoding='utf-8')).get('supporting_material')) for p in packets),"receipt_chains_checked":len(packets),"source_changes":manifest.get("source_files_changed"),"canonical_admissions":0,"active_pointer_changes":0}; print(json.dumps(result,indent=2)); return 0 if not errors else 2
if __name__=="__main__": raise SystemExit(main())
