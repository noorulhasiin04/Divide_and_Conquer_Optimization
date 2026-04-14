import time
import random

INF = float('inf')

def build_prefix(weights):
    P = [0] * (len(weights) + 1)
    for i, v in enumerate(weights):
        P[i+1] = P[i] + v
    return P

def cost(P, i, j):
    return P[j+1] - P[i]

def standard_dp(weights):
    n = len(weights)
    P = build_prefix(weights)
    dp = [[0]*n for _ in range(n)]
    ops = 0
    for l in range(2, n+1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = INF
            for k in range(i, j):
                ops += 1
                val = dp[i][k] + dp[k+1][j] + cost(P, i, j)
                if val < dp[i][j]:
                    dp[i][j] = val
    return dp[0][n-1], ops

def dco_dp(weights):
    n = len(weights)
    P = build_prefix(weights)
    dp  = [[INF]*n for _ in range(n)]
    ops = [0]
    for i in range(n):
        dp[i][i] = 0

    def solve(length, lo, hi, opt_lo, opt_hi):
        if lo > hi:
            return
        mid = (lo + hi) // 2
        j   = mid + length - 1
        if j >= n:
            solve(length, lo, mid-1, opt_lo, opt_hi)
            return
        best_k = opt_lo
        best_v = INF
        for k in range(opt_lo, min(opt_hi, j-1) + 1):
            ops[0] += 1
            val = dp[mid][k] + dp[k+1][j] + cost(P, mid, j)
            if val < best_v:
                best_v = val
                best_k = k
        dp[mid][j] = best_v
        solve(length, lo,    mid-1, opt_lo,  best_k)
        solve(length, mid+1, hi,    best_k, opt_hi)

    for length in range(2, n+1):
        solve(length, 0, n - length, 0, n - 2)

    return dp[0][n-1], ops[0]

def run_benchmark(sizes, seed=42):
    results = []
    random.seed(seed)
    for n in sizes:
        weights = [random.randint(1, 20) for _ in range(n)]
        t0 = time.perf_counter()
        ans1, ops1 = standard_dp(weights)
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        ans2, ops2 = dco_dp(weights)
        t3 = time.perf_counter()
        results.append({
            'n'        : n,
            'std_ops'  : ops1,
            'dco_ops'  : ops2,
            'std_time' : round((t1 - t0) * 1000, 3),
            'dco_time' : round((t3 - t2) * 1000, 3),
            'speedup'  : round(ops1 / max(ops2, 1), 2),
            'correct'  : ans1 == ans2
        })
    return results