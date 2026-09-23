import json
from jsonschema import validate
from pathlib import Path


def test_sample_paper_record_validates():
    schema = json.loads(Path("schemas/paper-record-v1.schema.json").read_text())
    sample = json.loads(Path("tests/fixtures/sample_paper_record.json").read_text())
    validate(instance=sample, schema=schema)
