# Search and Matching — Teaching Package

Companion materials for the paper *"An Interactive Introduction to Search and
Matching Models: A Large-Firm Approach for Undergraduate Teaching"* by Jose
Silva.

The package contains a self-contained teaching paper, an interactive Python
simulator that runs in Google Colab, and the source code that generates all
the figures in the paper.

---

## Contents

```
search_matching_package/
├── README.md                              <-- this file
├── index.html                             <-- interactive teaching webpage (NEW!)
├── search_matching_teaching.pdf           <-- the teaching paper (PDF)
├── search_matching_teaching.tex           <-- LaTeX source of the paper
├── slides.pdf                             <-- lecture slides (Beamer, 16:9)
├── slides.tex                             <-- LaTeX source of the slides
├── search_matching_simulator.ipynb        <-- Google Colab notebook
├── search_matching_simulator.py           <-- plain-Python version of the simulator
├── make_figures.py                        <-- script that generates all the figures
└── figures/                               <-- PDF + PNG of all five figures
    ├── fig_equilibrium.{pdf,png}          <-- WC ∩ JC equilibrium
    ├── fig_beveridge.{pdf,png}            <-- Beveridge curve
    ├── fig_productivity_shock.{pdf,png}   <-- comparative statics: A ↑
    ├── fig_ui_shock.{pdf,png}             <-- comparative statics: b ↑
    └── fig_interface.{pdf,png}            <-- mockup of the Colab interface
```

---

## Quick start

### Open the interactive webpage

The fastest way to explore the material is `index.html`. It contains the full
paper in browser-readable form, all five figures, and a **live simulator** that
runs the model directly in your browser via Pyodide — no Python installation
needed. Just double-click `index.html` to open it (works best in a recent
Chrome, Firefox, or Safari with internet access; first load takes a few
seconds while Python and SciPy are downloaded into the browser).

You can also host this file on any static-site service (GitHub Pages, Netlify,
your university's web folder) and share a single URL with students.

### Read the paper

Open `search_matching_teaching.pdf`. It is an 18-page teaching paper organized as:

- **Body (Sections 1–13):** environment, matching function, firms, JC, wage
  curve, equilibrium as the WC ∩ JC intersection, Beveridge curve, two worked
  comparative-statics examples (productivity shock and unemployment
  insurance), the interactive notebook, suggested labs, policy applications,
  connections to the literature, conclusion.
- **Appendix A:** derivation of the job creation condition from the firm's
  static profit-maximization problem.
- **Appendix B:** derivation of the wage equation from Nash bargaining (logs,
  differentiate, solve).
- **Appendix C:** calibration of the benchmark to U.S.\ data.
- **Appendix D:** documentation of the companion notebook (slider mapping +
  core code).

### Use the lecture slides

`slides.pdf` is a 24-slide Beamer deck (16:9 aspect ratio) that mirrors the
paper and uses the same five figures. Suitable for a 50-minute lecture. To
recompile after edits:

```bash
pdflatex slides.tex
pdflatex slides.tex   # second pass for the table of contents
```

The slides reference figures from `figures/`, so keep that directory
alongside the `.tex` file.

### Run the interactive simulator

The recommended way is Google Colab (no installation needed):

1. Go to <https://colab.research.google.com>.
2. Click **File → Upload notebook** and pick `search_matching_simulator.ipynb`.
3. Run the single code cell. Sliders and plots appear inline.

Alternatively, in a local Jupyter environment:

```bash
pip install numpy scipy matplotlib ipywidgets
jupyter notebook search_matching_simulator.ipynb
```

If you prefer a plain script, `search_matching_simulator.py` contains the same
code without the notebook wrapping.

### Re-generate the figures

The five figures in the paper are not screenshots — they are produced by
`make_figures.py` from the actual model code at the benchmark calibration. To
re-render them (e.g. after changing the calibration):

```bash
pip install numpy scipy matplotlib
python make_figures.py
```

This writes `.pdf` and `.png` versions of every figure into `figures/`.

### Re-compile the paper

The LaTeX source uses standard packages (`amsmath`, `booktabs`, `tcolorbox`,
`listings`, `hyperref`, ...). With a working TeX Live distribution:

```bash
pdflatex search_matching_teaching.tex
pdflatex search_matching_teaching.tex   # second pass for cross-references
```

The figures are pulled from `figures/` via `\includegraphics`.

---

## The model in one paragraph

A representative large firm employs many workers and chooses how many
vacancies to post. Matches between unemployed workers and vacancies are
created by a Cobb–Douglas matching function `M(u,v) = φ u^(1-α) v^α`. Filled
jobs separate exogenously at rate `s`. Firms maximize profits, which gives
the **job creation curve**: `A − w = sc / q(θ)`. Wages are determined by
Nash bargaining, which gives the **wage curve**: `w = (1−β)b + β(A + cθ)`.
**Equilibrium** is the unique tightness `θ*` at which WC = JC. Steady-state
unemployment is `u* = s / (s + p(θ*))`, and the resulting `(u*, v*)` pair
sits on the **Beveridge curve**.

## Benchmark calibration

| Parameter | Symbol | Value | Description |
|---|---|---|---|
| `s` | $s$ | 0.035 | Job separation rate |
| `c` | $c$ | 0.12 | Vacancy cost |
| `A` | $A$ | 1.00 | Productivity per worker |
| `b` | $b$ | 0.41 | Flow value of unemployment |
| `beta` | $\beta$ | 0.879 | Worker bargaining power |
| `phi` | $\phi$ | 0.754 | Matching efficiency |
| `alpha` | $\alpha$ | 0.50 | Vacancy elasticity in matching |

At these parameters the equilibrium is approximately
`θ* ≈ 0.635`, `w* ≈ 0.996`, `p* ≈ 0.601`, `q* ≈ 0.946`, `u* ≈ 0.055`,
`v* ≈ 0.035`.

---

## Citation

If you use these materials, please cite:

> Silva, J. (2026). *An Interactive Introduction to Search and Matching
> Models: A Large-Firm Approach for Undergraduate Teaching.*

## License

You are free to use, modify, and redistribute these materials for teaching
purposes.
