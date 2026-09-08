import Mathlib.Algebra.FreeMonoid.Basic
import MatrixFormalisation.MatrixSolutions

namespace MatrixSolutionsFutureWork

open MatrixSolutions

lemma soln_length_one_keeps_length_sub
  (eq : Equation)
  (_ : eq.fst.length = eq.snd.length)
  (_ : ∃ soln, eqnHasSolutionLengthOne eq soln) :
  ∀ soln, eqnHasSolutionLengthOne eq soln
  → (evalWord soln eq.fst).length = (evalWord soln eq.snd).length := by
    intro soln h_soln
    have h_eq := h_soln.1
    simp [eqnHasSolution] at h_eq
    apply congr_arg
    exact h_eq

lemma evalWord_length_of_soln_length_one
    (soln : Variables → FreeMonoid Letters)
    (hsoln : ∀ v, (soln v).length = 1) :
    ∀ w : M, (evalWord soln w).length = w.length := by
  intro w
  refine FreeMonoid.inductionOn' w ?_ ?_
  · simp [evalWord]
  · intro g xs ih
    have hgenlen : (evalGen soln g).length = 1 := by
      cases g with
      | inl l => simp [evalGen]
      | inr v => simp [evalGen, hsoln v]
    show (evalWord soln (FreeMonoid.of g * xs)).length
           = FreeMonoid.length (FreeMonoid.of g * xs)
    have hstep : evalWord soln (FreeMonoid.of g * xs)
                   = evalGen soln g * evalWord soln xs := by
      simp [evalWord, map_mul]
    rw [hstep, FreeMonoid.length_mul, FreeMonoid.length_mul, hgenlen, ih, FreeMonoid.length_of]

lemma soln_length_one_keeps_length_U
    (eq : Equation)
    (soln : Variables → FreeMonoid Letters)
    (h_soln : eqnHasSolutionLengthOne eq soln) :
    eq.fst.length = (evalWord soln eq.fst).length := by
  rw [evalWord_length_of_soln_length_one soln h_soln.2 eq.fst]

lemma soln_length_one_keeps_length_V
    (eq : Equation)
    (soln : Variables → FreeMonoid Letters)
    (h_soln : eqnHasSolutionLengthOne eq soln) :
    eq.snd.length = (evalWord soln eq.snd).length := by
  rw [evalWord_length_of_soln_length_one soln h_soln.2 eq.snd]

lemma soln_length_one_keeps_letters_U
  (eq : Equation)
  (soln : Variables → FreeMonoid Letters)
  (h_soln : eqnHasSolutionLengthOne eq soln) :
  ∀ i : Fin eq.fst.length,
    let U := eq.fst
    let U_i := U.get i
    let U'_i := (evalWord soln U).get (Fin.cast (
      soln_length_one_keeps_length_U eq soln h_soln
    ) i)
    isLetter U_i → U_i = .inl U'_i := by
      sorry

lemma soln_length_one_keeps_letters_V
  (eq : Equation)
  (soln : Variables → FreeMonoid Letters)
  (h_soln : eqnHasSolutionLengthOne eq soln) :
  ∀ i : Fin eq.snd.length,
    let V := eq.snd
    let V_i := V.get i
    let V'_i := (evalWord soln V).get (Fin.cast (
      soln_length_one_keeps_length_V eq soln h_soln
    ) i)
    isLetter V_i → V_i = .inl V'_i := by
      sorry

theorem soln_length_one_eqn_has_equal_letters
  (eq : Equation)
  (h_equal_length : eq.fst.length = eq.snd.length)
  (h_soln_length_one : ∃ soln, eqnHasSolutionLengthOne eq soln) :
  ∀ i : Fin (equationLength eq h_equal_length),
    let U_i := eq.fst.get i
    let V_i := eq.snd.get (Fin.cast h_equal_length i)
    (isLetter U_i ∧ isLetter V_i) → U_i = V_i := by
      -- there is a solution of length one
      -- => substituting in the solution does not change the length of the words
      -- => substituting does not change the letters at each position
      -- => if both are letters at the same position, they must be equal
      intro i Ui Vi ⟨hUi, hVi⟩
      obtain ⟨soln, h_soln⟩ := h_soln_length_one
      have h_sub_eq : evalWord soln eq.fst = evalWord soln eq.snd := h_soln.1

      have hUi' := soln_length_one_keeps_letters_U eq soln h_soln i hUi
      have hVi' := soln_length_one_keeps_letters_V eq soln h_soln (Fin.cast h_equal_length i) hVi

      let U'_i : Letters := (evalWord soln eq.fst).get
        (Fin.cast (soln_length_one_keeps_length_U eq soln h_soln) i)
      let V'_i : Letters := (evalWord soln eq.snd).get
        (Fin.cast (soln_length_one_keeps_length_V eq soln h_soln)
          (Fin.cast h_equal_length i))

      have hlenEq : (evalWord soln eq.fst).length = (evalWord soln eq.snd).length := by
        simpa using congrArg FreeMonoid.length h_sub_eq

      have hidx :
          Fin.cast (soln_length_one_keeps_length_U eq soln h_soln) i =
          Fin.cast (by
            simpa [h_equal_length, hlenEq] using
              soln_length_one_keeps_length_V eq soln h_soln)
            (Fin.cast h_equal_length i) := by
              simp [Fin.cast]

      have hUV : U'_i = V'_i := by
        sorry

      calc
        Ui = .inl U'_i := hUi'
        _ = .inl V'_i := by rw [hUV]
        _ = Vi := hVi'.symm

end MatrixSolutionsFutureWork
