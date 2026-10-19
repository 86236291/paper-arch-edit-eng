#!/usr/bin/env python3
"""扫描 repo，输出候选落点、层注册方式、测试目录、依赖版本。
用法: python repo_scan.py --root . --out audit.json
仅做静态扫描与启发式提示，结论需人工在 repo-audit-table 中确认。
"""
import argparse, json, os, re

def scan(root):
    hits = {"modules": [], "registries": [], "tests": [], "deps": {}}
    for dp, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            if fn.endswith(".py"):
                txt = open(p, errors="ignore").read()
                if re.search(r"class\s+\w+\(nn\.Module\)", txt):
                    hits["modules"].append(p)
                if re.search(r"(registry|REGISTRY|@register)", txt):
                    hits["registries"].append(p)
                if "pytest" in txt or fn.startswith("test_"):
                    hits["tests"].append(p)
            if fn in ("requirements.txt", "pyproject.toml", "environment.yml"):
                hits["deps"][p] = open(p, errors="ignore").read()[:2000]
    return hits

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--out", default="audit.json")
    a = p.parse_args()
    res = scan(a.root)
    json.dump(res, open(a.out, "w"), indent=2)
    print(f"written {a.out}; modules={len(res['modules'])} tests={len(res['tests'])}")

if __name__ == "__main__":
    main()