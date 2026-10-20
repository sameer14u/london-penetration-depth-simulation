# Interactive Simulation of Magnetic-Field Penetration in Diamagnetic Materials (London Model)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Solid State Physics — Assignment 1 (Question 6)**  
*Interactive Python-based numerical simulation and visualization of external magnetic-field penetration into superconducting and diamagnetic materials using London electrodynamics and Gorter–Casimir two-fluid temperature dependence.*

---

## 📌 Overview

This project provides an interactive simulation platform and computational physics engine to study the Meissner–Ochsenfeld effect and magnetic-field screening in superconducting materials. By solving the second London equation across multiple geometries (infinite slab, long circular cylinder, and rectangular cross-section), the software visualizes:
1. Spatial 2D magnetic-field distributions (colour contour maps).
2. Divergence-free 2D magnetic-field streamlines around and inside materials.
3. 1D radial and transversal field profiles vs. depth from the material surface.
4. Temperature dependence governed by the Gorter–Casimir two-fluid model $\lambda(T) = \lambda_0 / \sqrt{1 - (T/T_c)^4}$.
5. Quantitative parameter studies across applied field $B_0$, zero-temperature penetration depth $\lambda_0$, sample dimensions, and geometries.

---

## 🧮 Theoretical Background

### The London Equations
Proposed by Fritz and Heinz London in 1935 to account for the Meissner effect (zero resistance combined with perfect diamagnetism):

1. **First London Equation** (ballistic acceleration of Cooper pairs / supercarriers):
   $$\frac{\partial \mathbf{J}_s}{\partial t} = \frac{n_s e^2}{m} \mathbf{E}$$

2. **Second London Equation** (flux expulsion / screening condition):
   $$\nabla \times \mathbf{J}_s = -\frac{n_s e^2}{m} \mathbf{B}$$

Combining the curl of Maxwell-Ampère's Law ($\nabla \times \mathbf{B} = \mu_0 \mathbf{J}_s$) with the Coulomb/London gauge yields the Helmholtz screening equation:
$$\nabla^2 \mathbf{B} = \frac{1}{\lambda_L^2} \mathbf{B}$$

where $\lambda_L$ is the **London penetration depth**:
$$\lambda_L = \sqrt{\frac{m}{\mu_0 n_s e^2}}$$

### Temperature Dependence (Two-Fluid Model)
In Gorter and Casimir's thermodynamic model (1934), the total electron density splits into normal $n_n$ and superconducting $n_s$ fractions: $n_s(T) = n_0 [1 - (T/T_c)^4]$. Substituting into $\lambda_L$ gives:
$$\lambda(T) = \frac{\lambda_0}{\sqrt{1 - \left(\frac{T}{T_c}\right)^4}} \quad (T < T_c)$$

At $T \ge T_c$, $\lambda \to \infty$ and $n_s \to 0$, indicating transition into the normal state with full magnetic field penetration.

### Geometry-Specific Solutions
- **Infinite Slab** (thickness $d$, faces at $x = \pm d/2$):
  $$B(x) = B_0 \frac{\cosh(x/\lambda)}{\cosh(d / 2\lambda)}$$
- **Long Cylinder** (radius $R$, axial field $B_0$):
  $$B(r) = B_0 \frac{I_0(r/\lambda)}{I_0(R/\lambda)}$$
  *(where $I_0$ is the zeroth-order modified Bessel function of the first kind).*
- **Rectangular Cross-Section** ($a \times b$ along $x$ and $y$):
  $$B(x, y) \approx B_0 \left[ \frac{\cosh(x/\lambda)}{\cosh(a / 2\lambda)} \right] \cdot \left[ \frac{\cosh(y/\lambda)}{\cosh(b / 2\lambda)} \right]$$

---

## 🚀 Installation & Quick Start

### 1. Prerequisites
Ensure Python 3.9 or higher is installed on your system.

### 2. Setup Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Interactive Web Application
```bash
streamlit run app.py
```
The browser will automatically open at `http://localhost:8501`.

### 5. Run the Automated Physics Test Suite
```bash
python3 test_suite.py
```

### 6. Generate All Report Figures & Graphs
```bash
python3 generate_figures.py
```

---

## 📂 Project Structure

```plaintext
├── Assignment-1.pdf            # Original assignment prompt (Question 6)
├── README.md                   # Project documentation and user guide
├── REPORT.md                   # Comprehensive scientific report with citations
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git tracking exclusions
├── london_physics.py           # Core computational physics engine
├── app.py                      # Interactive Streamlit GUI application
├── test_suite.py               # Unit & physics validation test suite
├── generate_figures.py         # Batch figure generation script
└── figures/                    # Publication-grade figures & UI captures
    ├── app_interface_overview.png
    ├── fig1_2d_slab.png
    ├── fig2_2d_cylinder.png
    ├── fig3_2d_rectangle.png
    ├── fig4_1d_profiles.png
    ├── fig5_temperature_dependence.png
    ├── fig6_geometry_comparison_2d.png
    ├── fig7_geometry_comparison_1d.png
    ├── fig8_lambda_study.png
    ├── fig9_B0_study.png
    ├── fig10_temp_cylinder.png
    └── fig11_materials_comparison.png
```

---

## 🎛️ Simulation Controls & Interactive Features

| Parameter | Type / Range | Physical Interpretation |
|---|---|---|
| **Material** | Dropdown | Pre-configured elemental & ceramic superconductors (Nb, Pb, Al, Sn, Hg, YBCO, or Custom) |
| **Temperature ($T$)** | Slider (0.1 K to $1.05 T_c$) | Sets superfluid fraction $n_s(T)$ and drives $\lambda(T)$ |
| **Applied Field ($B_0$)** | Input (0.001 to 2.0 T) | External magnetic flux density |
| **Geometry** | Radio Buttons | Slab, Cylinder, or Rectangular geometry |
| **Dimensions ($d, R, a, b$)**| Sliders (50 to 3000 nm)| Geometric size compared against $\lambda$ |
| **Grid Resolution** | Slider (100 to 500) | Numerical spatial resolution for 2D field maps |

---

## 🔬 Key Physical Insights Demonstrated

1. **The Meissner Effect vs. Bulk Diamagnetism**: The magnetic field is strictly zero only deep in the interior ($x \gg \lambda$). Near the boundaries ($x \sim \lambda$), persistent screening supercurrents exist within the London penetration layer.
2. **Linear Field Scaling**: Under the London equation, the normalized field $B(x)/B_0$ is independent of $B_0$. Absolute field scales linearly with $B_0$ (valid below $H_{c1}$).
3. **Curvature and Demagnetization**: Cylindrical geometry demonstrates stronger internal field shielding than planar slabs due to azimuthal supercurrent loops concentrating screening efficiency.
4. **Thermal Criticality**: As $T \to T_c$, $\lambda(T)$ exhibits steep power-law divergence; once $T \ge T_c$, complete flux penetration is achieved.

---

## 📚 References

1. London, F., & London, H. (1935). *The Electromagnetic Equations of the Supraconductor*. **Proceedings of the Royal Society of London A**, 149(866), 71–88.
2. Gorter, C. J., & Casimir, H. B. G. (1934). *On Supraconductivity I & II*. **Physica**, 1(1–6), 306–320.
3. Tinkham, M. (2004). *Introduction to Superconductivity* (2nd ed.). Dover Publications.
4. Kittel, C. (2005). *Introduction to Solid State Physics* (8th ed.). John Wiley & Sons.
5. Ashcroft, N. W., & Mermin, N. D. (1976). *Solid State Physics*. Saunders College Publishing.
