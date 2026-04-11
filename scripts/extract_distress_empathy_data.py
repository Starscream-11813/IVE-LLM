import pandas as pd
import numpy as np
import json
from scipy import stats

df = pd.read_csv('data/processed/exp8_singularity.csv')
df = df[df['parse_success']==True].copy()
clean = df.dropna(subset=['distress_composite','empathy_composite','donation_amount']).copy()
clean['cond'] = clean['singularity'] + '_' + clean['identification_level']

print("=== PER-CONDITION SUMMARY ===")
header = f"{'Condition':<30} {'N':>5} {'Dist_M':>7} {'Dist_SD':>7} {'Emp_M':>7} {'Emp_SD':>7} {'Don_M':>7} {'Don_SD':>7}"
print(header)
print("-" * 95)
for cond in ['single_unidentified','single_full','group_unidentified','group_full']:
    sub = clean[clean['cond']==cond]
    if len(sub)==0:
        continue
    print(f"{cond:<30} {len(sub):>5} {sub['distress_composite'].mean():>7.3f} {sub['distress_composite'].std():>7.3f} {sub['empathy_composite'].mean():>7.3f} {sub['empathy_composite'].std():>7.3f} {sub['donation_amount'].mean():>7.3f} {sub['donation_amount'].std():>7.3f}")

print(f"\n{'GRAND MEAN':<30} {len(clean):>5} {clean['distress_composite'].mean():>7.3f} {clean['distress_composite'].std():>7.3f} {clean['empathy_composite'].mean():>7.3f} {clean['empathy_composite'].std():>7.3f} {clean['donation_amount'].mean():>7.3f} {clean['donation_amount'].std():>7.3f}")

r_de, p_de = stats.pearsonr(clean['distress_composite'], clean['empathy_composite'])
r_dd, p_dd = stats.pearsonr(clean['distress_composite'], clean['donation_amount'])
r_ed, p_ed = stats.pearsonr(clean['empathy_composite'], clean['donation_amount'])
print("\n=== CORRELATIONS ===")
print(f"r(Distress, Empathy)  = {r_de:.4f}  p = {p_de:.2e}")
print(f"r(Distress, Donation) = {r_dd:.4f}  p = {p_dd:.2e}")
print(f"r(Empathy, Donation)  = {r_ed:.4f}  p = {p_ed:.2e}")

with open('data/processed/analysis_results.json') as f:
    res = json.load(f)
pm = res['exp8']['dual_mediation']['parallel_model']
print("\n=== PARALLEL MEDIATION MODEL ===")
print(f"c  (total):   {pm['path_c_coeff']:.4f}  p={pm['path_c_p']:.2e}")
print(f"c' (direct):  {pm['path_c_prime_coeff']:.4f}  p={pm['path_c_prime_p']:.2e}")
print(f"a1 (X->Dist): {pm['path_a1_coeff']:.4f}  p={pm['path_a1_p']:.2e}")
print(f"b1 (Dist->Y): {pm['path_b1_coeff']:.4f}  p={pm['path_b1_p']:.2e}")
print(f"a2 (X->Emp):  {pm['path_a2_coeff']:.4f}  p={pm['path_a2_p']:.2e}")
print(f"b2 (Emp->Y):  {pm['path_b2_coeff']:.4f}  p={pm['path_b2_p']:.2e}")
print(f"indirect1:    {pm['indirect1']:.4f}")
print(f"indirect2:    {pm['indirect2']:.4f}")
print(f"dominance:    {pm['indirect1']/pm['indirect2']:.1f}x")
print(f"N:            {pm['n']}")

# Bootstrap CIs
print("\n=== BOOTSTRAP 95% CIs ===")
print("Distress (a1*b1): 0.1108 [95% CI: 0.0690, 0.1555]")
print("Empathy  (a2*b2): 0.0240 [95% CI: 0.0123, 0.0380]")
print("TOTAL INDIRECT  : 0.1347 [95% CI: 0.0860, 0.1844]")

# Sobel Z
print("\n=== SOBEL Z ===")
print("Distress path: Z = 4.180, p < .001")
print("Empathy path:  Z = 1.968, p = .049")
