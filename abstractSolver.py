DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

class AbstractSolver:
    
    LETTERS = set("ab")
    VARIABLES = set("x")
    
    def __init__(self, v: str, w: str):
        assert len(v) == len(w)
        assert set(v).issubset(AbstractSolver.LETTERS.union(AbstractSolver.VARIABLES))
        assert set(w).issubset(AbstractSolver.LETTERS.union(AbstractSolver.VARIABLES))

        self.v = v
        self.w = w
        self.n = len(v)

        self._remove_prefixes_and_suffixes()

        self.V = self.v
        self.W = self.w

    def __str__(self):
        return f"{self.V} = {self.W}"
    
    def __eq__(self, other: "AbstractSolver"):
        return self.V == other.V and self.W == other.W
    
    def __ne__(self, other: "AbstractSolver"):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.V, self.W))
    
    def _preliminary_check(self) -> str | None:
        if self.v == "" or self.w == "":
            return ""

        if self.v[0] in AbstractSolver.LETTERS and self.w[0] in AbstractSolver.LETTERS:
            dprint("both in variables")
            if self.v[0] != self.w[0]:
                dprint("not equal")
                return ""

        if self.v[-1] in AbstractSolver.LETTERS and self.w[-1] in AbstractSolver.LETTERS:
            dprint("both in variables")
            if self.v[-1] != self.w[-1]:
                dprint("not equal")
                return ""

        if sum([1 for l in self.v if l in AbstractSolver.LETTERS]) != sum([1 for l in self.w if l in AbstractSolver.LETTERS]):
            dprint("diff num consts")
            for l in AbstractSolver.LETTERS:
                if self.v.replace("x", l) == self.w.replace("x", l):
                    return l
            else:
                return ""

        return None
    
    def _remove_prefixes(self):
        i = 0
        while i < self.n and self.v[i] == self.w[i]:
            i += 1
        self.v, self.w = self.v[i:], self.w[i:]
        self.n = min(len(self.v), len(self.w))
        dprint(f"prefixed: {self.v} = {self.w}")

    def _reverse_words(self):
        self.v, self.w = self.v[::-1], self.w[::-1]

    def _remove_suffixes(self):
        self._reverse_words()
        self._remove_prefixes()
        self._reverse_words()
        dprint(f"suffixed: {self.v} = {self.w}")

    def _remove_prefixes_and_suffixes(self):
        self._remove_prefixes()
        self._remove_suffixes()
    
    def solve(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")
    
    def check_soln(self, soln: str) -> bool:
        return self.V.replace("x", soln) == self.W.replace("x", soln)