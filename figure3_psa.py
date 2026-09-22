import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(2026)
N = 10000
EQUIVOCAL_RATE, WTP = 0.26, 100000
BLENDED_FRAC_B, BLENDED_FRAC_C = 0.4034, 0.5966
DISC_YEARS = 1.5775

def beta_from_range(mean, lo, hi):
    sd = (hi-lo)/(2*1.96); var = sd**2
    if var >= mean*(1-mean): var = 0.9*mean*(1-mean)
    k = mean*(1-mean)/var - 1
    return stats.beta(mean*k, (1-mean)*k)

def gamma_from_range(mean, lo, hi):
    sd = (hi-lo)/(2*1.96); var = sd**2
    return stats.gamma(mean**2/var, scale=var/mean)

d_sens = beta_from_range(0.85, 0.60, 0.95)
d_spec = beta_from_range(0.82, 0.50, 0.95)
d_comp = beta_from_range(0.762, 0.50, 1.00)
d_prev = beta_from_range(1/3, 0.25, 0.40)
d_equiv = beta_from_range(0.26, 0.15, 0.35)
d_sc = beta_from_range(0.216, 0.12, 0.30)
d_biopsy = gamma_from_range(40661, 10000, 108682)
d_cranio = gamma_from_range(27442, 8450, 46434)
d_mri = gamma_from_range(1080, 800, 1500)
d_fee = stats.uniform(100, 500)
d_credit = stats.uniform(0, 600)
d_risk = beta_from_range(0.10, 0.05, 0.15)

dcost = np.zeros(N); dqaly = np.zeros(N)
for i in range(N):
    se,sp,c = d_sens.rvs(), d_spec.rvs(), d_comp.rvs()
    prev,eq,sc = d_prev.rvs(), d_equiv.rvs(), d_sc.rvs()
    biop,cran,mri_c = d_biopsy.rvs(), d_cranio.rvs(), d_mri.rvs()
    fee,credit,risk = d_fee.rvs(), d_credit.rvs(), d_risk.rvs()
    blended = BLENDED_FRAC_B*biop + BLENDED_FRAC_C*cran
    p_ai = sc*(1-sp*c)
    surg = (sc-p_ai)*prev*blended
    resolved = sp*c*prev
    mri_sav = resolved*mri_c/(1.03**(1/12))**2
    margin = credit-fee
    dc_equiv = -(surg+mri_sav+margin)
    dq_equiv = (sc-p_ai)*prev*risk*0.17*DISC_YEARS
    dcost[i] = dc_equiv*eq
    dqaly[i] = dq_equiv*eq

inmb = dqaly*WTP - dcost
pct = np.mean(inmb>0)*100

fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=300)
ax.scatter(dqaly, dcost, alpha=0.35, s=14, c='#2b83ba', edgecolor='none')
xr = np.linspace(dqaly.min(), dqaly.max(), 50)
ax.plot(xr, WTP*xr, color='red', linestyle='--', label='$100,000/QALY threshold')
ax.axhline(0, color='black', linewidth=0.8); ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Incremental QALY (full-cohort)')
ax.set_ylabel('Incremental Cost, USD (full-cohort)')
# title removed -- belongs in the manuscript legend, not the figure canvas
ax.legend()
plt.tight_layout()
plt.savefig('Figure3_PSA.tiff', dpi=300, format='tiff')
plt.savefig('Figure3_PSA.png', dpi=300)
print("Figure 3 saved.")
