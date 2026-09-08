import Mathlib.Algebra.FreeMonoid.Basic
import MatrixFormalisation.Basic

namespace MatrixSolutions

-- 2. Counting equations with solutions

def equationLength (eq : Equation) (_ : eq.fst.length = eq.snd.length) : Nat :=
  eq.fst.length

def eqnHasSolutionLengthOne (eq : Equation) (soln : Variables → FreeMonoid Letters) : Prop :=
  eqnHasSolution eq soln ∧ ∀ y : Variables, (soln y).length = 1

noncomputable
def tau_i
  (eq : Equation)
  (h_equal_length : eq.fst.length = eq.snd.length)
  (i : Fin (equationLength eq h_equal_length))
  (h_soln_length_one : ∃ soln, eqnHasSolutionLengthOne eq soln) : TauSymbols :=
    let U := eq.fst
    let V := eq.snd
    let u_i := U.get i
    let v_i := V.get (Fin.cast h_equal_length i)
    match (u_i, v_i) with
    | (.inl _, .inl _) => TauSymbols.one -- both letters will be equal (see thm in FutureWork.lean)
    | (.inl l, .inr _) => match l with
      | Letters.a => TauSymbols.a
      | Letters.b => TauSymbols.b
    | (.inr _, .inl l) => match l with
      | Letters.a => TauSymbols.a
      | Letters.b => TauSymbols.b
    | (.inr v, .inr _) =>                -- both are x (since only one variable)
      match Classical.choose h_soln_length_one v with
      | [Letters.a] => TauSymbols.α
      | [Letters.b] => TauSymbols.β
      | _ => TauSymbols.one              -- this case will not occur

end MatrixSolutions
