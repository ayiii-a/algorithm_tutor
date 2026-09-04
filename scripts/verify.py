#!/usr/bin/env python3
"""
Run a candidate solution against test cases before presenting it.

Usage
-----
    python3 scripts/verify.py SOLUTION_FILE --method NAME --cases JSON [--unordered] [--timeout SEC]

SOLUTION_FILE
    A Python file defining either a `Solution` class with the named method,
    or a bare top-level function with that name.

--cases
    A JSON list. Each entry is an object:
        {"args": [...], "expect": ...}                      compare the return value
        {"args": [...], "expect": ..., "inplace": 0}        compare args[0] after the call
                                                            (for problems that mutate input)
    `args` is the argument list, splatted into the call.

--unordered
    Compare lists ignoring order (and ignoring order within nested lists).
    Use for problems like Subsets or Group Anagrams where any order is accepted.

Exit code is 0 when every case passes, 1 otherwise.

Example
-------
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
    """Import the file and return the function to test."""
    spec = importlib.util.spec_from_file_location("candidate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
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
        f"'{method}' not found. Top-level names: {available}"
    )


def canonical(value):
    """Sort nested lists so that order-insensitive comparison works."""
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
    """Return (passed, actual, error_string)."""
    args = copy.deepcopy(case["args"])
    expected = case["expect"]
    inplace_index = case.get("inplace")

    try:
        if timeout:
            import signal

            def on_alarm(signum, frame):
                raise TimeoutError(f"exceeded {timeout}s")

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
    parser.add_argument("solution", help="path to the Python file under test")
    parser.add_argument("--method", required=True, help="method or function name to call")
    parser.add_argument("--cases", required=True, help="JSON list of test cases")
    parser.add_argument("--unordered", action="store_true",
                        help="compare lists ignoring order")
    parser.add_argument("--timeout", type=float, default=5,
                        help="per-case timeout in seconds (0 disables)")
    args = parser.parse_args()

    if not Path(args.solution).exists():
        print(f"FILE NOT FOUND: {args.solution}")
        sys.exit(1)

    try:
        cases = json.loads(args.cases)
    except json.JSONDecodeError as e:
        print(f"BAD --cases JSON: {e}")
        sys.exit(1)

    try:
        fn = load_callable(args.solution, args.method)
    except Exception as e:
        print(f"LOAD FAILED: {e}")
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
    print(f"{passed}/{total} passed")

    for i, case, actual, error in failures:
        print(f"\n--- case {i} FAILED ---")
        print(f"  args     : {json.dumps(case['args'])}")
        print(f"  expected : {json.dumps(case['expect'])}")
        if error:
            print(f"  raised   :\n{error}")
        else:
            print(f"  got      : {json.dumps(actual, default=str)}")

    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
