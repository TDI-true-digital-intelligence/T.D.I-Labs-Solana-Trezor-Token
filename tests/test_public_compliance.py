#!/usr/bin/env python3
"""test_public_compliance.py — Solana-Trezor-Token public legal invariants.
MIT LICENSE with legal-person holder; README trademark/AI/privacy/NFA sections;
no stale org links; no secret-shaped strings in public text.
Run: python3 tests/test_public_compliance.py
"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
FAILS, PASSES = [], []
def check(name, cond, detail=""):
    (PASSES if cond else FAILS).append(f"{name}{(' — ' + detail) if detail and not cond else ''}")

lic = (ROOT/"LICENSE").read_text() if (ROOT/"LICENSE").is_file() else ""
check("LICENSE is MIT", "MIT License" in lic and "Permission is hereby granted" in lic)
check("holder is legal person", "Robert Shields Jr. McDougall" in lic)
check("no brand-only holder", "T.D.I Labs + T.D.I Partner" not in lic)

rd = (ROOT/"README.md").read_text()
check("trademark notice", "SatoshiLabs" in rd and "not affiliated" in rd)
check("AI disclosure", "AI assistance" in rd or "AI-assistance" in rd)
check("privacy note", "Nothing is collected" in rd)
check("not-financial-advice", "not financial advice" in rd.lower())
check("no stale org links", "agi-digital-dot" not in rd)

SECRET = re.compile(r"(api[_-]?key|secret|password|mnemonic|seed\s*phrase|private[_-]?key)\s*[:=]\s*[\"\'][A-Za-z0-9_\-/+=.]{12,}", re.I)
for rel in ("README.md", "PROOF.md", "CLAIM-BASIS.md", "VERIFY-RECEIPTS.md", "proof.sh"):
    p = ROOT/rel
    if p.is_file():
        check(f"no secrets in {rel}", not SECRET.search(p.read_text(errors="ignore")))

print(f"PASS {len(PASSES)} / FAIL {len(FAILS)}")
for f in FAILS: print("  FAIL:", f)
sys.exit(1 if FAILS else 0)
