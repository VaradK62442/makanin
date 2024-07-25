# brute force implementation of Makanin's algorithm
# for solving word equations of size n with one variable
# always assume |v| = |w|

# we always have the case x... = a...
# assuming the equation has no matching prefixes and suffixes

from abstractSolver import AbstractSolver, dprint

class EquationSolver(AbstractSolver):

    ALLOWED_ITERATIONS = 100

    def __init__(self, v, w):
        super().__init__(v, w)
        self._replacements = []
    
    def _remove_prefixes(self):
        i = 0
        while i < self.n and self.v[i] == self.w[i]:
            i += 1
        self.v, self.w = self.v[i:], self.w[i:]
        self.n = min(len(self.v), len(self.w))
        dprint(f"prefixed: {self}")

    def _reverse_words(self):
        self.v, self.w = self.v[::-1], self.w[::-1]

    def _remove_suffixes(self):
        # i = 0
        # while i < self.n and self.v[-i-1] == self.w[-i-1]:
        #     i += 1
        # self.v, self.w = self.v[:-i], self.w[:-i]
        # self.n = min(len(self.v), len(self.w))
        self._reverse_words()
        self._remove_prefixes()
        self._reverse_words()
        dprint(f"suffixed: {self}")

    def _remove_prefixes_and_suffixes(self):
        self._remove_prefixes()
        self._remove_suffixes()

    def _replace_variable(self, variable, replacement):
        self.v = self.v.replace(variable, replacement)
        self.w = self.w.replace(variable, replacement)

    def _perform_replacement(self):
        self._replacements.append((self.v[0], self.w[0] + self.v[0]))
        dprint(f"appended: ({self.v[0]}, {self.w[0] + self.v[0]})")
        self._replace_variable(self.v[0], self.w[0] + self.v[0])
        dprint(f"replaced: {self}")
        self._remove_prefixes_and_suffixes()

    def _try_empty_replacement(self):
        if self.v.replace("x", "") == self.w.replace("x", ""):
            dprint("empty replacement")
            return True
        return False
    
    def _backtrack(self):
        solved_x = "x"
        for variable, replacement in self._replacements:
            solved_x = solved_x.replace(variable, replacement)

        solved_x = solved_x.replace("x", "")

        return solved_x

    def solve(self) -> str:
        dprint(self)

        count = 0
        while count < EquationSolver.ALLOWED_ITERATIONS and self.n > 1:
            # remove prefixes and suffixes
            self._remove_prefixes_and_suffixes()

            # if v = w, then triviality
            if self.v == self.w:
                dprint("Triviality")
                return ""
            
            if self._try_empty_replacement():
                break

            # if v = x.. and w = a.., then set x = ax, and cancel
            if self.v[0] in AbstractSolver.VARIABLES and self.w[0] in AbstractSolver.LETTERS:
                self._perform_replacement()

            # if v = a.. and w = x.., then swap, and set x = xa, and cancel
            elif self.v[0] in AbstractSolver.LETTERS and self.w[0] in AbstractSolver.VARIABLES:
                self.v, self.w = self.w, self.v
                dprint(f"swapped: {self}")
                self._perform_replacement()

            dprint(self)
            count += 1

        return self._backtrack()
    

def main():
    eqn = EquationSolver("abax", "xaab")
    soln = eqn.solve()
    print(f"valid soln: {eqn.check_soln(soln)}")
    print(f"soln: x = {soln}")


if __name__ == "__main__":
    main()