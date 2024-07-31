from equationSolver import EquationSolver
from abstractSolver import dprint

class OleksiiSolver(EquationSolver):
    def __init__(self, v: str, w: str):
        super().__init__(v, w)
        
    def solve(self) -> str:
        dprint(self)

        count = 0
        self._remove_prefixes_and_suffixes()
        if not self._preliminary_check():
            return ""
        A = self._get_A(); B = self._get_B()

        while count < EquationSolver.ALLOWED_ITERATIONS and len(A) != len(B) and self.n > 1:
            # repeat while A and B are different lengths
            self._perform_replacement()
            A = self._get_A(); B = self._get_B()
            dprint(A, B)

            count += 1

        dprint(f"final: {A} {B}")
        solver = EquationSolver("x"+A, B+"x")
        soln = solver.solve()
        if soln == "":
            soln = "x"
        
        return self._backtrack(solved_x = soln)

    def _get_A(self):
        return self.v[1:f"{self.v[1:]}x".find("x")+1]
    
    def _get_B(self):
        return self.w[:self.w.find("x")]


def main():
    eqn = OleksiiSolver("xbxab", "abbxx")
    soln = eqn.solve()
    print(f"valid soln: {eqn.check_soln(soln)}")
    print(f"soln: x = {soln}")


if __name__ == "__main__":
    main()