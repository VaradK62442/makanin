from equationSolver import EquationSolver
from pprint import pprint as pp

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
        self._equations = []
        self._results = {}
        self._formatted_results = {}

    def _generate_equations(self, word="", num_letters=None):
        if num_letters is None:
            num_letters = self.n

        # recursive approach
        # base case: num_letters = 1
        if num_letters <= 1:
            for letter in list(EquationGenerator.ALL_SYMBOLS):
                self._equations.append(word + letter)
        
        else:
            for letter in list(EquationGenerator.ALL_SYMBOLS):
                self._generate_equations(word + letter, num_letters - 1)

    def solve_all(self):
        self._generate_equations()

        for i, v in enumerate(self._equations):
            for j, w in enumerate(self._equations[i+1:]):
                # ensure there is at least one x in the equation
                if "x" not in v and "x" not in w:
                    continue

                e = EquationSolver(v, w)
                soln = e.solve()

                self._results[e] = (soln, e.check_soln(soln))

    def format_results(self):
        for key, value in self._results.items():
            if value[1]:
                if value[0] != "":
                    self._formatted_results[key] = 2
                else:
                    self._formatted_results[key] = 1
            else:
                self._formatted_results[key] = 0

    def print_results(self):
        self.format_results()
        col_width = 15

        for key, value in self._formatted_results.items():
            print(str(key).ljust(col_width) + EquationGenerator.RESULTS_DICT[value])

    def count_soln_types(self):
        self.format_results()

        soln_types = {0: 0, 1: 0, 2: 0}

        for _, value in self._formatted_results.items():
            soln_types[value] += 1

        print(f"Results for n = {self.n}:")
        for key, value in soln_types.items():
            print(f"{EquationGenerator.RESULTS_DICT[key]} - {value}")

def main():
    e = EquationGenerator(3)
    e.solve_all()
    # e.print_results()
    e.count_soln_types()


if __name__ == "__main__":
    main()