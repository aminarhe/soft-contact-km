# soft-contact-km
Mathematical Modeling Capstone Project: a bubble gripper (inflated elastic membrane)
pressed onto a rigid object, building on the kinematic-match (KM) method of
Agüero et al. (2022), *Impact of a rigid sphere onto an elastic membrane*.

## Layout

```
figures/   scripts for the write-up figures
plots/     generated PNGs (same names as the plots/ folder in Overleaf)
```

| Script | Output |
|---|---|
| `figures/fig_variables.py` | `plots/fig_variables.png`: set-up and variables |
| `figures/fig_curvature.py` | `plots/fig_curvature.png`: pressure and curvature (1D piece) |
| `figures/fig_two_curvatures.py` | `plots/fig_two_curvatures.png`: curvature in two directions |

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy matplotlib
python figures/fig_variables.py
python figures/fig_curvature.py
python figures/fig_two_curvatures.py
```

Scripts can be run from any folder; outputs always go to `plots/`.
