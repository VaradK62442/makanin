from equationGenerator import EquationGenerator
from equationSolver import EquationSolver
from abstractSolver import dprint

from time import time

def generate_all_equations(n):
    equations = []

    g = EquationGenerator(n)
    g._generate_equations()

    for i, v in enumerate(g._words):
        for _, w in enumerate(g._words[i+1:]):
            if "x" not in v and "x" not in w:
                continue
            equations.append(EquationSolver(v, w))

    return equations


def get_num_letters_in_set(word, set):
    return len([v for v in word if v in set])


def get_desired_equations(equations):
    # get all eqns with same number of constants    
    return [
        eqn for eqn in equations if \
            get_num_letters_in_set(eqn.V, EquationSolver.LETTERS) == \
                get_num_letters_in_set(eqn.W, EquationSolver.LETTERS)
    ]


def do_solns_exist(equations):
    def run(eqn) -> str:
        letters = EquationSolver.LETTERS
        variables = EquationSolver.VARIABLES

        def case1(eqn):
            # case 1: Cx... = xD...
            return (all([x in eqn.V for x in variables]) and eqn.V[0] not in variables and eqn.W[0] in variables and eqn.W[1] in letters) or \
                   (eqn.V[0] in variables and eqn.V[1] in letters and all([x in eqn.W for x in variables]) and eqn.W[0] not in variables)
        
        
        def case2(eqn):
            # case 2: Cx... = xx...
            return (all([x in eqn.V for x in variables]) and eqn.V[0] not in variables and all([l in variables for l in eqn.W[:2]])) or \
                   (all([l in variables for l in eqn.V[:2]]) and all([x in eqn.W for x in variables]) and eqn.W[0] not in variables)
                   

        def case3(eqn):
            # case 3: x... = C...
            return (eqn.V[0] in letters and eqn.W[0] in variables) or \
                   (eqn.V[0] in variables and eqn.V[0] in letters)

        # try trivial soln
        V, W = eqn.V, eqn.W
        x_is_non_trivial = False
        V = V.replace("x", ""); W = W.replace("x", "")#
        if V == W:
            return ""
        else:
            x_is_non_trivial = True

        def prefixes_match(v, w):
            # check if letters up to first occurrence of x are equal
            v_consts = v[:v.find("x")]; w_consts = w[:w.find("x")]
            min_length = min(len(v_consts), len(w_consts))
            v_consts = v_consts[:min_length]; w_consts = w_consts[:min_length]

            return v_consts == w_consts

        if not prefixes_match(eqn.V, eqn.W) or not prefixes_match(eqn.V[::-1], eqn.W[::-1]):
            return False

        # check number of variables in eqn
        if get_num_letters_in_set(eqn.V, EquationSolver.VARIABLES) != get_num_letters_in_set(eqn.W, EquationSolver.VARIABLES):
            return False
        
        if case1(eqn):
            dprint(f"Case 1: {eqn}")
            # of the form Cx... = xD...
            # extract just C'x, xD'
            if eqn.V[0] in variables:
                V = eqn.W; W = eqn.V
            else:
                V = eqn.V; W = eqn.W

            C_length = V.find("x")
            D_length = f"{W[1:]}x".find("x") # add dummy x to end
            
            if C_length > D_length:
                return None

            min_length = min(C_length, D_length)
            C = V[:C_length]; D = W[1:D_length+1]

            C_prime = C[C_length-min_length:]
            D_prime = D[:min_length]

            e = EquationSolver(C_prime+"x", "x"+D_prime, x_is_non_trivial)
            quad_soln = e.solve()

            if eqn.V.replace("x", quad_soln) == eqn.W.replace("x", quad_soln):
                return quad_soln
            else: return False 

        elif case2(eqn):
            return None

        elif case3(eqn):
            return None
        
        else: return None


    results = []
    # equations = [EquationSolver("bbaxa", "xbaba")]
    for eqn in equations:
        results.append(run(eqn))
    
    print(f"Solutions found: {len([e for e in results if type(e) == type('')])}")
    print(f"Solutions not found: {len([e for e in results if e == False])}")
    print(f"Other: {len([e for e in results if e == None])}")

    # check validity against EquationSolver
    invalid_solns = 0
    for i, result in enumerate(results):
        e = equations[i]
        soln = e.solve()
        valid_soln = e.check_soln(soln)
        if result != False and result != None:
            if result != soln:
                print(f"Invalid result: {e}, {result}, {soln}")
                invalid_solns += 1

        elif result is False:
            if valid_soln:
                print(f"Invalid result: {e}, {result}, {soln}")
                invalid_solns += 1

    print(f"Invalid solns: {invalid_solns}")


def main():
    start_time = time()

    n = 6
    equations = generate_all_equations(n)
    same_const_eqns = get_desired_equations(equations)
    do_solns_exist(same_const_eqns)

    print(f"Time taken: {time() - start_time}")


if __name__ == "__main__":
    main()