def fib(n: int) -> int:
    """计算斐波那契数列的第 n 项。

    使用迭代方式实现，避免递归导致的栈溢出和性能问题。

    Args:
        n: 斐波那契数列的项数（从 1 开始计数）。

    Returns:
        第 n 项斐波那契数。n <= 0 时返回 0。
    """
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1

    prev: int = 1
    curr: int = 1
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


if __name__ == "__main__":
    # 基本验证
    test_cases: list[tuple[int, int]] = [
        (-1, 0),
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (5, 5),
        (10, 55),
        (20, 6765),
        (50, 12586269025),
    ]

    for n, expected in test_cases:
        result = fib(n)
        status = "PASS" if result == expected else "FAIL"
        print(f"fib({n}) = {result} (expected {expected}) [{status}]")
