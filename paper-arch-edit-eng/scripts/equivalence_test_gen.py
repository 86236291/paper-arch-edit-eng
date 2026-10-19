#!/usr/bin/env python3
"""生成等价性测试骨架（pytest 文件）。
用法: python equivalence_test_gen.py --module-a pkg.a:Model --module-b pkg.b:Model \
        --input 1,3,224,224 --out tests/test_equivalence_generated.py
纪律: 必须在 SGD 与 AdamW 训练后各跑一次；float32 与混合精度各跑一次。
"""
import argparse

TEMPLATE = '''import torch, pytest
from {a} import Model as A
from {b} import Model as B

@pytest.mark.parametrize("dtype,atol", [(torch.float32, 1e-5), (torch.float16, 1e-2)])
@pytest.mark.parametrize("opt", ["sgd", "adamw"])
def test_equivalence(dtype, atol, opt):
    torch.manual_seed(0)
    x = torch.randn({shape}).to(dtype)
    a, b = A().to(dtype), B().to(dtype)
    # TODO: 接入 opt 训练若干步后，再比较 a 与 b 输出
    with torch.no_grad():
        ya, yb = a(x), b(x)
    assert torch.allclose(ya, yb, atol=atol), (ya - yb).abs().max()
'''

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--module-a", required=True)
    p.add_argument("--module-b", required=True)
    p.add_argument("--input", default="1,3,224,224")
    p.add_argument("--out", default="tests/test_equivalence_generated.py")
    a = p.parse_args()
    shape = "(" + ",".join(a.input.split(",")) + ",)"
    code = TEMPLATE.format(a=a.module_a, b=a.module_b, shape=shape)
    open(a.out, "w").write(code)
    print(f"written {a.out}")

if __name__ == "__main__":
    main()