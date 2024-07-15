from equationSolver import EquationSolver

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

    def __init__(self, n):
        self.n = n
        self._words = []
        self._results = {}
        self._formatted_results = {}
        self.soln_found_prop = None

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

                e = EquationSolver(v, w)
                
                # do not include equation if it has matching prefixes and suffixes
                # e._remove_prefixes_and_suffixes()
                # if e.V == e.v and e.W == e.w:
                soln = e.solve()
                self._results[e] = (soln, e.check_soln(soln))

    def _format_results(self):
        for key, value in self._results.items():
            if value[1]:
                if value[0] != "":
                    self._formatted_results[key] = (2, value[0])
                else:
                    self._formatted_results[key] = (1, value[0])
            else:
                self._formatted_results[key] = (0, value[0])

    def print_results(self, filename=None):
        self._format_results()
        col_width = 15
        file = open(filename, "w")
        
        for key, value in self._formatted_results.items():
            res = str(key).ljust(col_width) + EquationGenerator.RESULTS_DICT[value[0]]
            if value[0] == 2:
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

        print(f"Results for n = {self.n}:")
        print(f"Solutions found for {total_solns_found} equations" + \
              f" ({self.soln_found_prop * 100:.2f}%)")

        for key, value in soln_types.items():
            print(f"{EquationGenerator.RESULTS_DICT[key]} - {value}")

def main():
    n = 3
    e = EquationGenerator(n)
    e.solve_all()
    e.print_results(filename="results.txt")
    e.count_soln_types()


if __name__ == "__main__":
    main()