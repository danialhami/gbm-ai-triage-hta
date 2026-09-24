# gbm-ai-triage-hta

Reference implementation and figure-generation code for:

> Hami, D. **Value-based operational thresholds for artificial intelligence MRI triage in glioblastoma.** *npj Digital Medicine* (submitted).

This repository contains the decision-analytic model underlying the paper's early health-technology-assessment (early-HTA) of AI-assisted MRI triage for glioblastoma pseudoprogression, restricted to the RANO 2.0-equivocal subset of surveillance scans. All reported base-case, scenario, and probabilistic-sensitivity results in the manuscript are reproduced exactly by the code below.

## Requirements

- Python 3.12
- NumPy 2.4
- SciPy 1.17
- Matplotlib

Install with:
```bash
pip install numpy scipy matplotlib
```

## Contents

| File | Reproduces |
|---|---|
| `figure1_frontier.py` | Figure 1 — cost-effectiveness frontier (NMB across AI sensitivity × specificity), base-case reimbursement scenario |
| `figure2_map.py` | Figure 2 — Maximum Acceptable Price (MAP) curves for the Optimized, Base-Case, and Decayed diagnostic performance profiles |
| `figure3_psa.py` | Figure 3 — probabilistic sensitivity analysis, 10,000-iteration Monte Carlo simulation (random seed 2026) |

Each script is self-contained and can be run independently:
```bash
python3 figure1_frontier.py
python3 figure2_map.py
python3 figure3_psa.py
```

Each produces a `.png` (preview) and a `.tiff` (300 dpi, print-ready) version of its figure in the working directory.

## Model summary

The core decision rule governing the AI arm's surgical-intervention probability among pseudoprogression patients is:

```
P(Surgery | PsP)_AI = P(Surgery | PsP)_SC × (1 − Specificity × Compliance)
```

i.e., the AI arm departs from the standard-care baseline only when the algorithm correctly identifies pseudoprogression *and* the clinician follows that recommendation; all other cases (AI error, or a correct call that is overridden) revert to the standard-care baseline rate. Base-case parameters (sensitivity, specificity, clinician compliance, procedure costs, health-state utilities, and Weibull survival parameters) are listed in Table 2 of the manuscript and reproduced as named constants at the top of each script.

Repeat-MRI cost savings are modelled under Option D: only AI-confirmed, compliant pseudoprogression cases forgo the scheduled confirmatory rescan.

Overall survival for QALY discounting is constructed by convolving the model's progression-free-survival and post-progression-survival Weibull curves (rather than using either curve alone), giving a mean overall survival of ≈1.63 years, consistent with the source trial.

## Reproduced headline results (base case)

- Non-therapeutic surgeries averted: 11.70 / 1,000 patients
- Incremental cost: −$467.61 per patient (full-cohort basis)
- Incremental QALYs: +0.000314
- Incremental Net Monetary Benefit: +$498.98 (WTP $100,000/QALY)
- Maximum Acceptable Price: $2,219 per scan (base-case profile)
- Probabilistic sensitivity analysis: cost-effective in 100% of 10,000 iterations

Scenario analyses (zero-reimbursement, false-negative-penalty threshold, automation-bias threshold) are described in the manuscript's Results and Discussion; their parameter settings can be reproduced by adjusting the `cpt_credit`, `fee`, and `mri_on` arguments in the model functions.

## License

Code released for reproducibility of the associated manuscript. Contact the author for reuse beyond that purpose.

## Contact

Danial Hami — danialhami@csu.edu.cn
