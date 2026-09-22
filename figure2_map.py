import numpy as np
import matplotlib.pyplot as plt

EQUIVOCAL_RATE, PSP_PREV, SC_RATE = 0.26, 1/3, 0.216
BLENDED_COST = 0.4034*40661 + 0.5966*27442
MRI_COST, COMPLIANCE, WTP = 1080.0, 0.762, 100000
DEFICIT_RISK, DEFICIT_UTIL, DISC_YEARS = 0.10, 0.17, 1.5775

def map_and_fixed_value(sens, spec):
    p_ai = SC_RATE * (1 - spec*COMPLIANCE)
    surg = (SC_RATE - p_ai) * PSP_PREV * BLENDED_COST
    resolved = spec*COMPLIANCE*PSP_PREV
    mri = resolved * MRI_COST / (1.03**(1/12))**2
    dqaly = (SC_RATE - p_ai) * PSP_PREV * DEFICIT_RISK * DEFICIT_UTIL * DISC_YEARS
    fixed_value = dqaly*WTP + surg + mri
    return fixed_value + 400.0  # MAP = fixed value + CPT credit

profiles = {'Optimized (90% Se, 80% Sp)': (0.90, 0.80),
            'Base-Case (85% Se, 82% Sp)': (0.85, 0.82),
            'Decayed (77% Se, 63% Sp)': (0.77, 0.63)}
fees = np.linspace(0, 3000, 200)
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
colors = ['#1b7837', '#2166ac', '#b2182b']
for (label, (se, sp)), col in zip(profiles.items(), colors):
    fixed_value = map_and_fixed_value(se, sp) - 400.0
    nmb_curve = fixed_value + (400.0 - fees)
    map_price = fixed_value + 400.0
    ax.plot(fees, nmb_curve, label=f'{label}; MAP=${map_price:,.0f}', color=col, linewidth=2.2)
ax.axhline(0, color='black', linestyle='--')
ax.set_xlabel('Software Licensing Fee per Scan (USD)')
ax.set_ylabel('Incremental NMB, per equivocal-subset patient (USD)')
ax.set_title('Figure 2: Maximum Acceptable Price')
ax.legend()
plt.tight_layout()
plt.savefig('Figure2_MAP.tiff', dpi=300, format='tiff')
plt.savefig('Figure2_MAP.png', dpi=300)
print("Figure 2 saved.")
