import pandas as pd
import numpy as np
from scipy import stats
import pingouin as pg

EXCLUDE = ['gemini-2.5-flash', 'llama3-8b-instruct']

df = pd.read_csv('data/processed/exp1_basic_ive.csv')
df = df[(df['parse_success']==True) & (df['condition_persona']=='none') & (df['condition_prompt_frame']=='first_person')].copy()
df_excl = df[~df['model_key'].isin(EXCLUDE)].copy()

def cd(g1,g2):
    n1,n2=len(g1),len(g2)
    if n1<2 or n2<2: return float('nan')
    v1,v2=g1.var(ddof=1),g2.var(ddof=1)
    sp=np.sqrt(((n1-1)*v1+(n2-1)*v2)/(n1+n2-2))
    return (g1.mean()-g2.mean())/sp if sp>0 else 0

# Pooled (full 16)
ig_f = df[df['condition_identifiability']=='identifiable']['donation_amount'].dropna()
sg_f = df[df['condition_identifiability']=='statistical']['donation_amount'].dropna()
d_f = cd(ig_f, sg_f)
t_f, p_f = stats.ttest_ind(ig_f, sg_f)

# Pooled (excl 14)
ig_e = df_excl[df_excl['condition_identifiability']=='identifiable']['donation_amount'].dropna()
sg_e = df_excl[df_excl['condition_identifiability']=='statistical']['donation_amount'].dropna()
d_e = cd(ig_e, sg_e)
t_e, p_e = stats.ttest_ind(ig_e, sg_e)

print(f"FULL 16: Ident={ig_f.mean():.3f} Stat={sg_f.mean():.3f} d={d_f:.4f} t={t_f:.4f} p={p_f:.6f} n_i={len(ig_f)} n_s={len(sg_f)}")
print(f"EXCL 14: Ident={ig_e.mean():.3f} Stat={sg_e.mean():.3f} d={d_e:.4f} t={t_e:.4f} p={p_e:.6f} n_i={len(ig_e)} n_s={len(sg_e)}")
print()

print(f"FULL var(ident)={ig_f.var():.4f} var(stat)={sg_f.var():.4f}")
print(f"EXCL var(ident)={ig_e.var():.4f} var(stat)={sg_e.var():.4f}")
print()

# ANOVA on excluded set
aov = pg.anova(data=df_excl.dropna(subset=['donation_amount']), dv='donation_amount', between=['condition_identifiability', 'model_key'])
print("ANOVA (14-model pool):")
for _, row in aov.iterrows():
    src = row['Source']
    print(f"  {src:50s} F={row['F']:10.3f}  p={row['p-unc']:.6e}  np2={row['np2']:.6f}")
