import Mathlib.Algebra.FreeMonoid.Basic


namespace MatrixSolutions

inductive Letters
  | a | b
deriving Repr, DecidableEq

inductive Variables
  | x
deriving Repr, DecidableEq

abbrev Gen := Letters ⊕ Variables
abbrev M := FreeMonoid Gen
abbrev Equation := M × M

def evalGen (soln : Variables → FreeMonoid Letters) : Gen → FreeMonoid Letters
  | .inl l => FreeMonoid.of l
  | .inr v => soln v

def evalWord (soln : Variables → FreeMonoid Letters) : M → FreeMonoid Letters :=
  FreeMonoid.lift (evalGen soln)

def eqnHasSolution (eq : Equation) (soln : Variables → FreeMonoid Letters) : Prop :=
  evalWord soln eq.fst = evalWord soln eq.snd

def word : List Gen → M
  | [] => 1
  | g :: gs => FreeMonoid.of g * word gs

def abax : M := word [.inl Letters.a, .inl Letters.b, .inl Letters.a, .inr Variables.x]
def xaab : M := word [.inr Variables.x, .inl Letters.a, .inl Letters.a, .inl Letters.b]

example : eqnHasSolution (abax, xaab) (
  fun _ => FreeMonoid.of Letters.a * FreeMonoid.of Letters.b
) := by
  simp [
    eqnHasSolution,
    evalWord,
    abax, xaab,
    word,
    evalGen,
    mul_assoc
  ]

end MatrixSolutions
