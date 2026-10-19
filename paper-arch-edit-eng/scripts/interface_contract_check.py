#!/usr/bin/env python3
"""接口契约校验：用固定输入跑候选落点，比较上下游形状/dtype。
用法: python interface_contract_check.py --module pkg.mod:Class --input 1,3,224,224
输出 JSON：上游输出、目标输出、下游期望、是否匹配。
"""
import argparse, importlib, json, torch

def load(spec):
    mod, _, attr = spec.partition(":")
    return getattr(importlib.import_module(mod), attr)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--module", required=True)
    p.add_argument("--input", default="1,3,224,224")
    a = p.parse_args()
    shape = tuple(int(x) for x in a.input.split(","))
    x = torch.randn(*shape)
    m = load(a.module)()
    with torch.no_grad():
        y = m(x)
    out = {
        "input_shape": list(x.shape), "input_dtype": str(x.dtype),
        "output_shape": list(y.shape), "output_dtype": str(y.dtype),
        "note": "需人工补上下游期望形状后判定是否匹配"
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()