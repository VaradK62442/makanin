import Mathlib.Algebra.FreeMonoid.Basic

-- 1. Background

inductive Letters
  | a | b
deriving Repr, DecidableEq

inductive Variables
  | x
deriving Repr, DecidableEq

inductive TauSymbols
  | one | a | b | α | β
deriving Repr, DecidableEq

abbrev Gen := Letters ⊕ Variables
abbrev M := FreeMonoid Gen
abbrev Equation := M × M

def isLetter : Gen → Prop :=
  fun g => ∃ l : Letters, g = .inl l

def isVariable : Gen → Prop :=
  fun g => ∃ v : Variables, g = .inr v

abbrev a : Gen := .inl Letters.a
abbrev b : Gen := .inl Letters.b
abbrev x : Gen := .inr Variables.x

def evalGen (soln : Variables → FreeMonoid Letters) : Gen → FreeMonoid Letters
  | .inl l => FreeMonoid.of l
  | .inr v => soln v

def evalWord (soln : Variables → FreeMonoid Letters) : M → FreeMonoid Letters :=
  FreeMonoid.lift (evalGen soln)

def eqnHasSolution (eq : Equation) (soln : Variables → FreeMonoid Letters) : Prop :=
  evalWord soln eq.fst = evalWord soln eq.snd

-- helper to construct words
def word : List Gen → M
  | [] => 1
  | g :: gs => FreeMonoid.of g * word gs

example : eqnHasSolution (word [a, b, a, x], word [x, a, a, b]) (
  fun _ => FreeMonoid.of Letters.a * FreeMonoid.of Letters.b
) := by
  simp [
    eqnHasSolution,
    evalWord,
    word,
    evalGen,
    mul_assoc
  ]
