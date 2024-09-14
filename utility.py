# utility functions
# things that don't really fit anywhere else in the files
from equationGenerator import EquationGenerator
from equationSolver import EquationSolver

from pprint import pprint as pp
from matplotlib import pyplot as plt
from tqdm import tqdm
from math import comb, ceil
import os


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



def find_solns_given_criteria(n, criteria, filename=None):
    # function to find equations with solutions that satisfy the given criteria
    if filename is not None:
        file = open(filename, "w")

    count = 0
    g = EquationGenerator(n)
    g._generate_equations()

    for i, v in enumerate(g._words):
        for _, w in enumerate(g._words[i:]):
            if "x" not in v and "x" not in w:
                continue

            if criteria(v, w):
                count += 1
                if filename is not None:
                    file.write(f"{v} = {w}\n")

    if filename is not None:
        file.close()

    return count

def find_soln_analysis(criteria, folder):
    print(f"results for {criteria.__name__}")
    SUPER_FOLDER = "soln_analysis"
    full_folder = os.path.join(SUPER_FOLDER, folder)
    MAX = 7
    if not os.path.isdir(full_folder):
        os.mkdir(full_folder)
    for i in range(2, MAX+1):
        count = find_solns_given_criteria(i, criteria, filename=f"{full_folder}/{folder}_{i}.txt")
        print(f"n = {i}, count = {count}")
        print(f"n = {i}, count = {count}", file=open(f"{full_folder}/{folder}.txt", "a"))

def soln_is_valid(v, w, soln):
    return v.replace("x", soln) == w.replace("x", soln)


def is_empty_soln(v, w):
    return soln_is_valid(v, w, "")

def find_empty_solns(n, filename=None):
    return find_solns_given_criteria(n, is_empty_soln, filename)

def empty_soln_formula(n):
    return sum([
        (comb(n, k) + comb(comb(n, k), 2)) * 2**(n-k) for k in range(1, n+1)
    ])

def empty_soln_analysis():
    find_soln_analysis(is_empty_soln, "empty_soln_results")

# empty_soln_analysis()


def soln_length_one(v, w):
    if soln_is_valid(v, w, ""):
        if soln_is_valid(v, w, "a") or soln_is_valid(v, w, "b"):
            return True
    return False

def find_solns_at_least_one(n, filename=None):
    # function to find equations with a solution that is not the empty word
    # and has solution of length 1
    return find_solns_given_criteria(n, soln_length_one, filename)

def soln_length_one_analysis():
    return find_soln_analysis(soln_length_one, "soln_length_one_results")

# soln_length_one_analysis()


def soln_length_two(v, w):
    if not soln_is_valid(v, w, ""):
        if not soln_is_valid(v, w, "a") and not soln_is_valid(v, w, "b"):
            if soln_is_valid(v, w, "aa") or soln_is_valid(v, w, "ab") or soln_is_valid(v, w, "ba") or soln_is_valid(v, w, "bb"):
                return True
    return False

def find_solns_size_two(n, filename=None):
    """
    Find equations with solutions of size two
    and not size one or empty
    """
    return find_solns_given_criteria(n, soln_length_two, filename)

def two_soln_analysis():
    find_soln_analysis(soln_length_two, "soln_length_two_results")

# two_soln_analysis()


def soln_empty_and_one(v, w):
    if soln_is_valid(v, w, ""):
        if soln_is_valid(v, w, "a") or soln_is_valid(v, w, "b"):
            return True
    return False

def find_solns_empty_and_one(n, filename=None):
    # function to find equations with a solution that is empty word
    # and has solution of length 1
    return find_solns_given_criteria(n, soln_empty_and_one, filename)

def empty_and_one_analysis():
   return find_soln_analysis(soln_empty_and_one, "empty_and_one_results")

# empty_and_one_analysis()


def soln_one_and_two(v, w):
    if not soln_is_valid(v, w, ""):
        if soln_is_valid(v, w, "a") or soln_is_valid(v, w, "b"):
            if soln_is_valid(v, w, "aa") or soln_is_valid(v, w, "ab") or soln_is_valid(v, w, "ba") or soln_is_valid(v, w, "bb"):
                return True
    return False

def find_solns_one_and_two(n, filename=None):
    # function to find equations with a solution that is not the empty word
    # and has solution of length 1 and 2
    return find_solns_given_criteria(n, soln_one_and_two, filename)

def one_and_two_analysis():
    return find_soln_analysis(soln_one_and_two, "one_and_two_results")

# one_and_two_analysis()