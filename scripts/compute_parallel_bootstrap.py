import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def main():
    csv_path = 'data/processed/exp8_singularity.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    df = df[df['identification_level'].isin(['unidentified', 'full'])].dropna(
        subset=['donation_amount', 'distress_composite', 'empathy_composite']
    ).copy()
    
    df['X'] = (df['identification_level'] == 'full').astype(int)
    n = len(df)
    
    boot_dist = []
    boot_emp = []
    boot_total = []
    rng = np.random.RandomState(42)
    n_bootstrap = 5000
    
    print(f"Starting Bootstrap (N={n}, Iterations={n_bootstrap})...")
    
    X = df['X'].values
    M1 = df['distress_composite'].values
    M2 = df['empathy_composite'].values
    Y = df['donation_amount'].values
    
    for i in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        X_b, M1_b, M2_b, Y_b = X[idx], M1[idx], M2[idx], Y[idx]
        
        try:
            a1 = sm.OLS(M1_b, sm.add_constant(X_b)).fit().params[1]
            a2 = sm.OLS(M2_b, sm.add_constant(X_b)).fit().params[1]
            model_p = sm.OLS(Y_b, sm.add_constant(np.column_stack([X_b, M1_b, M2_b]))).fit()
            b1 = model_p.params[2]
            b2 = model_p.params[3]
            
            ind1 = a1 * b1
            ind2 = a2 * b2
            boot_dist.append(ind1)
            boot_emp.append(ind2)
            boot_total.append(ind1 + ind2)
        except Exception:
            continue
            
        if (i+1) % 1000 == 0:
            print(f"  Completed {i+1} iterations...")

    ci_dist = [np.percentile(boot_dist, 2.5), np.percentile(boot_dist, 97.5)]
    ci_emp = [np.percentile(boot_emp, 2.5), np.percentile(boot_emp, 97.5)]
    ci_total = [np.percentile(boot_total, 2.5), np.percentile(boot_total, 97.5)]
    
    print("\n" + "="*40)
    print("PARALLEL MEDIATION BOOTSTRAP RESULTS")
    print("="*40)
    print(f"Distress (a1*b1): {np.mean(boot_dist):.4f} [95% CI: {ci_dist[0]:.4f}, {ci_dist[1]:.4f}]")
    print(f"Empathy  (a2*b2): {np.mean(boot_emp):.4f} [95% CI: {ci_emp[0]:.4f}, {ci_emp[1]:.4f}]")
    print(f"TOTAL INDIRECT  : {np.mean(boot_total):.4f} [95% CI: {ci_total[0]:.4f}, {ci_total[1]:.4f}]")
    print("="*40)

if __name__ == "__main__":
    main()
