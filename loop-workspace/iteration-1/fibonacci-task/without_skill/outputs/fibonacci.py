def fib(n: int) -> int:
    """Calculate the nth Fibonacci number using iteration.

    Args:
        n: The index in the Fibonacci sequence (1-indexed).

    Returns:
        The nth Fibonacci number. Returns 0 for n <= 0.
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    a: int = 0
    b: int = 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    test_cases = [0, 1, 2, 3, 5, 10, 20, 50]
    for n in test_cases:
        print(f"fib({n}) = {fib(n)}")
