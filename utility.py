# utility functions
# things that don't really fit anywhere else in the files
from equationGenerator import EquationGenerator

from pprint import pprint as pp

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
    pp(f"Results for n={n}: {results_count} ({100 * results_count[True] / (results_count[True] + results_count[False]):.2f}% have a solution)")


analyse_reverse_eqns(2, "reverse_eqn_results/reverse_eqns_2")
analyse_reverse_eqns(3, "reverse_eqn_results/reverse_eqns_3")
analyse_reverse_eqns(4, "reverse_eqn_results/reverse_eqns_4")
analyse_reverse_eqns(5, "reverse_eqn_results/reverse_eqns_5")
analyse_reverse_eqns(6, "reverse_eqn_results/reverse_eqns_6")
analyse_reverse_eqns(7, "reverse_eqn_results/reverse_eqns_7")