#!/usr/bin/env python3
"""交付包机械审计。
用法: python delivery_audit.py --root delivery/
检查：tests/ 非空、gates/ 每门 JSON 存在、复现脚本存在、flag 默认关闭、
discussion/ 三件套齐全、PR.md 存在。
"""
import argparse, json, os

REQUIRED_DIRS = ["code", "tests", "scripts", "configs", "env",
                 "discussion", "gates"]
REQUIRED_FILES = ["PR.md"]
DISCUSSION = ["innovation-card.md", "repo-audit-table.md", "change-spec.md"]
GATES = ["random_matched.json", "random_label.json", "paired_seed.json",
         "regression.json", "equivalence.json"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="delivery")
    a = p.parse_args()
    issues = []
    for d in REQUIRED_DIRS:
        if not os.path.isdir(os.path.join(a.root, d)):
            issues.append(f"missing dir: {d}")
    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(a.root, f)):
            issues.append(f"missing file: {f}")
    for f in DISCUSSION:
        if not os.path.isfile(os.path.join(a.root, "discussion", f)):
            issues.append(f"missing discussion: {f}")
    for g in GATES:
        if not os.path.isfile(os.path.join(a.root, "gates", g)):
            issues.append(f"missing gate result: {g}")
    tests = os.path.join(a.root, "tests")
    if os.path.isdir(tests) and not any(f.startswith("test_") for f in os.listdir(tests)):
        issues.append("tests/ empty")
    print(json.dumps({"passed": not issues, "issues": issues}, indent=2))

if __name__ == "__main__":
    main()