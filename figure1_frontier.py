import numpy as np
import matplotlib.pyplot as plt

# Base-case parameters (favorable scenario, as used in the manuscript's primary analysis)
EQUIVOCAL_RATE = 0.26
PSP_PREV = 1/3
SC_RATE = 0.216
BLENDED_COST = 0.4034*40661 + 0.5966*27442
MRI_COST = 1080.0
CPT_CREDIT, FEE = 400.0, 300.0
DEFICIT_RISK, DEFICIT_UTIL = 0.10, 0.17
DISC_YEARS = 1.5775  # validated discounted survival years
WTP = 100000
COMPLIANCE = 0.762

def nmb(sens, spec):
    p_ai = SC_RATE * (1 - spec*COMPLIANCE)
    surg = (SC_RATE - p_ai) * PSP_PREV * BLENDED_COST
    resolved = spec*COMPLIANCE*PSP_PREV
    mri = resolved * MRI_COST / (1.03**(1/12))**2
    margin = CPT_CREDIT - FEE
    dqaly = (SC_RATE - p_ai) * PSP_PREV * DEFICIT_RISK * DEFICIT_UTIL * DISC_YEARS
    return (dqaly*WTP + surg + mri + margin) * EQUIVOCAL_RATE

sens_r = np.linspace(0.60, 0.95, 80)
spec_r = np.linspace(0.50, 0.95, 80)
grid = np.array([[nmb(se, sp) for se in sens_r] for sp in spec_r])

fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=300)
c = ax.contourf(sens_r, spec_r, grid, levels=20, cmap='RdYlGn')
plt.colorbar(c, ax=ax, label='Incremental Net Monetary Benefit, full-cohort (USD)')
ax.scatter(0.85, 0.82, color='blue', marker='*', s=200, edgecolor='white', zorder=5,
           label=f'Base case (85% Se, 82% Sp; NMB=${nmb(0.85,0.82):.0f})')
ax.set_xlabel('AI Sensitivity'); ax.set_ylabel('AI Specificity')
# title removed -- belongs in the manuscript legend, not the figure canvas
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('Figure1_Frontier.tiff', dpi=300, format='tiff')
plt.savefig('Figure1_Frontier.png', dpi=300)
print("Figure 1 saved.")
