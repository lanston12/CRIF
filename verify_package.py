from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parent
freeze = json.loads((root / "experiments/evaluation/study_eval_v1.freeze.json").read_text())
for section in ("sources", "configs"):
    for relative, expected in freeze[section].items():
        actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        assert actual == expected, f"Hash mismatch: {relative}"
provenance = (root / "config/plant_provenance.md").read_text(encoding="utf-8")
for relative, expected in re.findall(r"^\| ((?:CRAFT|GNC|HYDRO|INS|LIBRARY)/[^|]+\.m) \| ([a-f0-9]{64}) \|", provenance, re.M):
    actual = hashlib.sha256((root / "external/MSS_pinned" / relative).read_bytes()).hexdigest()
    assert actual == expected, f"MSS mismatch: {relative}"
e4 = root / "logs/mechanisms/evaluation/mechanism_eval_v1/E4_CRIF_2101.mat"
assert hashlib.sha256(e4.read_bytes()).hexdigest() == "c07c3d7826fab7102f9dace7570ad0599901087820b0fa855420286f421eeb9a", "E4-B trace mismatch"
print("PASS: frozen source/config, pinned MSS, and E4-B trace hashes")
