def factorial(n: int) -> int:
    """
    Calculate factorial of `n`.
    
    Parameters
    ----------
    n : int
        Non-negative integer.

    Returns
    -------
    int
        Factorial of `n`.

    Notes
    -----
    When `sys.getrecursionlimit()` is 3000, the maximum allowed `n` is 2959
    before:
      RecursionError: maximum recursion depth exceeded in comparison
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def factorial_tail_rec(n: int) -> int:
    """
    Same as `factorial` but in tail-recursive style. Since Python does not
    support tail-recursion [1], this function is equivalent to `factorial`.

    Notes
    -----
    The maximum allowed `n` is 2958 (one unit less than in `factorial`).

    References
    ----------
    [1] https://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html
    """
    def factorial_aux(n, current_prod):
        if n == 0:
            return current_prod
        else:
            return factorial_aux(n - 1, current_prod * n)
    return factorial_aux(n, 1)


def factorial_python(n: int) -> int:
    """
    Implementation that works in Python. Tested up to 10^5.
    """
    current_prod = 1
    while True:
        if n == 0:
            return current_prod
        else:
            n, current_prod = n - 1, current_prod * n
