from equationSolver import EquationSolver
from abstractSolver import dprint

class OleksiiSolver(EquationSolver):
    def __init__(self, v: str, w: str):
        super().__init__(v, w)
        dprint(f"initialised: {self}")
        
    def solve(self) -> str:

        def _get_A(self):
            return self.v[1:f"{self.v[1:]}x".find("x")+1]
        
        def _get_B(self):
            return self.w[:self.w.find("x")]
        
        dprint(self)

        count = 0
        prelim = self._preliminary_check()
        if prelim is not None:
            return prelim
        dprint("preliminary check passed")

        if self.v[0] in EquationSolver.LETTERS:
            self.v, self.w = self.w, self.v

        A = _get_A(); B = _get_B()

        while count < EquationSolver.ALLOWED_ITERATIONS and len(A) != len(B) and self.n > 1:
            if self._try_empty_replacement():
                A = ""; B = ""
                break

            A = _get_A(); B = _get_B()
            dprint(f"iteration {count}: {A} {B}; {self.v} = {self.w}; {self.n}")
            self._perform_replacement()

            count += 1

        dprint(f"final: {A} {B}")
        solver = EquationSolver("x"+A, B+"x")
        soln = solver.solve()
        if soln == "":
            soln = "x"
        
        return self._backtrack(solved_x=soln)


def main():
    eqn = OleksiiSolver("xbxab", "abbxx")
    soln = eqn.solve()
    print(f"valid soln: {eqn.check_soln(soln)}")
    print(f"soln: x = {soln}")


if __name__ == "__main__":
    main()