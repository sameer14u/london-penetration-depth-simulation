# Project Guide: Interactive Simulation of Magnetic-Field Penetration in a Diamagnetic Material

## Solid State Physics — Assignment 1 (Question 6)
**Indian Institute of Technology Hyderabad (IIT Hyderabad)**  
**Department of Physics | B.Tech. Engineering Physics**  
**Course Instructor**: Prof. Arabinda Haldar  

---

### 👥 Team Members
1. **EP24BTECH11025** — Sameer Choudhary*
2. **EP24BTECH11024** — Samarth Gupta
3. **EP24BTECH11032** — Tejas Prashant Bharadwaj
4. **EP24BTECH11026** — Samyak Rai
5. **EP24BTECH11027** — Saraangan B
6. **EP24BTECH11028** — Savireddy Ansika
7. **EP24BTECH11029** — Shanmukh Machiraju
8. **EP24BTECH11030** — Snigdha Indupalli
9. **EP24BTECH11031** — Srija Baratam
10. **EP24BTECH11033** — Vishal

**Official GitHub Repository**:  
[`https://github.com/sameer14u/london-penetration-depth-simulation`](https://github.com/sameer14u/london-penetration-depth-simulation)

---

## 1. Overview & Objectives

This guide provides a comprehensive manual for the **Question 6 Assignment: Interactive Simulation of Magnetic-Field Penetration in a Diamagnetic Material**. It details the underlying physics in clear terms, explains how the numerical simulation works, describes every file in the directory, outlines installation and execution procedures, provides troubleshooting guidance, and walks through the project workflow.

### Project Goals Achieved
- **Theoretical Foundations**: Rigorous mathematical formulation of London electrodynamics, the first and second London equations, boundary-value problems across three distinct geometries, and the Gorter–Casimir two-fluid model.
- **Numerical Simulation Engine**: Numerically stable implementation solving for 1D and 2D spatial distributions of magnetic field inside and outside superconducting materials, with overflow protection for large aspect ratios ($d/\lambda, R/\lambda > 500$).
- **Interactive User Interface**: Full-featured web dashboard built in **Streamlit** with 6 intuitive tabs, live slider controls, immediate reactive updates, and physical screening metrics.
- **Visualizations**: 2D vector streamline diagrams, high-resolution contour colourmaps, 1D attenuation vs. depth plots, temperature divergence curves, and cross-geometry comparative analyses.
- **Native LaTeX Document Typesetting**: The final academic report is typeset and compiled entirely using native LaTeX (`latex_report/report.tex`), using proper mathematical equation environments (`equation`, `align`), standard academic typography, and genuine simulation figures.
- **Quality Assurance**: Automated unit and physics test suite passing 8 out of 8 tests, comprehensive scientific documentation, and clean formatting without unwanted cache or temporary files.
- **Submission Deliverables**: Ready-to-submit publication-grade PDF report (`SSP_Assignment1_Q6_Report.pdf`, 16 pages), LaTeX source package (`latex_report/`), academic Markdown report (`REPORT.md`), and GitHub repository presentation (`README.md`).

---

## 2. Physics Explained in Simple Terms

### Why Normal Conductors Cannot Explain Superconductors
A normal metal (like copper or silver) has electrical resistance because moving electrons collide with vibrating lattice atoms and impurities. If you cool an ordinary conductor so its resistance becomes hypothetically zero (a "perfect conductor"), Faraday's law of electromagnetic induction states:
$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t} \implies \frac{\partial \mathbf{B}}{\partial t} = \mathbf{0}$$
This means a perfect conductor simply **freezes** whatever magnetic flux was inside it. If cooled in a magnetic field, the field remains trapped inside.

### The Meissner Effect
In 1933, Walther Meissner and Robert Ochsenfeld discovered that real superconductors do not just freeze flux—they **actively expel** any magnetic field from their interior when cooled below their critical temperature $T_c$:
$$\mathbf{B}_{\text{interior}} = \mathbf{0}$$
Superconductors are therefore **perfect diamagnets** ($\chi = -1$). This active expulsion occurs whether the magnetic field is applied after cooling or before cooling.

### The London Explanation (1935)
Brothers Fritz and Heinz London explained that below $T_c$, a fraction of electrons form a resistanceless "superfluid" (Cooper pairs). When an external magnetic field is applied:
1. The field induces circulating surface screening currents (**supercurrents**, $\mathbf{J}_s$).
2. By Lenz's law, these currents create their own internal magnetic field that exactly cancels the applied external field inside the bulk.
3. The screening is not instantaneous at the microscopic surface; instead, the field decays exponentially over a characteristic skin depth called the **London Penetration Depth** ($\lambda_L$):
   $$\lambda_L = \sqrt{\frac{m}{\mu_0 n_s e^2}}$$
   For typical metals (Niobium, Lead, Aluminium), $\lambda_L$ is between **20 nm and 200 nm**.

### How Temperature Changes Penetration
As temperature $T$ rises toward $T_c$, thermal energy breaks Cooper pairs apart into normal electrons. The density of superconducting electrons $n_s(T)$ drops:
$$n_s(T) = n_0 \left[1 - \left(\frac{T}{T_c}\right)^4\right]$$
Because $\lambda_L \propto 1/\sqrt{n_s}$, the penetration depth **grows larger** as temperature increases:
$$\lambda(T) = \frac{\lambda_0}{\sqrt{1 - (T/T_c)^4}}$$
When $T \ge T_c$, $n_s \to 0$ and $\lambda \to \infty$. The screening currents vanish, and the external magnetic field penetrates the material completely (normal metallic state).

---

## 3. How the Simulation Works

### Algorithmic Pipeline
1. **Parameter Resolution**:
   - The user selects a material or inputs custom values ($T_c$, $\lambda_0$).
   - Current temperature $T$ is used in the Gorter–Casimir formula to compute $\lambda(T)$. If $T \ge T_c$, $\lambda = \infty$ is flagged.
2. **Dimension Ratios**:
   - The ratio of characteristic sample dimension to penetration depth ($d/\lambda$ for slab, $R/\lambda$ for cylinder) is computed to assess screening strength:
     - **Strong screening** ($d/\lambda > 10$): Field drops virtually to zero in the interior.
     - **Partial penetration** ($2 < d/\lambda < 10$): Field decays but penetrates noticeable depth.
     - **Weak screening** ($d/\lambda < 2$): Field penetrates through the bulk.
3. **Geometry-Specific Equations**:
   - **Slab of thickness $d$**:
     $$B(x) = B_0 \frac{\cosh(x/\lambda)}{\cosh(d/2\lambda)}$$
   - **Cylinder of radius $R$**:
     $$B(r) = B_0 \frac{I_0(r/\lambda)}{I_0(R/\lambda)}$$
     Exterior field line deflection uses exact 2D magnetic dipole response.
   - **Rectangular cross-section ($a \times b$)**:
     $$B(x,y) \approx B_0 \left[\frac{\cosh(x/\lambda)}{\cosh(a/2\lambda)}\right] \cdot \left[\frac{\cosh(y/\lambda)}{\cosh(b/2\lambda)}\right]$$
4. **Overflow Protection**:
   - If $d/(2\lambda) > 500$ or $R/\lambda > 500$, raw calls to $\cosh$ or $I_0$ would overflow double-precision floats to `inf`.
   - The engine automatically switches to logarithmic asymptotic expansions ($\exp(u - v)$ or $\sqrt{v/u}\exp(u-v)$), guaranteeing numerical stability.
5. **Interactive Visualization**:
   - Matplotlib renders 2D contour maps with `RdBu_r` colour schemes, vector streamplots showing field expulsion, and 1D line graphs comparing profiles against ideal exponential decay $e^{-x/\lambda}$.

---

## 4. File-by-File Directory Reference

Every file in the repository serves a distinct, necessary role:

| Filename / Directory | Purpose |
|---|---|
| `latex_report/` | **Complete standalone LaTeX source folder**. Contains `report.tex` (the complete report in native LaTeX) and `figures/` (all figures utilized by the document). Can be built cleanly on any standard TeX distribution. |
| `latex_report/report.tex` | **Master LaTeX document source**. Defines the title page, table of contents, mathematical derivations using native `amsmath` environments (`equation`, `align`), genuine figure inclusions, tables, and academic citations. |
| `SSP_Assignment1_Q6_Report.pdf` | **Final submission-ready PDF report** (16 pages, 2.1 MB). Generated directly by compiling `latex_report/report.tex`. |
| `london_physics.py` | **Core physics engine**. Contains physical constants, material library (Nb, Pb, Al, Sn, Hg, YBCO), Gorter–Casimir temperature function, 1D analytical profiles, 2D vector/scalar field grid generators, and comparison functions. Zero UI dependencies. |
| `app.py` | **Interactive Streamlit web application**. Houses the user interface, sidebar parameter inputs, 6 tabs (2D visualization, 1D profiles, temperature dependence, geometry comparison, parameter study, theory), reactive recomputation, and Matplotlib plotting pipelines. |
| `generate_figures.py` | **Batch plotting script**. Generates all 11 publication-grade PNG diagrams into the `figures/` directory. Useful for offline inspection and building documents without launching the browser UI. |
| `test_suite.py` | **Automated test suite**. Runs 8 unit and physical consistency tests validating boundary conditions, asymptotic screening, spatial symmetry, temperature divergence, and grid dimensions. |
| `REPORT.md` | **Academic report in Markdown format**. Complete LaTeX-formatted technical report covering executive summary, derivations, numerical methods, results, limitations, and citations. |
| `README.md` | **GitHub repository front page**. Visually appealing project documentation with badges, screenshots, feature overview, quickstart instructions, and scientific insights. |
| `PROJECT_GUIDE.md` | **This complete project guide**. Explains the physics, simulation inner workings, file descriptions, workflows, and troubleshooting. |
| `requirements.txt` | **Dependencies file**. Specifies required Python packages (`numpy`, `scipy`, `matplotlib`, `streamlit`, `pytest`). |
| `.gitignore` | **Git exclusion rules**. Prevents temporary files, Python `__pycache__`, OS artifacts (`.DS_Store`), and virtual environments from cluttering the repository. |
| `Assignment-1.pdf` | **Original assignment brief**. Contains the problem statement and grading criteria for Question 6. |
| `figures/` | **Directory of generated figures**. Contains all high-resolution PNG plots, 2D field maps, 1D profile graphs, and the UI overview capture (`app_interface_overview.png`). |

---

## 5. LaTeX Report Compilation Instructions

The LaTeX report is fully self-contained inside `latex_report/`.

### 5.1 Using Tectonic (Recommended, Modern & Zero-Config)
```bash
cd "/Users/sameerchoudhary/Desktop/SSP Assignment/latex_report"
tectonic report.tex
```
This automatically resolves any required packages and produces `report.pdf`.

### 5.2 Using Traditional pdflatex or latexmk
```bash
cd "/Users/sameerchoudhary/Desktop/SSP Assignment/latex_report"
pdflatex report.tex
pdflatex report.tex  # Second run to resolve cross-references and Table of Contents
```
Or via latexmk:
```bash
latexmk -pdf report.tex
```

---

## 6. Installation, Execution & Workflows

### 6.1 Environment Setup
Open your terminal and navigate to the project directory:
```bash
cd "/Users/sameerchoudhary/Desktop/SSP Assignment"
```

Activate or create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 6.2 Running the Interactive Web App
Launch the Streamlit app:
```bash
streamlit run app.py
```
Open your web browser at:
```
http://localhost:8501
```

### 6.3 Running the Test Suite
Verify that all numerical and physical checks pass:
```bash
python3 test_suite.py
```
Expected output:
```plaintext
Running automated test suite...
ALL TESTS PASSED SUCCESSFULLY (8/8)!
```

### 6.4 Regenerating Figures
If you adjust physics parameters in `generate_figures.py` and wish to rebuild all 11 plots:
```bash
python3 generate_figures.py
```

---

## 7. Version History & Updates

- **v1.2.0 (Current Release)**:
  - **Native LaTeX Report Architecture**: Replaced separate image-rendered equations with clean native LaTeX mathematical typesetting (`amsmath` environments: `equation`, `align`).
  - **Unwanted Assets Cleaned**: Removed the `equations_rendered/` folder and legacy python PDF builder.
  - **Dedicated LaTeX Package**: Created `latex_report/` containing `report.tex` and a bundled `figures/` folder for standalone compilation.
  - **Master PDF**: Generated `SSP_Assignment1_Q6_Report.pdf` (16 pages) directly from LaTeX. Verified all equations, symbols, subscripts, superscripts, fractions, and vector notation render properly without clipping.
- **v1.1.0**:
  - Updated institutional details: IIT Hyderabad, Department of Physics, Course Instructor Prof. Arabinda Haldar.
  - Formatted team members list with Sameer Choudhary* placed first.
- **v1.0.0**:
  - Initial implementation of the London physics engine, Streamlit interface, and automated test suite.
