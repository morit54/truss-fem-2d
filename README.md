# truss-fem-2d

## Description
Lightweight 2D truss solver using the finite element method.

- no external FE libraries
- NumPy and math only
- easy to run on IOS Pythonista
- optional PDF report with ReportLab

## Features
### Screenshots
- Beispiel auf dem Rechner
- Beispiel mit pythonista

## Installation
### Winwows & Mac
eventuell mit pip
### IOS
Installation auf dem Ipad.

## Quick Start

## Input-Format

## Calculation (FE-Theory)
### Element Stiffness Matrix
The element stiffness matrix shall be calculated for each 2D truss element.
The size and angle of each truss element is defined by choosing the start and end node and therefore its coordinates.

$\alpha = \tan^{-1}\left(\frac{opposite}{adjacent}\right) = \tan^{-1}\left(\frac{\Delta y}{\Delta x}\right)
= \tan^{-1}\left(\frac{y_2 - y_1}{x_2 - x_1}\right)$

$s = \sin(\alpha)$  
$c = \cos(\alpha)$  


$$
\frac{E \cdot A}{l} \cdot 
\begin{bmatrix}
c^2 & s \cdot c & -c^2 & -s \cdot c\\
s \cdot c & s^2 & -s \cdot c & -s^2\\
-c^2 & -s \cdot c & c^2 & s \cdot c\\
-s \cdot c & -s^2 & s \cdot c & s^2\\
\end{bmatrix}
\cdot
\begin{bmatrix}
u_1\\ v_1\\ u_2\\ v_2\\
\end{bmatrix}
=
\begin{bmatrix}
F_{x1}\\ F_{y1}\\ F_{x2}\\ F_{y2}\\
\end{bmatrix}
$$

$$
K =
\begin{bmatrix}
k_{11} & k_{12} & k_{13} & k_{14}\\
k_{21} & k_{22} & k_{23} & k_{24}\\
k_{31} & k_{32} & k_{33} & k_{34}\\
k_{41} & k_{42} & k_{43} & k_{44}\\
\end{bmatrix}
$$


### Assembly of the System Stiffness Matrix
### Boundary Conditions
### Solve System

$$
\begin{bmatrix}
k_{11} & k_{12} & k_{13} & k_{14}\\
k_{21} & k_{22} & k_{23} & k_{24}\\
k_{31} & k_{32} & k_{33} & k_{34}\\
k_{41} & k_{42} & k_{43} & k_{44}\\
\end{bmatrix}
\cdot
\begin{bmatrix}
u_1\\ v_1\\ u_2\\ v_2\\
\end{bmatrix}
=
\begin{bmatrix}
F_{x1}\\ F_{y1}\\ F_{x2}\\ F_{y2}\\
\end{bmatrix}
$$




$F = K \cdot u$
### Support Reactions
Auflagerreaktionen

## Validation

## Limitations
Systemgrenzen

## Project Structure
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.














