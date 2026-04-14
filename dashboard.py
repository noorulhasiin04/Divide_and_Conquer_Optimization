import os
import time
from dco import standard_dp, dco_dp, run_benchmark

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    RED     = "\033[91m"
    YELLOW  = "\033[93m"
    WHITE   = "\033[97m"
    DIM     = "\033[2m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def line(w=66):
    print(C.DIM + "-" * w + C.RESET)

def header():
    clear()
    print()
    print(C.CYAN + C.BOLD + "  ╔══════════════════════════════════════════════════════════════╗" + C.RESET)
    print(C.CYAN + C.BOLD + "  ║   🚀  DCO Smart Route Optimizer  —  DAA Project Dashboard   ║" + C.RESET)
    print(C.CYAN + C.BOLD + "  ║        Divide & Conquer Optimization  vs  Standard DP        ║" + C.RESET)
    print(C.CYAN + C.BOLD + "  ╚══════════════════════════════════════════════════════════════╝" + C.RESET)
    print()

def bar(label, value, max_val, color, width=28):
    filled = int((value / max(max_val, 1)) * width)
    empty  = width - filled
    b      = color + "█" * filled + C.DIM + "░" * empty + C.RESET
    print(f"  {label:<12} {b}  {color}{value:,}{C.RESET}")

def show_benchmark(results):
    print(C.BOLD + C.WHITE + "  📊  BENCHMARK RESULTS" + C.RESET)
    line()
    print(f"  {'n':>5}  {'Std Ops':>10}  {'DCO Ops':>10}  {'Speedup':>9}  {'Match':>7}")
    line()
    for r in results:
        sc = C.GREEN if r['speedup'] >= 1 else C.YELLOW
        oc = C.GREEN if r['correct'] else C.RED
        ok = "YES" if r['correct'] else "NO"
        print(
            f"  {C.YELLOW}{r['n']:>5}{C.RESET}  "
            f"{C.RED}{r['std_ops']:>10,}{C.RESET}  "
            f"{C.GREEN}{r['dco_ops']:>10,}{C.RESET}  "
            f"{sc}{r['speedup']:>8}x{C.RESET}  "
            f"{oc}{ok:>7}{C.RESET}"
        )
    line()

def show_bar_chart(results):
    print(C.BOLD + C.WHITE + "  📈  OPERATIONS BAR CHART" + C.RESET)
    line()
    max_ops = max(r['std_ops'] for r in results)
    for r in results:
        print(f"\n  {C.YELLOW}n = {r['n']}{C.RESET}")
        bar("Standard ", r['std_ops'], max_ops, C.RED)
        bar("DCO      ", r['dco_ops'], max_ops, C.GREEN)
    print()
    line()

def show_complexity():
    print(C.BOLD + C.WHITE + "  🧠  COMPLEXITY TABLE" + C.RESET)
    line()
    rows = [
        ("n = 10",   "1,000",         "33",       "~30x"),
        ("n = 50",   "125,000",       "282",       "~443x"),
        ("n = 100",  "1,000,000",     "664",       "~1,506x"),
        ("n = 500",  "125,000,000",   "4,483",     "~27,880x"),
        ("n = 1000", "1,000,000,000", "9,966",     "~100,000x"),
    ]
    print(f"  {'Size':<10}  {'Standard O(n3)':>17}  {'DCO O(n2logn)':>14}  {'Speedup':>11}")
    line()
    for size, std, dco, sp in rows:
        print(
            f"  {C.YELLOW}{size:<10}{C.RESET}  "
            f"{C.RED}{std:>17}{C.RESET}  "
            f"{C.GREEN}{dco:>14}{C.RESET}  "
            f"{C.CYAN}{sp:>11}{C.RESET}"
        )
    line()
    print(f"  {C.DIM}Standard DP  →  O(n3)  |  DCO  →  O(n2 log n){C.RESET}")
    print(f"  {C.DIM}DCO skips unnecessary splits using Monotone Property{C.RESET}")
    line()

def show_custom():
    print(C.BOLD + C.WHITE + "  🎯  TEST YOUR OWN INPUT" + C.RESET)
    line()
    raw = input(C.YELLOW + "  Enter weights separated by spaces\n  Example: 3 7 2 5 4\n  You: " + C.RESET)
    try:
        weights = list(map(int, raw.strip().split()))
        if len(weights) < 2:
            print(C.RED + "\n  Need atleast 2 numbers!" + C.RESET)
            return
        print(C.DIM + f"\n  Your weights  →  {weights}" + C.RESET)
        print(C.DIM +  "  Running both algorithms..." + C.RESET)

        t0 = time.perf_counter()
        ans1, ops1 = standard_dp(weights)
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        ans2, ops2 = dco_dp(weights)
        t3 = time.perf_counter()

        print()
        print(f"  {'Algorithm':<14}  {'Min Cost':>10}  {'Ops Used':>10}  {'Time ms':>10}")
        line()
        print(f"  {C.RED}{'Standard DP':<14}{C.RESET}  "
              f"{C.RED}{ans1:>10}{C.RESET}  "
              f"{C.RED}{ops1:>10,}{C.RESET}  "
              f"{C.RED}{(t1-t0)*1000:>9.3f}{C.RESET}")
        print(f"  {C.GREEN}{'DCO':<14}{C.RESET}  "
              f"{C.GREEN}{ans2:>10}{C.RESET}  "
              f"{C.GREEN}{ops2:>10,}{C.RESET}  "
              f"{C.GREEN}{(t3-t2)*1000:>9.3f}{C.RESET}")
        line()

        if ans1 == ans2:
            sp = round(ops1 / max(ops2, 1), 2)
            print(f"\n  {C.GREEN}Both give SAME answer — DCO is CORRECT!{C.RESET}")
            print(f"  {C.CYAN}DCO used {sp}x operations vs Standard!{C.RESET}")
        else:
            print(f"\n  {C.RED}Something went wrong — check input!{C.RESET}")
        line()
    except ValueError:
        print(C.RED + "\n  Invalid! Numbers only — example: 3 7 2 5 4" + C.RESET)

def main():
    sizes = [5, 10, 15, 20, 30, 50]
    print(C.YELLOW + "\n  Loading... please wait..." + C.RESET)
    results = run_benchmark(sizes)

    while True:
        header()
        print(C.BOLD + "  MENU" + C.RESET)
        line()
        print(f"  {C.CYAN}[1]{C.RESET}  📊  Benchmark Results Table")
        print(f"  {C.CYAN}[2]{C.RESET}  📈  Bar Chart Comparison")
        print(f"  {C.CYAN}[3]{C.RESET}  🧠  Complexity Table")
        print(f"  {C.CYAN}[4]{C.RESET}  🎯  Test Your Own Input")
        print(f"  {C.CYAN}[5]{C.RESET}  🔄  Re-run Benchmark")
        print(f"  {C.RED}[0]{C.RESET}  ❌  Exit")
        line()
        ch = input(C.YELLOW + "  Choose [0-5]: " + C.RESET).strip()

        if ch == "1":
            header()
            show_benchmark(results)
        elif ch == "2":
            header()
            show_bar_chart(results)
        elif ch == "3":
            header()
            show_complexity()
        elif ch == "4":
            header()
            show_custom()
        elif ch == "5":
            header()
            print(C.YELLOW + "  Running benchmark..." + C.RESET)
            results = run_benchmark(sizes)
            print(C.GREEN + "  Done!" + C.RESET)
            time.sleep(1)
            continue
        elif ch == "0":
            clear()
            print(C.GREEN + "\n  Bye da! 👋\n" + C.RESET)
            break
        else:
            print(C.RED + "  Invalid! Choose 0 to 5 only." + C.RESET)
            time.sleep(0.8)
            continue

        input(C.DIM + "\n  Press Enter to go back to menu..." + C.RESET)

if __name__ == "__main__":
    main()
