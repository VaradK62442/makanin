DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

class AbstractSolver:
    
    LETTERS = set("ab")
    VARIABLES = set("x")
    
    def __init__(self, v: str, w: str):
        assert len(v) == len(w)
        assert set(v).issubset(AbstractSolver.LETTERS.union(AbstractSolver.VARIABLES))
        assert set(w).issubset(AbstractSolver.LETTERS.union(AbstractSolver.VARIABLES))

        self.V = v
        self.W = w

        self.v = v
        self.w = w
        self.n = len(v)

    def __str__(self):
        return f"{self.V} = {self.W}"
    
    def __eq__(self, other: "AbstractSolver"):
        return self.V == other.V and self.W == other.W
    
    def __ne__(self, other: "AbstractSolver"):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.V, self.W))
    
    def _preliminary_check(self) -> bool:
        if self.v[0] in AbstractSolver.VARIABLES and self.w[0] in AbstractSolver.VARIABLES:
            if self.v[0] != self.w[0]:
                return False
        return True
    
    def solve(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")
    
    def check_soln(self, soln: str) -> bool:
        return self.V.replace("x", soln) == self.W.replace("x", soln)