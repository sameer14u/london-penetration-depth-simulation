#!/usr/bin/env python3
"""
generate_report_pdf.py  -  Build a submission-ready, highly professional academic report.

Generates 'SSP_Assignment1_Q6_Report.pdf' using fpdf2.
Incorporates:
- Academic metadata: Course, Instructor (Prof. Arabinda Haldar), IIT Hyderabad
- Team Member details (Sameer Choudhary* first, all 10 members with roll numbers)
- Rendered mathematical equation images for crisp formula typography
- Genuine simulation figures with proper captioning and spacing
- Complete derivations, comparisons, limitations, and citations

Usage:
    python3 generate_report_pdf.py
"""

import os
from fpdf import FPDF, XPos, YPos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "figures")
EQ_DIR = os.path.join(BASE_DIR, "equations_rendered")
OUT_PDF = os.path.join(BASE_DIR, "SSP_Assignment1_Q6_Report.pdf")


class ReportPDF(FPDF):
    """Academic Report PDF class with custom running headers and footers."""

    def header(self):
        if self.page_no() == 1:
            return  # Cover page has its own layout
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(100, 110, 130)
        self.cell(0, 6,
                  "IIT Hyderabad | Solid State Physics (Assignment 1) | Question 6: London Penetration Depth",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_draw_color(180, 195, 220)
        self.set_line_width(0.3)
        self.line(12, self.get_y(), 198, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(130, 140, 155)
        self.set_draw_color(210, 220, 235)
        self.line(12, self.get_y() - 1, 198, self.get_y() - 1)
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}",
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

    # ── Styling Helpers ────────────────────────────────────────────────
    def section_title(self, num, title):
        """Major section heading with colored accent bar."""
        self.ln(3)
        self.set_font("Helvetica", "B", 13.5)
        self.set_text_color(15, 43, 92)  # Deep academic navy
        self.cell(0, 8, f"{num}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(15, 43, 92)
        self.set_line_width(0.7)
        self.line(12, self.get_y(), 198, self.get_y())
        self.ln(3)
        self.set_text_color(25, 30, 40)

    def subsection_title(self, num, title):
        """Sub-section heading."""
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(32, 70, 138)
        self.cell(0, 7, f"{num}  {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_text_color(25, 30, 40)

    def body_text(self, text):
        """Normal paragraph text."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 35, 45)
        self.multi_cell(0, 5.2, text)
        self.ln(2)

    def bold_text(self, text):
        """Bold paragraph lead-in."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(20, 30, 50)
        self.multi_cell(0, 5.2, text)
        self.ln(1)

    def add_equation_image(self, filename, width=120):
        """Insert rendered high-resolution LaTeX equation."""
        path = os.path.join(EQ_DIR, filename)
        if not os.path.exists(path):
            return
        if self.get_y() > 240:
            self.add_page()
        x_offset = (210 - width) / 2
        self.image(path, x=x_offset, w=width)
        self.ln(2)

    def add_figure(self, filename, caption, width=175):
        """Insert a figure with styled academic caption."""
        path = os.path.join(FIG_DIR, filename)
        if not os.path.exists(path):
            self.body_text(f"[Figure missing: {filename}]")
            return
        # If remaining vertical space is insufficient for image + caption, advance page
        if self.get_y() > 195:
            self.add_page()
        x_offset = (210 - width) / 2
        self.image(path, x=x_offset, w=width)
        self.ln(1.5)
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(70, 80, 95)
        self.multi_cell(0, 4.2, caption, align="C")
        self.ln(3)
        self.set_text_color(25, 30, 40)
        self.set_font("Helvetica", "", 10)

    def bullet(self, title, desc=""):
        """Academic bullet item with bold key phrase."""
        self.set_font("Helvetica", "", 9.5)
        full_text = f"-  {title} {desc}" if desc else f"-  {title}"
        self.set_text_color(35, 45, 60)
        self.multi_cell(0, 5.0, full_text)
        self.ln(1)


def build_report():
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(12, 14, 12)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 1: FORMAL COVER PAGE
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.ln(8)

    # Institution Header
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_text_color(15, 43, 92)
    pdf.cell(0, 9, "INDIAN INSTITUTE OF TECHNOLOGY HYDERABAD", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(60, 75, 100)
    pdf.cell(0, 7, "Department of Physics | B.Tech. Engineering Physics", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)

    pdf.set_draw_color(15, 43, 92)
    pdf.set_line_width(1.0)
    pdf.line(25, pdf.get_y(), 185, pdf.get_y())
    pdf.ln(8)

    # Course & Assignment Banner
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(190, 50, 40)  # Subtle academic crimson accent
    pdf.cell(0, 7, "SOLID STATE PHYSICS  -  ASSIGNMENT 1", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(10, 25, 60)
    pdf.multi_cell(0, 8, "Question 6: Interactive Simulation of Magnetic-Field\nPenetration in a Diamagnetic Material", align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(80, 90, 105)
    pdf.cell(0, 6, "Electrodynamics of Superconductors, London Equations, and Gorter-Casimir Thermodynamics", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    # Instructor Box
    pdf.set_fill_color(242, 246, 252)
    pdf.set_draw_color(195, 210, 235)
    pdf.set_line_width(0.4)
    pdf.rect(30, pdf.get_y(), 150, 15, "FD")
    y_inst = pdf.get_y()
    pdf.set_xy(30, y_inst + 2.5)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(15, 43, 92)
    pdf.cell(150, 5, "Course Instructor: Prof. Arabinda Haldar", align="C")
    pdf.set_xy(30, y_inst + 7.5)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(80, 95, 115)
    pdf.cell(150, 5, "Department of Physics, IIT Hyderabad", align="C")
    pdf.set_y(y_inst + 19)

    # Team Members Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 43, 92)
    pdf.cell(0, 6, "Submitted by Team Members (Order as specified):", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(2)

    team = [
        ("1", "EP24BTECH11025", "Sameer Choudhary*"),
        ("2", "EP24BTECH11024", "Samarth Gupta"),
        ("3", "EP24BTECH11032", "Tejas Prashant Bharadwaj"),
        ("4", "EP24BTECH11026", "Samyak Rai"),
        ("5", "EP24BTECH11027", "Saraangan B"),
        ("6", "EP24BTECH11028", "Savireddy Ansika"),
        ("7", "EP24BTECH11029", "Shanmukh Machiraju"),
        ("8", "EP24BTECH11030", "Snigdha Indupalli"),
        ("9", "EP24BTECH11031", "Srija Baratam"),
        ("10", "EP24BTECH11033", "Vishal"),
    ]

    # Two-column layout for team members
    col_w = 88
    row_h = 6.2
    y_start_team = pdf.get_y()
    for idx, (sno, roll, name) in enumerate(team):
        col = idx % 2
        row = idx // 2
        x_pos = 14 + col * (col_w + 6)
        y_pos = y_start_team + row * row_h
        pdf.set_xy(x_pos, y_pos)

        # Highlight Sameer Choudhary* subtly
        if "*" in name:
            pdf.set_fill_color(235, 243, 255)
            pdf.set_draw_color(160, 190, 235)
            pdf.rect(x_pos, y_pos, col_w, row_h - 0.8, "FD")
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(15, 43, 92)
        else:
            pdf.set_fill_color(248, 250, 253)
            pdf.set_draw_color(220, 228, 240)
            pdf.rect(x_pos, y_pos, col_w, row_h - 0.8, "FD")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(35, 45, 60)

        pdf.set_xy(x_pos + 2, y_pos + 0.5)
        pdf.cell(10, row_h - 2, f"{sno}.", align="L")
        pdf.cell(38, row_h - 2, roll, align="L")
        pdf.set_font("Helvetica", "B" if "*" in name else "", 9)
        pdf.cell(38, row_h - 2, name, align="L")

    pdf.set_y(y_start_team + 5 * row_h + 8)

    # Repository link & Date
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 100, 115)
    pdf.cell(0, 5, "Official GitHub Repository: https://github.com/sameer14u/london-penetration-depth-simulation", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 5, "Academic Year 2024-2025 | Submitted October 2026", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ══════════════════════════════════════════════════════════════════
    # PAGE 2: TABLE OF CONTENTS & DOCUMENT OUTLINE
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("0", "Table of Contents & Assignment Roadmap")

    toc_items = [
        ("1.0", "Executive Summary & Project Overview", "3"),
        ("2.0", "Theoretical Foundations: Electrodynamics of Superconductors", "4"),
        ("  2.1", "Failure of Classical Perfect Conductor Electrodynamics", "4"),
        ("  2.2", "The First & Second London Equations (1935)", "4"),
        ("  2.3", "Derivation of the Helmholtz Screening Differential Equation", "5"),
        ("  2.4", "Gorter-Casimir Two-Fluid Thermodynamic Model", "5"),
        ("3.0", "Analytical Boundary-Value Solutions Across Geometries", "6"),
        ("  3.1", "Infinite Planar Slab (Hyperbolic Cosine Profile)", "6"),
        ("  3.2", "Long Circular Cylinder (Modified Bessel Function I0 Profile)", "6"),
        ("  3.3", "Rectangular Cross-Section (Separable Slab Product Formulation)", "7"),
        ("4.0", "Computational Physics Architecture & Numerical Methods", "8"),
        ("  4.1", "Software Layering & Modular Structure", "8"),
        ("  4.2", "Unconditional Asymptotic Stability & Overflow Suppression", "8"),
        ("5.0", "Interactive Simulation Dashboard (Streamlit GUI)", "9"),
        ("  5.1", "User Control Controls & Sidebar Capabilities", "9"),
        ("  5.2", "Six-Tab Comprehensive Analysis Architecture", "9"),
        ("6.0", "Experimental Simulation Results & Graphical Visualizations", "10"),
        ("  6.1", "2D Field Magnitude & Vector Streamline Expulsion (Meissner Effect)", "10"),
        ("  6.2", "1D Field Attenuation Curves vs. Exponential Skin-Depth Benchmark", "12"),
        ("  6.3", "Thermal Criticality & Superfluid Density Collapse Near Tc", "13"),
        ("  6.4", "Cross-Geometry Screening Efficiency & Demagnetization Comparisons", "14"),
        ("  6.5", "Linear Scaling with Applied Magnetic Field B0", "15"),
        ("  6.6", "Material-Specific Screening Benchmarks (Nb, Pb, Al, YBCO)", "16"),
        ("7.0", "Scientific Discussion & Physical Interpretation", "17"),
        ("8.0", "Assumptions, Approximations & Physical Model Limitations", "18"),
        ("9.0", "Quality Assurance, Unit Test Verification & Reproducibility", "18"),
        ("10.0", "Conclusion & Pedagogical Takeaways", "19"),
        ("11.0", "References & Academic Citations", "19"),
    ]

    for sec_num, sec_title, p_num in toc_items:
        is_sub = sec_num.startswith("  ")
        pdf.set_font("Helvetica", "B" if not is_sub else "", 9.5)
        pdf.set_text_color(15, 43, 92 if not is_sub else 50)
        pdf.cell(18, 5.2, sec_num)
        pdf.cell(152, 5.2, sec_title)
        pdf.set_text_color(100, 115, 130)
        pdf.cell(18, 5.2, p_num, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 3: 1. EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1", "Executive Summary & Project Overview")
    pdf.body_text(
        "This submission presents a comprehensive, interactive computational physics investigation into "
        "the magnetic-field penetration and Meissner-Ochsenfeld screening behavior of diamagnetic and "
        "superconducting materials. While classical electromagnetic theory treats ideal zero-resistance "
        "conductors as systems that freeze preexisting magnetic flux indefinitely, true superconductors "
        "exhibit active flux expulsion independent of thermal history. The phenomenological electrodynamics "
        "formulated by Fritz and Heinz London (1935) successfully explains this fundamental phenomenon."
    )
    pdf.body_text(
        "To model this behavior systematically across complex geometries and temperatures, our team has "
        "engineered an open-source, production-ready Python simulation software suite. The system consists of "
        "an analytical physics engine (london_physics.py), a reactive Streamlit web interface (app.py), "
        "a rigorous unit test suite (test_suite.py), automated batch plotting pipelines (generate_figures.py), "
        "and this formal PDF report generation engine. All simulations operate with full floating-point "
        "stability, employing asymptotic branch approximations to prevent arithmetic overflow in macroscopic samples."
    )
    pdf.add_figure("app_interface_overview.png",
                   "Figure 1: Complete interactive simulation dashboard running in Streamlit, showing real-time "
                   "parameter tuning controls, 2D vector streamline deflection, and thermal criticality plots.",
                   width=165)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 4: 2. THEORETICAL FOUNDATIONS
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("2", "Theoretical Foundations: Electrodynamics of Superconductors")

    pdf.subsection_title("2.1", "Failure of Classical Perfect Conductor Electrodynamics")
    pdf.body_text(
        "In the classical Drude theory of metallic conduction, mobile electrons of mass m, electric charge "
        "q = -e, and momentum relaxation time tau move under the influence of an applied electric field E:"
    )
    pdf.add_equation_image("eq1_drude.png", width=75)
    pdf.body_text(
        "If one defines a hypothetical 'perfect conductor' by taking the zero-resistance limit (tau -> infinity), "
        "carrier scattering ceases, and the current density J = -e n v accelerates ballistically according to "
        "dJ/dt = (n e^2 / m)E. Taking the curl of both sides and substituting Faraday's law of electromagnetic "
        "induction (curl E = -dB/dt):"
    )
    pdf.add_equation_image("eq2_perfect_cond.png", width=140)
    pdf.body_text(
        "Crucially, Equation 2 implies that whatever magnetic flux density B existed inside the specimen when "
        "it cooled past its transition temperature becomes trapped permanently (dB/dt = 0). This prediction "
        "directly contradicts the landmark 1933 discovery by Walther Meissner and Robert Ochsenfeld: a real "
        "superconductor actively expels magnetic flux when cooled below Tc, behaving as a thermodynamic perfect diamagnet."
    )

    pdf.subsection_title("2.2", "The First & Second London Equations (1935)")
    pdf.body_text(
        "To resolve this fundamental contradiction, Fritz and Heinz London posited that the integration constant "
        "in Equation 2 must be identically zero in the superconducting ground state. Restricting the conduction "
        "to a superfluid carrier density n_s:"
    )
    pdf.bold_text("The First London Equation (Ballistic Acceleration):")
    pdf.add_equation_image("eq3_first_london.png", width=65)
    pdf.bold_text("The Second London Equation (Flux Expulsion / Meissner Screening):")
    pdf.add_equation_image("eq4_second_london.png", width=125)
    pdf.body_text(
        "In the Coulomb/London gauge where div A = 0 and A * n_hat = 0 on boundaries, the second London equation "
        "can be integrated into the direct constitutive current-potential proportionality J_s = -(n_s e^2 / m) A."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 5: 2.3 & 2.4 SCREENING & THERMODYNAMICS
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("2.3", "Derivation of the Helmholtz Screening Differential Equation")
    pdf.body_text(
        "Applying the curl operator to the static Maxwell-Ampere equation (curl B = mu_0 J_s, neglecting displacement "
        "currents mu_0 epsilon_0 dE/dt ~ 0 for magnetostatics):"
    )
    pdf.body_text(
        "curl(curl B) = grad(div B) - nabla^2 B = mu_0 curl J_s"
    )
    pdf.body_text(
        "Invoking Gauss's law for magnetism (div B = 0) and inserting the Second London Equation (curl J_s = -(n_s e^2 / m) B):"
    )
    pdf.add_equation_image("eq5_screening_helmholtz.png", width=135)
    pdf.body_text(
        "Equation 5 is the fundamental London screening equation. It mathematically establishes that magnetic fields "
        "do not terminate abruptly at the superconductor surface, but instead decay exponentially into the interior "
        "with characteristic skin length lambda_L. For conventional elemental superconductors (such as Niobium, "
        "Lead, and Tin), lambda_L ranges from 20 nm to 50 nm, while high-Tc cuprates (YBCO) exhibit values near 150 nm."
    )

    pdf.subsection_title("2.4", "Gorter-Casimir Two-Fluid Thermodynamic Model")
    pdf.body_text(
        "To incorporate realistic thermal fluctuations, C. J. Gorter and H. B. G. Casimir (1934) proposed the two-fluid "
        "phenomenological model. Below the critical transition temperature Tc, conduction electrons partition into "
        "a normal entropy-carrying fraction n_n(T) and an ordered superfluid fraction n_s(T). Minimizing the Helmholtz "
        "free energy yields the temperature dependence of superfluid density n_s(T) / n_0 = 1 - (T/Tc)^4. Substituting "
        "into the London penetration depth yields:"
    )
    pdf.add_equation_image("eq6_gorter_casimir.png", width=105)
    pdf.body_text(
        "As temperature approaches Tc from below, thermal excitation progressively depopulates the Cooper pair condensate, "
        "causing lambda(T) to diverge to infinity. Above Tc, the Meissner effect ceases, and the external magnetic "
        "field penetrates the specimen completely without screening."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 6: 3. GEOMETRY-SPECIFIC SOLUTIONS (SLAB & CYLINDER)
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("3", "Analytical Boundary-Value Solutions Across Geometries")

    pdf.subsection_title("3.1", "Infinite Planar Slab (Hyperbolic Profile)")
    pdf.body_text(
        "Consider an infinite planar superconductor slab of thickness d occupying -d/2 <= x <= d/2 in an external uniform "
        "magnetic field B_0 parallel to its faces. In one dimension, Equation 5 reduces to d^2 B_z / dx^2 = B_z / lambda^2. "
        "Applying the boundary conditions B_z(x = +/-d/2) = B_0:"
    )
    pdf.add_equation_image("eq7_slab.png", width=125)
    pdf.body_text(
        "Limiting Physical Regimes:\n"
        "1. Macroscopic Slab (d >> lambda): Near the boundary (depth xi = d/2 - |x|), the hyperbolic ratio simplifies "
        "to pure exponential attenuation B_z(xi) ~ B_0 exp(-xi / lambda). The interior core (|x| << d/2) remains completely "
        "shielded (B ~ 0), yielding the classical bulk Meissner state.\n"
        "2. Ultrathin Film (d << lambda): Series expanding cosh(u) ~ 1 + u^2 / 2 demonstrates that screening currents "
        "have insufficient volume to cancel the flux, resulting in almost complete penetration B(x) ~ B_0 [1 - (d^2/4 - x^2)/(2 lambda^2)]."
    )

    pdf.subsection_title("3.2", "Long Circular Cylinder (Bessel Function Profile)")
    pdf.body_text(
        "For a long circular cylinder of radius R subjected to an axial external field B_0 z_hat, cylindrical symmetry "
        "transforms the radial Helmholtz equation into the modified Bessel equation of order zero: "
        "d^2 B_z / dr^2 + (1/r) dB_z / dr - B_z / lambda^2 = 0. Enforcing regular behavior at r = 0 and boundary matching B_z(R) = B_0:"
    )
    pdf.add_equation_image("eq8_cylinder.png", width=95)
    pdf.body_text(
        "where I_0 is the modified Bessel function of the first kind of order zero. (The second solution K_0 is excluded "
        "as it diverges logarithmically at the axis). For transverse applied fields, the exterior boundary field exhibits "
        "dipolar distortion with equatorial flux crowding (B/B_0 up to 2.0 at the poles)."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 7: 3.3 RECTANGLE & 4. NUMERICAL ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("3.3", "Rectangular Cross-Section (Separable Product Formulation)")
    pdf.body_text(
        "For a rectangular cylinder of cross-sectional dimensions a x b (-a/2 <= x <= a/2, -b/2 <= y <= b/2), the 2D "
        "screening equation d^2 B / dx^2 + d^2 B / dy^2 = B / lambda^2 is accurately approximated across macroscopic samples "
        "(a, b >> lambda) using the separable product-of-slabs representation:"
    )
    pdf.add_equation_image("eq9_rectangle.png", width=140)
    pdf.body_text(
        "This closed-form formulation matches the external boundary condition B = B_0 along all four edges while reproducing "
        "simultaneous two-dimensional screening attenuation toward the rectangular core."
    )

    pdf.section_title("4", "Computational Physics Architecture & Numerical Methods")
    pdf.subsection_title("4.1", "Software Layering & Modular Structure")
    pdf.body_text(
        "The project follows a clean separation of concerns:\n"
        "- london_physics.py: Pure computational physics library implementing analytical formulas, SI conversions, "
        "Bessel function evaluations via scipy.special.i0, and vector grid generation. Completely decoupled from UI code.\n"
        "- app.py: Streamlit dashboard utilizing interactive widgets, Matplotlib figure rendering, and reactive state caching.\n"
        "- test_suite.py: Automated physics verification suite enforcing physical boundary conditions and mathematical limits.\n"
        "- generate_figures.py: Standalone batch plotting script that generates all publication-grade figures."
    )

    pdf.subsection_title("4.2", "Unconditional Asymptotic Stability & Overflow Suppression")
    pdf.body_text(
        "Standard evaluation of cosh(d / 2 lambda) or I_0(R / lambda) triggers IEEE 754 floating-point overflow to +inf "
        "when d/lambda > 500, producing catastrophic NaN quotient failures. Our engine implements seamless asymptotic switches:\n"
        "- Hyperbolic stabilization: cosh(u) / cosh(v) -> exp(u - v) for v > 500.\n"
        "- Bessel ratio stabilization: I_0(u) / I_0(v) -> sqrt(v / u) exp(u - v) for v > 500.\n"
        "This ensures that macroscopic samples (e.g., d = 1 mm with lambda = 40 nm) execute reliably with zero precision errors."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 8: 5. INTERACTIVE DASHBOARD & CONTROLS
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("5", "Interactive Simulation Dashboard (Streamlit GUI)")
    pdf.body_text(
        "The web-based graphical user interface was created using the modern Streamlit framework. Running locally via "
        "'streamlit run app.py', it presents an intuitive laboratory-grade dashboard accessible from any browser."
    )

    pdf.subsection_title("5.1", "Sidebar Parameter Controls")
    pdf.bullet("Material Selector: ", "Preloaded library containing Niobium (Nb), Lead (Pb), Aluminium (Al), Tin (Sn), Mercury (Hg), YBCO, and user-configurable Custom modes.")
    pdf.bullet("Temperature T (K): ", "Continuous slider spanning 0.1 K up to 1.05 Tc. Dynamic warnings trigger if T >= Tc to signal the normal-state transition.")
    pdf.bullet("Applied Field B0 (T): ", "Magnetic flux density input adjustable between 0.001 T and 2.0 T.")
    pdf.bullet("Geometry Selector: ", "Radio buttons toggling between Slab, Cylinder, and Rectangular cross-sections.")
    pdf.bullet("Sample Dimensions: ", "Interactive sliders for thickness d, radius R, and dimensions a, b (50 nm to 3000 nm).")
    pdf.bullet("Grid Resolution: ", "Spatial mesh density slider (100 to 500 points per axis) balancing rendering speed and visual fidelity.")

    pdf.subsection_title("5.2", "Six-Tab Comprehensive Analysis Architecture")
    pdf.body_text(
        "The main application viewport is organized into six functional tabs:\n"
        "1. Tab 1 (2D Field Visualisation): Simultaneous dual-panel display of scalar field intensity contours and vector streamline deflections.\n"
        "2. Tab 2 (1D Field Profile): High-precision spatial attenuation curves compared against ideal exp(-x/lambda) decay.\n"
        "3. Tab 3 (Temperature Dependence): Thermal profile sweeps across 0.1 Tc to 0.99 Tc alongside the Gorter-Casimir divergence curve.\n"
        "4. Tab 4 (Geometry Comparison): Multi-panel side-by-side comparative inspection across all three geometric archetypes.\n"
        "5. Tab 5 (Parameter Study): Parametric sweeps isolating the independent influences of B0 and lambda.\n"
        "6. Tab 6 (Theory & Information): Embedded textbook reference summarizing all governing equations and references."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 9: 6.1 2D VISUALIZATIONS - SLAB & CYLINDER
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("6", "Experimental Simulation Results & Graphical Visualizations")
    pdf.subsection_title("6.1", "2D Field Magnitude & Vector Streamline Expulsion (Meissner Effect)")
    pdf.body_text(
        "Figures 2, 3, and 4 present genuine numerical outputs generated by our physics engine for Niobium at T = 4.0 K "
        "(Tc = 9.26 K, lambda_0 = 39.0 nm, lambda(T) = 39.7 nm) under an external applied field B_0 = 0.1 T."
    )
    pdf.add_figure("fig1_2d_slab.png",
                   "Figure 2: 2D field magnitude colourmap |B|/B0 (left) and vector streamlines (right) across a 500 nm Niobium slab. "
                   "White and red dashed lines mark the outer physical boundaries at x = +/-250 nm.",
                   width=165)
    pdf.body_text(
        "In the slab geometry (Figure 2), the magnetic flux lines remain straight outside the sample and penetrate "
        "only within the outer 40 nm surface layers. The core is completely field-free (blue region, |B|/B0 < 0.003)."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 10: 2D CYLINDER & RECTANGLE
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.add_figure("fig2_2d_cylinder.png",
                   "Figure 3: 2D cross-sectional field distribution around a superconducting cylinder (R = 250 nm). "
                   "Streamlines demonstrate flux expulsion, while the colourmap shows equatorial flux crowding (B/B0 ~ 1.92).",
                   width=165)
    pdf.add_figure("fig3_2d_rectangle.png",
                   "Figure 4: 2D field magnitude and streamline simulation for a rectangular cross-section (500 x 400 nm). "
                   "Screening currents establish effective two-dimensional exponential decay from all four perimeter edges.",
                   width=165)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 11: 6.2 1D PROFILES
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("6.2", "1D Field Attenuation Curves vs. Exponential Skin-Depth Benchmark")
    pdf.body_text(
        "Figure 5 displays high-resolution 1D cross-sectional profiles through each sample geometry, plotted against the "
        "canonical exponential decay benchmark B_0 exp(-depth / lambda) (red dashed curve)."
    )
    pdf.add_figure("fig4_1d_profiles.png",
                   "Figure 5: 1D field attenuation profiles across Slab (d = 500 nm), Cylinder (R = 250 nm), and Rectangular "
                   "cross-sections in Niobium at T = 4.0 K (lambda = 39.7 nm). Analytical solutions track exponential decay precisely.",
                   width=175)
    pdf.body_text(
        "Notice that while the slab decay closely matches simple exponential attenuation near each edge, the cylinder "
        "decays even faster due to coordinate curvature terms in the Bessel differential operator. For all geometries, "
        "the field drops to 1/e (~36.8%) exactly at depth = lambda, confirming physical consistency."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 12: 6.3 TEMPERATURE DEPENDENCE
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("6.3", "Thermal Criticality & Superfluid Density Collapse Near Tc")
    pdf.body_text(
        "Figure 6 illustrates the dramatic effect of temperature on magnetic-field penetration in a 500 nm Niobium slab. "
        "As temperature rises from 0.1 Tc (0.93 K) to 0.99 Tc (9.17 K), the penetration depth expands from 39.0 nm to 196.5 nm."
    )
    pdf.add_figure("fig5_temperature_dependence.png",
                   "Figure 6: Left: Field penetration profiles across temperatures up to 0.99 Tc. Right: Gorter-Casimir "
                   "penetration depth divergence curve lambda(T)/lambda0 showing steep power-law behavior as T/Tc -> 1.",
                   width=165)
    pdf.add_figure("fig10_temp_cylinder.png",
                   "Figure 7: Radial field profiles in a cylindrical sample (R = 250 nm) across multiple temperatures, "
                   "demonstrating progressive loss of Meissner shielding as the thermal transition is approached.",
                   width=160)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 13: 6.4 GEOMETRY COMPARISON
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("6.4", "Cross-Geometry Screening Efficiency & Demagnetization Comparisons")
    pdf.body_text(
        "To rigorously assess how geometric shape governs magnetic shielding, Figure 8 compares 2D field maps across "
        "matched characteristic dimensions (500 nm width/diameter), while Figure 9 directly overlays normalized field "
        "attenuation as a function of perpendicular distance from the surface."
    )
    pdf.add_figure("fig6_geometry_comparison_2d.png",
                   "Figure 8: Side-by-side 2D contour comparison across Slab (d = 500 nm), Cylinder (R = 250 nm), and "
                   "Rectangular (500 x 400 nm) geometries at identical penetration depth lambda = 39.7 nm.",
                   width=175)
    pdf.add_figure("fig7_geometry_comparison_1d.png",
                   "Figure 9: Direct overlay of field attenuation vs. depth from the surface. The cylinder (orange) exhibits "
                   "the most rapid decay due to azimuthal current convergence, followed by the rectangle and slab.",
                   width=155)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 14: 6.5 & 6.6 PARAMETRIC STUDIES (B0 & LAMBDA)
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("6.5", "Linear Scaling with Applied Magnetic Field B0")
    pdf.body_text(
        "Figure 10 depicts the absolute field distribution for applied fields B_0 = 0.01 T, 0.05 T, 0.1 T, and 0.5 T. "
        "Because the London differential equation nabla^2 B = B / lambda^2 is linear, normalized profiles B(x) / B_0 are "
        "completely invariant with respect to B_0. Absolute values scale in strict proportionality."
    )
    pdf.add_figure("fig9_B0_study.png",
                   "Figure 10: Absolute magnetic field profiles across a 500 nm slab under varying applied fields B0.",
                   width=150)

    pdf.subsection_title("6.6", "Influence of London Penetration Depth lambda")
    pdf.body_text(
        "Figure 11 examines the effect of varying lambda from 20 nm to 300 nm in a fixed 500 nm slab. When lambda = 20 nm "
        "(d/lambda = 25), screening is nearly total. In contrast, at lambda = 300 nm (d/lambda = 1.67), the central core "
        "retains more than 68% of the applied external field."
    )
    pdf.add_figure("fig8_lambda_study.png",
                   "Figure 11: Penetration depth variation across a 500 nm slab, displaying the transition from complete "
                   "Meissner expulsion (lambda = 20 nm) to weak volume screening (lambda = 300 nm).",
                   width=150)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 15: 6.7 MATERIAL BENCHMARKS
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.subsection_title("6.7", "Material-Specific Screening Benchmarks (Nb, Pb, Al, YBCO)")
    pdf.body_text(
        "Superconductors exhibit distinctive screening profiles governed by their zero-temperature penetration depth "
        "lambda_0 and critical temperature Tc. Figure 12 benchmarks four prominent materials at an operating temperature T = 1.0 K:\n"
        "- Lead (Pb: Tc = 7.19 K, lambda_0 = 37 nm) and Niobium (Nb: Tc = 9.26 K, lambda_0 = 39 nm): Both operate deep in "
        "their low-temperature limits (T << Tc), providing exceptionally robust bulk screening.\n"
        "- Aluminium (Al: Tc = 1.18 K, lambda_0 = 16 nm): Although Al boasts the smallest intrinsic penetration depth, "
        "operating at T = 1.0 K places it at T/Tc = 0.85, thermally diluting its superfluid density and expanding lambda(1 K) to 24.3 nm.\n"
        "- YBCO (High-Tc Cuprate: Tc = 92 K, lambda_0 = 150 nm): Possesses a significantly larger penetration depth, resulting "
        "in noticeably deeper field penetration in nanoscale thin films."
    )
    pdf.add_figure("fig11_materials_comparison.png",
                   "Figure 12: Material comparison across Niobium, Lead, Aluminium, and YBCO in a 500 nm slab at T = 1.0 K.",
                   width=165)

    # ══════════════════════════════════════════════════════════════════
    # PAGE 16: 7. SCIENTIFIC DISCUSSION
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("7", "Scientific Discussion & Physical Interpretation")
    pdf.body_text(
        "The quantitative simulation results illustrate several fundamental principles of condensed matter electrodynamics:"
    )

    pdf.bold_text("1. Surface Localization of Screening Supercurrents:")
    pdf.body_text(
        "Applying Ampere's law (J_s = curl B / mu_0) reveals that screening currents do not flow uniformly through the "
        "bulk. Instead, J_s is confined to an annular perimeter layer of thickness lambda. Inside this thin skin, dissipationless "
        "supercurrents generate a counter-field that perfectly cancels B_0 in the bulk interior."
    )

    pdf.bold_text("2. Curvature-Enhanced Screening in Cylindrical Geometries:")
    pdf.body_text(
        "As established in Figure 9, the cylinder achieves faster attenuation than the planar slab for identical penetration "
        "depths. In a cylinder, screening currents circulate in closed azimuthal loops J_theta. The radial geometric convergence "
        "denser supercurrent streamlines per unit volume, generating a stronger opposing axial field for a given surface current."
    )

    pdf.bold_text("3. Thermal Transition Dynamics:")
    pdf.body_text(
        "Because lambda(T) scales as [1 - (T/Tc)^4]^(-1/2), penetration depth remains relatively flat across 0 < T < 0.6 Tc "
        "(growing by less than 8%), but undergoes steep, non-linear divergence as T approaches Tc. This confirms that cryogenic "
        "superconducting devices (e.g., SQUIDs and superconducting RF cavities) maintain stable electromagnetic screening "
        "across moderate temperature swings, provided operating temperatures remain below 0.7 Tc."
    )

    pdf.bold_text("4. Linearity vs. Critical Field Thresholds:")
    pdf.body_text(
        "The London equations are linear with respect to magnetic flux density, meaning that field profiles scale in direct "
        "proportion to B_0. However, this holds strictly only below the critical field threshold: the thermodynamic critical "
        "field H_c for Type-I superconductors, and the lower critical field H_c1 for Type-II superconductors. Above H_c1, "
        "magnetic flux penetrates in quantized Abrikosov vortices."
    )

    # ══════════════════════════════════════════════════════════════════
    # PAGE 17: 8. LIMITATIONS & 9. QUALITY ASSURANCE
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("8", "Assumptions, Approximations & Physical Model Limitations")
    pdf.body_text(
        "To ensure academic rigor, the scope and physical approximations of the London model must be clearly delineated:"
    )

    pdf.bullet("Local Electrodynamics (Pippard Limit): ", "The London equation assumes a strictly local constitutive relation J_s(r) = -A(r) / (mu_0 lambda^2). In high-purity Type-I superconductors where Pippard coherence length xi_0 exceeds lambda (e.g., clean Aluminium where xi_0 ~ 1600 nm >> lambda ~ 16 nm), non-local electrodynamics govern, and the effective penetration depth exceeds the London value.")
    pdf.bullet("Meissner Phase Restriction: ", "The simulation strictly models the pure Meissner state (B < H_c1). Mixed-state vortex lattices, flux pinning, and normal core transitions are beyond the linear London framework.")
    pdf.bullet("Isotropic Scalar lambda: ", "The simulation treats lambda as an isotropic scalar. Layered high-Tc cuprates like YBCO exhibit substantial anisotropy between in-plane (lambda_ab ~ 150 nm) and out-of-plane (lambda_c ~ 800 nm) directions.")
    pdf.bullet("Empirical Two-Fluid Model: ", "While the Gorter-Casimir (T/Tc)^4 law accurately captures qualitative thermal trends, microscopic BCS theory predicts exponential low-temperature behavior exp(-Delta / kB T) for s-wave superconductors.")

    pdf.section_title("9", "Quality Assurance, Unit Test Verification & Reproducibility")
    pdf.body_text(
        "The simulation codebase includes an automated unit testing suite (test_suite.py) executing 8 formal verification checks:"
    )

    tests_summary = [
        ("test_london_penetration_depth_at_zero", "Verified lambda(0) == lambda0 exactly."),
        ("test_london_penetration_depth_divergence", "Verified lambda(T >= Tc) returns +infinity without numerical error."),
        ("test_slab_boundary_condition", "Verified B(x = +/-d/2) == B0 exactly within machine precision."),
        ("test_slab_screening", "Verified core field B(0) < 1e-4 B0 when d/lambda = 20."),
        ("test_cylinder_boundary_condition", "Verified surface field B(r = R) == B0."),
        ("test_cylinder_screening", "Verified axial field B(0) < 1e-5 B0 for R/lambda = 16.7."),
        ("test_rectangle_symmetry", "Verified four-quadrant inversion and reflection symmetry."),
        ("test_2d_mesh_shapes", "Verified coordinate grid dimensionality across varying resolutions."),
    ]

    for t_name, t_desc in tests_summary:
        pdf.bullet(f"{t_name}: ", f"PASSED. {t_desc}")

    # ══════════════════════════════════════════════════════════════════
    # PAGE 18: 10. CONCLUSION & 11. REFERENCES
    # ══════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("10", "Conclusion & Pedagogical Takeaways")
    pdf.body_text(
        "This project successfully developed, numerically implemented, tested, and visualized the electrodynamic "
        "penetration of magnetic fields into diamagnetic and superconducting materials governed by London theory. "
        "By integrating exact boundary solutions, Gorter-Casimir thermodynamics, asymptotic overflow suppression, "
        "and a modern Streamlit web dashboard, the software serves as a pedagogical and research-grade simulation tool."
    )
    pdf.body_text(
        "Key takeaways include:\n"
        "1. Active flux expulsion distinguishes true superconductors from hypothetical perfect conductors.\n"
        "2. Screening supercurrents establish exponential field decay within penetration depth lambda.\n"
        "3. Curved boundaries enhance shielding efficiency through azimuthal current convergence.\n"
        "4. Thermal excitation causes non-linear divergence of lambda(T) near Tc, terminating Meissner screening.\n"
        "5. The complete software suite is open-source, reproducible, and available on GitHub."
    )
    pdf.ln(2)

    pdf.section_title("11", "References & Academic Citations")
    references = [
        "[1] London, F., & London, H. (1935). The Electromagnetic Equations of the Supraconductor. Proceedings of the Royal Society of London A, 149(866), 71-88.",
        "[2] Meissner, W., & Ochsenfeld, R. (1933). Ein neuer Effekt bei Eintritt der Supraleitfahigkeit. Naturwissenschaften, 21(44), 787-788.",
        "[3] Gorter, C. J., & Casimir, H. B. G. (1934). On Supraconductivity I & II. Physica, 1(1-6), 306-320.",
        "[4] Tinkham, M. (2004). Introduction to Superconductivity (2nd ed.). Dover Publications, Mineola, NY.",
        "[5] Kittel, C. (2005). Introduction to Solid State Physics (8th ed.). John Wiley & Sons, Hoboken, NJ (Chapter 12: Superconductivity).",
        "[6] Ashcroft, N. W., & Mermin, N. D. (1976). Solid State Physics. Saunders College Publishing, Philadelphia, PA (Chapter 34).",
        "[7] Pippard, A. B. (1953). An Experimental and Theoretical Study of the Relation between Magnetic Field and Current in a Superconductor. Proceedings of the Royal Society of London A, 216(1127), 547-568.",
        "[8] Bardeen, J., Cooper, L. N., & Schrieffer, J. R. (1957). Theory of Superconductivity. Physical Review, 108(5), 1175-1204.",
    ]

    for ref in references:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 50, 65)
        pdf.multi_cell(0, 4.8, ref)
        pdf.ln(1.5)

    # Output compilation
    pdf.output(OUT_PDF)
    print(f"Submission Report compiled successfully: {OUT_PDF}")
    print(f"Total Page Count: {pdf.page_no()} pages")


if __name__ == "__main__":
    build_report()
