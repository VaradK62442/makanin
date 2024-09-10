# utility functions
# things that don't really fit anywhere else in the files
from equationGenerator import EquationGenerator
from equationSolver import EquationSolver

from pprint import pprint as pp
from matplotlib import pyplot as plt
from tqdm import tqdm
from math import comb, ceil


def find_solns_greater_than_1(n, filename):
    results = []
    with open(filename, "w") as file:
        g = EquationGenerator(n)
        g._generate_equations()
        for i, v in enumerate(g._words):
            for _, w in enumerate(g._words[i+1:]):
                if "x" not in v and "x" not in w:
                    continue

                e = g._solver(v, w)
                soln = e.solve()

                valid_soln = e.check_soln(soln)
                if valid_soln and soln == "":
                    if e.V.replace('x', 'a') == e.W.replace('x', 'a'):
                        soln = 'a^k'
                    elif e.V.replace('x', 'b') == e.W.replace('x', 'b'):
                        soln = 'b^k'                
                    
                if valid_soln and len(soln) > 1 and '^' not in soln:
                    results.append((str(e), soln))
                    file.write(f"{str(e)}: x = {soln}\n")


    return results

# find_solns_greater_than_1(5, "solns_greater_than_1.txt")


def analyse_reverse_eqns(n, filename):
    results = {}
    results_count = {True: 0, False: 0}

    g = EquationGenerator(n)
    g._generate_equations()
    for i, v in enumerate(g._words):
        if "x" not in v:
            continue

        w = v[::-1]
        e = g._solver(v, w)
        soln = e.solve()
        valid_soln = e.check_soln(soln)

        if valid_soln and soln == "":
            if e.V.replace('x', 'a') == e.W.replace('x', 'a'):
                soln = 'a^k'
            elif e.V.replace('x', 'b') == e.W.replace('x', 'b'):
                soln = 'b^k'

        results[e] = (soln, valid_soln)

    true_file = open(f"{filename}_true.txt", "w")
    false_file = open(f"{filename}_false.txt", "w")
    for e, (soln, valid_soln) in results.items():
        if valid_soln:
            true_file.write(f"{str(e)}: x = {soln}\n")
            results_count[True] += 1
        else:
            false_file.write(f"{str(e)}\n")
            results_count[False] += 1

    true_file.close(); false_file.close()
    total = results_count[True] + results_count[False]

    return (100 * results_count[True]/total, 100 * results_count[False]/total)


def graph_results(results_dict):
    # expected dict mapping n: (percentage_true, percentage_false)
    _, ax = plt.subplots()
    ax.set_xlabel("n")
    ax.set_ylabel("Percentage of equations")
    ax.set_title("Percentage of equations with solutions")
    ax.bar(results_dict.keys(), [v[0] for v in results_dict.values()], label="True")
    ax.legend()
    plt.show()


def reverse_analysis():
    results = {}
    for i in tqdm(range(2, 11)):
        results[i] = analyse_reverse_eqns(i, f"reverse_eqn_results/reverse_eqns_{i}")

    for i in results.keys():
        pp(f"Results for n = {i}: {results[i][0]:.2f}% have a solution")
    graph_results(results)

# reverse_analysis()


def find_empty_solns(n, filename=None):
    # function to find equations with the empty word as a solution    
    if filename is not None:    
        file = open(filename, "w")

    count = 0
    g = EquationGenerator(n)
    g._generate_equations()

    for i, v in enumerate(g._words):
        for _, w in enumerate(g._words[i:]):
            if "x" not in v and "x" not in w:
                continue

            if v.replace("x", "") == w.replace("x", ""):
                count += 1
                if filename is not None:
                    file.write(f"{v} = {w}\n")

    if filename is not None:
        file.close()
    return count

def empty_soln_formula(n):
    return sum([
        (comb(n, k) + comb(comb(n, k), 2)) * 2**(n-k) for k in range(1, n+1)
    ])

def empty_soln_analysis():
    MAX = 8
    for i in range(2, MAX+1):
        count = find_empty_solns(i, filename=f"empty_soln_results/empty_solns_{i}.txt")
        formula = empty_soln_formula(i)

        print(f"n = {i}, count = {count}, formula = {formula}")

# empty_soln_analysis()


def find_solns_at_least_one(n, filename=None):
    # function to find equations with a solution that is not the empty word
    # and has solution of length 1
    if filename is not None:
        file = open(filename, "w")

    count = 0
    g = EquationGenerator(n)
    g._generate_equations()

    for i, v in enumerate(g._words):
        for _, w in enumerate(g._words[i:]):
            if "x" not in v and "x" not in w:
                continue

            # v and w should have same num of variables
            if sum([1 for c in v if c == "x"]) != sum([1 for c in w if c == "x"]):
                continue

            if v.replace("x", "") != w.replace("x", ""):
                if v.replace("x", "a") == w.replace("x", "a") or v.replace("x", "b") == w.replace("x", "b"):
                    count += 1
                    if filename is not None:
                        file.write(f"{v} = {w}\n")
                        
    if filename is not None:
        file.close()

    return count

def non_empty_analysis():
    MAX = 7
    for i in range(2, MAX+1):
        count = find_solns_at_least_one(i, filename=f"solns_at_least_one_results/solns_at_least_one{i}.txt")
        print(f"n = {i}, count = {count}")

non_empty_analysis()