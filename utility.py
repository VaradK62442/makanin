# utility functions
# things that don't really fit anywhere else in the files
from equationGenerator import EquationGenerator
from equationSolver import EquationSolver

from pprint import pprint as pp
from matplotlib import pyplot as plt
from tqdm import tqdm


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


reverse_analysis()