#!/usr/bin/env python3
"""Deterministically validate candidate canonical-language registries and records."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import jsonschema

SCHEMAS={"DEFINITION_REGISTRY":"definition_record_v1.schema.json","SYMBOL_NOTATION_REGISTRY":"symbol_notation_record_v1.schema.json","AXIOM_REGISTRY":"axiom_record_v1.schema.json","TRUTH_KERNEL_REGISTRY":"truth_kernel_record_v1.schema.json","FORMAL_OBJECT_REGISTRY":"formal_object_record_v1.schema.json","BRIDGE_REGISTRY":"bridge_record_v1.schema.json","PROJECTION_REGISTRY":"projection_record_v1.schema.json"}

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--registry-dir",required=True); parser.add_argument("--source",action="append",default=[]); args=parser.parse_args(); root=Path(args.registry_dir).resolve(); schema_root=Path(__file__).resolve().parents[1]/"_schema"; envelope=json.loads((schema_root/"canonical_language_registry_v1.schema.json").read_text(encoding="utf-8")); results=[]
    for registry_id,schema_name in SCHEMAS.items():
        path=root/f"{registry_id}.candidate.json"; value=json.loads(path.read_text(encoding="utf-8")); jsonschema.validate(value,envelope); record_schema=json.loads((schema_root/schema_name).read_text(encoding="utf-8"))
        for record in value["proposed_objects"]: jsonschema.validate(record,record_schema)
        if value["admitted_objects"] or value["active_versions"]: raise ValueError(f"real candidate registry unexpectedly contains admission state: {registry_id}")
        results.append({"registry":registry_id,"proposed":len(value["proposed_objects"]),"admitted":0,"active":0,"status":"PASS"})
    sources=[]
    for raw in args.source:
        path=Path(raw).resolve(); sources.append({"path":str(path),"sha256":"sha256:"+hashlib.sha256(path.read_bytes()).hexdigest()})
    print(json.dumps({"status":"PASS","registries":results,"sources_after_validation":sources,"canonical_admission_performed":False,"active_pointer_changed":False},ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
