# brute force implementation of Makanin's algorithm
# for solving word equations of size n with one variable
# always assume |v| = |w|

# we always have the case x... = a...
# assuming the equation has no matching prefixes and suffixes

DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


class EquationSolver:

    LETTERS = set("ab")
    VARIABLES = set("x")
    ALLOWED_ITERATIONS = 100

    def __init__(self, v, w):
        assert len(v) == len(w)
        assert set(v).issubset(EquationSolver.LETTERS.union(EquationSolver.VARIABLES))
        assert set(w).issubset(EquationSolver.LETTERS.union(EquationSolver.VARIABLES))

        self.V = v
        self.W = w

        self.v = v
        self.w = w
        self.n = len(v)

        self._replacements = []

    def __str__(self):
        return f"{self.V} = {self.W}"
    
    def __eq__(self, other):
        return self.V == other.V and self.W == other.W

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.V, self.W))
    
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
        # try replacing x with empty string
        # if V == W, then return true
        # else return false
        
        if self.v.replace("x", "") == self.w.replace("x", ""):
            dprint("empty replacement")
            return True
        return False
    
    def backtrack(self):
        self._replacements = self._replacements[::-1]
        solved_x = "x"
        for variable, replacement in self._replacements:
            solved_x = solved_x.replace(variable, replacement)

        solved_x = solved_x.replace("x", "")

        return solved_x

    def solve(self):
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
            if self.v[0] in EquationSolver.VARIABLES and self.w[0] in EquationSolver.LETTERS:
                self._perform_replacement()

            # if v = a.. and w = x.., then swap, and set x = xa, and cancel
            elif self.v[0] in EquationSolver.LETTERS and self.w[0] in EquationSolver.VARIABLES:
                self.v, self.w = self.w, self.v
                dprint(f"swapped: {self}")
                self._perform_replacement()

            dprint(self)
            count += 1

        return self.backtrack()

    def check_soln(self, solved_x):
        return self.V.replace("x", solved_x) == self.W.replace("x", solved_x)
    

def main():
    eqn = EquationSolver("abxax", "axbbx")
    soln = eqn.solve()
    print(f"valid soln: {eqn.check_soln(soln)}")
    print(f"soln: x = {soln}")


if __name__ == "__main__":
    main()