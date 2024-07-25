from abstractSolver import AbstractSolver

class PairwiseEqnSolver(AbstractSolver):

    def __init__(self, v, w):
        super().__init__(v, w)

        self.P = []
        for p, q in zip(v, w):
            if p != q:
                self.P.append((p, q))

    def solve(self) -> str:
        # if only (x,x) and (c,c) for c in {a,b}
        if len(self.P) == 0:
            return ""
        
        # if (a,b) in P, no soln
        if {'a', 'b'} in self.P:
            return ""
        
        # if both (a,x) and (b,x) in P, no soln
        if {'a', 'x'} in self.P and {'b', 'x'} in self.P:
            return ""

        # if only (a,x) then x=a is a soln, could be a^k
        if not any([pair[0] == 'b' or pair[1] == 'b' for pair in self.P]):
            if self.V.replace('x', 'a'*self.n) == self.W.replace('x', 'a'*self.n):
                return ""
            elif self.V.replace('x', 'a') == self.W.replace('x', 'a'):
                return "a"
            
        if not any([pair[0] == 'a' or pair[1] == 'a' for pair in self.P]):
            if self.V.replace('x', 'b'*self.n) == self.W.replace('x', 'b'*self.n):
                return ""
            elif self.V.replace('x', 'b') == self.W.replace('x', 'b'):
                return "b"

        return ""
        
def main():
    e = PairwiseEqnSolver("axa", "aba")
    print(e.solve())

if __name__ == "__main__":
    main()