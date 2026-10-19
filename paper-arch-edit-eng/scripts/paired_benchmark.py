#!/usr/bin/env python3
"""配对基准：baseline vs 改造 vs 随机基线，输出配对统计与门判定。
用法: python paired_benchmark.py --csv runs.csv --baseline baseline --alpha 2.0
CSV 列: seed, variant, metric
输出 JSON：每变体的均值、配对SE、是否 |Δ|<2SE、是否随机基线追平。
"""
import argparse, csv, json, math
from collections import defaultdict

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--baseline", default="baseline")
    p.add_argument("--random", default="random_matched")
    p.add_argument("--alpha", type=float, default=2.0)
    p.add_argument("--gate_ratio", type=float, default=0.9)
    a = p.parse_args()
    data = defaultdict(dict)
    for r in csv.DictReader(open(a.csv)):
        data[r["variant"]][r["seed"]] = float(r["metric"])
    seeds = sorted(set.intersection(*[set(v) for v in data.values()]))
    base = [data[a.baseline][s] for s in seeds]
    out = {"seeds": len(seeds), "variants": {}}
    for v, vals in data.items():
        if v == a.baseline: continue
        diffs = [vals[s] - data[a.baseline][s] for s in seeds]
        n = len(diffs); mean_d = sum(diffs)/n
        var = sum((d-mean_d)**2 for d in diffs)/(n-1) if n > 1 else 0.0
        se = math.sqrt(var/n) if n > 1 else float("inf")
        out["variants"][v] = {
            "mean_diff": mean_d, "paired_se": se,
            "inconclusive_under_alpha": abs(mean_d) < a.alpha*se,
        }
    # 随机基线门
    if a.random in data:
        d = data.get("design")
        if d:
            ratio = max(data[a.random].values()) / max(d.values())
            out["random_gate"] = {"ratio": ratio,
                                  "downgrade": ratio >= a.gate_ratio}
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()