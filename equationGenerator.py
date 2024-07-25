from equationSolver import EquationSolver
from pairwiseEqnSolver import PairwiseEqnSolver

class EquationGenerator:
    # class to generate equations of length n

    LETTERS = EquationSolver.LETTERS
    VARIABLES = EquationSolver.VARIABLES

    ALL_SYMBOLS = LETTERS.union(VARIABLES)
    RESULTS_DICT = {
        2: "Solution found",
        1: "Infinite solutions",
        0: "No solution found",
    }

    def __init__(self, n, solver=EquationSolver):
        self.n = n
        self._words = []
        self._results = {}
        self._formatted_results = {}
        self.soln_found_prop = None
        self._solver = solver

    def _generate_equations(self, word="", num_letters=None):
        if num_letters is None:
            num_letters = self.n

        # recursive approach
        # base case: num_letters = 1
        if num_letters <= 1:
            for letter in list(EquationGenerator.ALL_SYMBOLS):
                self._words.append(word + letter)
        
        else:
            for letter in list(EquationGenerator.ALL_SYMBOLS):
                self._generate_equations(word + letter, num_letters - 1)

    def solve_all(self):
        self._generate_equations()

        for i, v in enumerate(self._words):
            for _, w in enumerate(self._words[i+1:]):
                # ensure there is at least one x in the equation
                if "x" not in v and "x" not in w:
                    continue

                e = self._solver(v, w)
                
                # do not include equation if it has matching prefixes and suffixes
                # e._remove_prefixes_and_suffixes()
                # if e.V == e.v and e.W == e.w:
                soln = e.solve()

                valid_soln = e.check_soln(soln)
                if valid_soln and soln == "":
                    if e.V.replace('x', 'a') == e.W.replace('x', 'a'):
                        soln = 'a^k'
                    elif e.V.replace('x', 'b') == e.W.replace('x', 'b'):
                        soln = 'b^k'                
                
                self._results[e] = (soln, valid_soln)

    def _format_results(self):
        for key, value in self._results.items():
            if value[1]:
                if len(value[0]) == 1:
                    self._formatted_results[key] = (2, value[0])
                else:
                    self._formatted_results[key] = (1, value[0])
            else:
                self._formatted_results[key] = (0, value[0])

    def print_results(self, filename=None):
        self._format_results()
        col_width = 16
        file = open(filename, "w")
        
        for key, value in self._formatted_results.items():
            res = str(key).ljust(col_width) + EquationGenerator.RESULTS_DICT[value[0]].ljust(int(col_width * 1.5))
            if value[0] != 0:
                res += f" - {value[1]}"

            if filename is None:
                print(res)
            else:
                print(res, file=file)

    def count_soln_types(self):
        self._format_results()

        soln_types = {0: 0, 1: 0, 2: 0}

        for _, value in self._formatted_results.items():
            soln_types[value[0]] += 1

        total_solns_found = soln_types[1] + soln_types[2]
        self.soln_found_prop = (total_solns_found) / len(self._formatted_results.values())

        print(f"Results for n = {self.n} with solver {self._solver.__name__}:")
        print(f"Solutions found for {total_solns_found} equations" + \
              f" ({self.soln_found_prop * 100:.2f}%)")

        for key, value in soln_types.items():
            print(f"{EquationGenerator.RESULTS_DICT[key]} - {value}")
        print()

    def run(self, filename=None):
        self.solve_all()
        self.print_results(filename)
        self.count_soln_types()

def compare_soln_types(type1, type2):
    no_match_count = 0
    for solver in type1._formatted_results.keys():
        type1_valid_soln, type1_soln = type1._formatted_results[solver]
        type2_valid_soln, type2_soln = type2._formatted_results[solver]
        if type1_valid_soln == type2_valid_soln:
            if type1_valid_soln != 0 and type1_soln != type2_soln:
                no_match_count += 1
        else:
            no_match_count += 1
            print(f"{type1_valid_soln, type1_soln} != {type2_valid_soln, type2_soln}")
            print(f"{solver}")

    print(f"non-matching solutions: {no_match_count}")

def main():
    n = 4

    e = EquationGenerator(n)
    e.run("results.txt")

    p = EquationGenerator(n, solver=PairwiseEqnSolver)
    p.run("pairwise_results.txt")

    compare_soln_types(e, p)


if __name__ == "__main__":
    main()