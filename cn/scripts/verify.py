#!/usr/bin/env python3
"""
在展示解法之前，先拿测试用例把它跑一遍。

用法
----
    python3 scripts/verify.py 解法文件 --method 方法名 --cases JSON [--unordered] [--timeout 秒]

解法文件
    一个 Python 文件，里面要么有带该方法的 `Solution` 类，要么有同名的顶层函数。

--cases
    一个 JSON 列表，每项是一个对象：
        {"args": [...], "expect": ...}                      比较返回值
        {"args": [...], "expect": ..., "inplace": 0}        调用后比较 args[0]
                                                            （用于原地修改输入的题）
    `args` 是参数列表，会被展开后传入。

--unordered
    比较列表时忽略顺序（嵌套列表内部也忽略）。
    用于子集、字母异位词分组这类任意顺序都算对的题。

全部用例通过时退出码为 0，否则为 1。

示例
----
    python3 scripts/verify.py sol.py --method minPathSum \\
        --cases '[{"args": [[[1,3,1],[1,5,1],[4,2,1]]], "expect": 7},
                  {"args": [[[1,2,3],[4,5,6]]], "expect": 12}]'
"""

import argparse
import copy
import importlib.util
import json
import sys
import traceback
from pathlib import Path


def load_callable(path: str, method: str):
    """导入文件，返回待测函数。"""
    spec = importlib.util.spec_from_file_location("candidate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "Solution"):
        instance = module.Solution()
        if hasattr(instance, method):
            return getattr(instance, method)
    if hasattr(module, method):
        return getattr(module, method)

    available = [n for n in dir(module) if not n.startswith("_")]
    raise AttributeError(
        f"找不到 '{method}'。顶层可用名称：{available}"
    )


def canonical(value):
    """把嵌套列表排序，使无序比较成立。"""
    if isinstance(value, list):
        inner = [canonical(v) for v in value]
        try:
            return sorted(inner, key=repr)
        except TypeError:
            return inner
    return value


def equal(actual, expected, unordered: bool) -> bool:
    if unordered:
        return canonical(actual) == canonical(expected)
    return actual == expected


def run_one(fn, case, unordered, timeout):
    """返回 (是否通过, 实际值, 错误信息)。"""
    args = copy.deepcopy(case["args"])
    expected = case["expect"]
    inplace_index = case.get("inplace")

    try:
        if timeout:
            import signal

            def on_alarm(signum, frame):
                raise TimeoutError(f"超过 {timeout} 秒")

            signal.signal(signal.SIGALRM, on_alarm)
            signal.alarm(int(timeout))

        returned = fn(*args)

        if timeout:
            signal.alarm(0)
    except Exception:
        if timeout:
            try:
                signal.alarm(0)
            except Exception:
                pass
        return False, None, traceback.format_exc(limit=3).strip()

    actual = args[inplace_index] if inplace_index is not None else returned
    return equal(actual, expected, unordered), actual, None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("solution", help="待测的 Python 文件路径")
    parser.add_argument("--method", required=True, help="要调用的方法名或函数名")
    parser.add_argument("--cases", required=True, help="测试用例的 JSON 列表")
    parser.add_argument("--unordered", action="store_true",
                        help="比较列表时忽略顺序")
    parser.add_argument("--timeout", type=float, default=5,
                        help="单个用例的超时秒数（0 表示不限）")
    args = parser.parse_args()

    if not Path(args.solution).exists():
        print(f"文件不存在：{args.solution}")
        sys.exit(1)

    try:
        cases = json.loads(args.cases)
    except json.JSONDecodeError as e:
        print(f"--cases 的 JSON 格式有误：{e}")
        sys.exit(1)

    try:
        fn = load_callable(args.solution, args.method)
    except Exception as e:
        print(f"加载失败：{e}")
        sys.exit(1)

    passed = 0
    failures = []

    for i, case in enumerate(cases):
        ok, actual, error = run_one(fn, case, args.unordered, args.timeout)
        if ok:
            passed += 1
        else:
            failures.append((i, case, actual, error))

    total = len(cases)
    print(f"{passed}/{total} 通过")

    for i, case, actual, error in failures:
        print(f"\n--- 用例 {i} 失败 ---")
        print(f"  参数    ：{json.dumps(case['args'], ensure_ascii=False)}")
        print(f"  期望    ：{json.dumps(case['expect'], ensure_ascii=False)}")
        if error:
            print(f"  抛出异常：\n{error}")
        else:
            print(f"  实际    ：{json.dumps(actual, default=str, ensure_ascii=False)}")

    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
