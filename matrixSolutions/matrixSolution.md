# Matrix Solutions

Related code in file ```matrixSolution.py```.

Given an equation $U = V$ with $U$ and $V$ having a differing number of constants, say $abx = xbx$, we can convert it into a vector, $(a, b, x)^T = (x, b, x)^T$.
This equation has the solution $x = a$, and a matrix can be used that represents this equation and its solution.
We need a matrix $A$ such that $Au = Av$, where $u$ and $v$ are the vectors representing the variables in the equation.

The above example has matrix
$$
A = \begin{bmatrix}
    a & 0 & 0\\
    0 & 1 & 0\\
    0 & 0 & a
\end{bmatrix}
$$
defined under the multiplication operation:

- $c * c = c$

- $c * x = c$

- $c * 1 = c$

where $c \in \{a, b\}$.
We must have that the matrix is diagonal, and cannot contain both $a$ and $b$.

One equation can also have many matrices. For example, the above equation could have matrix
$$
A = \begin{bmatrix}
    1 & 0 & 0\\
    0 & 1 & 0\\
    0 & 0 & a
\end{bmatrix}
$$
To mitigate this, we require that the $(i,i)^\text{th}$ entry in the matrix is $1$ if and only if the $i^\text{th}$ letters in each side of the equation are both constants.

Note that one matrix can correspond to multiple equations. 
For example, the above matrix can also be used to solve $xba = aba$.

Since one matrix can correspond to multiple equations, we can construct an equivalence relation between equations.
Define $(U, V) \sim (W, X)$ if and only if there exists a matrix $A$ such that $Au = Av$ and $Aw = Ax$.
This partitions the set of all equations of the same length $n$, $S_n$, into equivalence classes.

The question is now the following. Given a matrix $A$, can we recover *all* (or at least some) of the equations that correspond to it?
For example, for the above matrix
$$
A = \begin{bmatrix}
    a & 0 & 0\\
    0 & 1 & 0\\
    0 & 0 & a
\end{bmatrix}
$$
defined under the multiplication operation, we have that the first element must be either $a$ or $x$ (since $a*b$ is not defined), but not both $a$.

- $a** = x**$

- $x** = x**$

The second element must be either $a$ or $b$ (since it must be a constant).

- $*\;a\;* = *\;a\;*$

- $*\;b\;* = *\;b\;*$

The third element must be either $a$ or $x$ by above.

- $**a = **x$

- $**x = **a$

- $**x = **x$

This leads to $2$ choices for first letter, $2$ for second, and $3$ for third, so $12$ total equations.

- $aaa = xax$

- $aax = xaa$**

- $aax = xax$

- $aba = xbx$

- $abx = xba$**

- $abx = xbx$

- $xaa = xax$

- $xax = xaa$*

- $xax = xax$*

- $xba = xbx$

- $xbx = xba$*

- $xbx = xbx$*

After redundancies removed (*), we have 8 equations.
After removing equations with both sides having the same number of constants (**), we have 6 equations.

Hence, the matrix $A$ corresponds to these $6$ equations.

- $aaa = xax$

- $aax = xax$

- $aba = xbx$

- $abx = xbx$

- $xaa = xax$

- $xba = xbx$

Note that we can represent a matrix as a tuple with the diagonal elements, to make things easier to express. 
e.g. the above matrix $A$ would be represented as the tuple $(a, 1, a)$.

### Future thoughts

Notice that the more "rules" we add on the matrix / tuple, the more information we encode, but the more the tuple just represents the equation itself. For example, adding another symbol for the $i^\text{th}$ elements both being $x$ will further disambiguate equations and give more information in the matrix.

We want to strike a careful balance between encoding too little and encoding too much, since we don't want to just end up essentially having a unique tuple for each equation.

---

## $\alpha$, $\beta$ symbols

Similar to the $a$ and $1$ symbol, we introduce a new symbol that can be in the matrix - $\alpha$ and $\beta$. An $\alpha$ is in the $i^\text{th}$ position in the matrix if and only if the $i^\text{th}$ letters are both $x$, and the solution is $x=a$. This is symmetric with $\beta$, except if the solution is $x=b$. 

## Counting

We have the following formula to count all possible equations for a given value of $n$. Fix a matrix with some $k$ number of $a$ elements. This gives 
$$
\sum_{i=0}^{\left\lceil {k\over 2}\right\rceil-1}{k\choose i}
$$
possible equations that are contributed by the $a$ elements.
The remaining values are either $1$ or $\alpha$. $\alpha$ contributes one equation, $1$ contributes two. To count the number of equations contributed, we have
$$
\sum_{j=0}^{n-k}2^j{n-k\choose j}.
$$
This multiplied by two to account for $a$ or $b$, and then multiplied by $n\choose k$ gives all possible equations for a fixed $k$.
Thus, the number of all possible equations for a fixed $n$ is
$$
\sum_{k=0}^n\left(2{n\choose k}\times\sum_{i=0}^{\left\lceil {k\over 2}\right\rceil-1}{k\choose i}\times\sum_{j=0}^{n-k}2^j{n-k\choose j}\right).
$$

Note that this only generates equations which lead to equations with differing number of constants on either side.