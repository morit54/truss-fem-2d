# Description
Lightweight 2D truss solver using the finite element method.

- no external FE libraries
- NumPy and math only
- easy to run on IOS Pythonista
- optional PDF report with ReportLab

# Features
## Screenshots
- Beispiel auf dem Rechner
- Beispiel mit pythonista

# Installation
## Winwows & Mac
eventuell mit pip

## IOS
Installation auf dem Ipad.

# Quick Start

# Input-Format

# Calculation: Finite Element Method  (linear)
## Element Stiffness Matrix
The element stiffness matrix shall be calculated for each 2D truss element.
The size and angle of each truss element is defined by choosing the start and end node and therefore its coordinates.

$\alpha = \tan^{-1}\left(\frac{opposite}{adjacent}\right) = \tan^{-1}\left(\frac{\Delta y}{\Delta x}\right)
= \tan^{-1}\left(\frac{y_2 - y_1}{x_2 - x_1}\right)$

$E \rightarrow$ modulus of elasticity  
$A \rightarrow$ area of the cross section  
$L = \sqrt{\Delta y^2 + \Delta x^2} = \sqrt{(y_2 - y_1)^2 + (x_2 - x_1)^2}$  

$s = \sin(\alpha)$  
$c = \cos(\alpha)$  


```math
K = 
\frac{E \cdot A}{l} \cdot 
\begin{bmatrix}
c^2 & s \cdot c & -c^2 & -s \cdot c\\
s \cdot c & s^2 & -s \cdot c & -s^2\\
-c^2 & -s \cdot c & c^2 & s \cdot c\\
-s \cdot c & -s^2 & s \cdot c & s^2\\
\end{bmatrix}
```


## Assembly of the System Stiffness Matrix
Assuming we want to calculate a static system with `4 nodes` in total and want to add the first element to the system stiffness matrix.
The first element starts at `node 2` and ends at `node 4`.

### global element stiffness matrix
```math
K = 
\frac{E \cdot A}{l} \cdot 
\begin{bmatrix}
c^2 & s \cdot c & -c^2 & -s \cdot c\\
s \cdot c & s^2 & -s \cdot c & -s^2\\
-c^2 & -s \cdot c & c^2 & s \cdot c\\
-s \cdot c & -s^2 & s \cdot c & s^2\\
\end{bmatrix}
=
\begin{bmatrix}
k_{11} & k_{12} & k_{13} & k_{14}\\
k_{21} & k_{22} & k_{23} & k_{24}\\
k_{31} & k_{32} & k_{33} & k_{34}\\
k_{41} & k_{42} & k_{43} & k_{44}\\
\end{bmatrix}
```

The location (row and column in the system stiffness matrix) of each value of the element stiffness matrix is **only** dependent on the start- and end node of that specific element.

||$u_2$|$v_2$|$u_4$|$v_4$|
|:-:|:-:|:-:|:-:|:-:|
|$F_{x,2}$|$k_{11}$|$k_{12}$|$k_{13}$|$k_{14}$|
|$F_{y,2}$|$k_{21}$|$k_{22}$|$k_{23}$|$k_{24}$|
|$F_{x,4}$|$k_{31}$|$k_{32}$|$k_{33}$|$k_{34}$|
|$F_{y,4}$|$k_{41}$|$k_{42}$|$k_{43}$|$k_{44}$|

### system stiffness matrix
- the matrix will always have a shape of $n \times n$
    - in this case $\rightarrow 2 \,\left[\frac{DOF}{node}\right]$ 
    - $\rightarrow n_{rows} = n_{cols} = n_{nodes} \cdot 2$
- The empty system stiffness matrix contains only zeros.
- each value of all global element stiffness matrices shall be added to  the existing value with matching indices

||$u_1$|$v_1$|$u_2$|$v_2$|$u_3$|$v_3$|$u_4$|$v_4$|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|$F_{x,1}$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|
|$F_{y,1}$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|
|$F_{x,2}$|$0$|$0$|$0 + k_{11}$|$0 + k_{12}$|$0$|$0$|$0 + k_{13}$|$0 + k_{14}$|
|$F_{y,2}$|$0$|$0$|$0 + k_{21}$|$0 + k_{22}$|$0$|$0$|$0 + k_{23}$|$0 + k_{24}$|
|$F_{x,3}$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|
|$F_{y,3}$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|$0$|
|$F_{x,4}$|$0$|$0$|$0 + k_{31}$|$0 + k_{32}$|$0$|$0$|$0 + k_{33}$|$0 + k_{34}$|
|$F_{y,4}$|$0$|$0$|$0 + k_{41}$|$0 + k_{42}$|$0$|$0$|$0 + k_{43}$|$0 + k_{44}$|

## Boundary Conditions

## Solve System
$K \rightarrow$ System Stiffness Matrix  
$F \rightarrow$ force vector  
$u \rightarrow$ displacements  

$$F = K \cdot u$$
by rearranging the equation to
$$u = F \cdot K^{-1}$$
by inverting the system stiffness matrix we can now calculate the displacements of each node in the global coordinate system.

## Support Reactions
Auflagerreaktionen

# Validation
I validated the code by calculating a simple truss example by hand and comparing each result. Click [here](example.ipynb) to go to the example.

# Limitations
The linear system of equations is solved by using `numpy.linalg.solve` which uses a dense LU decomposition (LAPACK). This could result in high memory use.
- **Memory:** the system stiffness matrix is stored densely and is not suitable for large sparse matrices because all of the zeros will be processed.
    - This could result in a `MemoryError` for systems exceeding ~6000 - 9000 DOF (~3000 - 4500 nodes) if the code is run on Pythonista on an Ipad.
    - For larger models with a sparse system stiffness matrix, switching to `scipy.sparse.linalg.spsolve` is recommended.
- **Unstable structures:** If the system stiffnes matrix is singular or nearly singular a `LinAlgError` is expected.

# Project Structure
Hier steht die Projektstruktur.

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.














