# Mathematical Formulations and Statistical Methods

This document outlines the mathematical equations and statistical frameworks employed across the 10 experiments in this research project to analyze the Identifiable Victim Effect (IVE) in Large Language Models (LLMs).

---

## 1. Effect Size Measures

### 1.1 Cohen's $d$ (Standardized Mean Difference)
Cohen's $d$ was used as the primary measure of effect size to quantify the magnitude of the difference in donation amounts between the "Identifiable Victim" and "Statistical Group" conditions.

$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_p}$$

Where:
- $\bar{x}_1$ and $\bar{x}_2$ are the sample means of the two groups.
- $s_p$ is the **pooled standard deviation**, calculated as:

$$s_p = \sqrt{\frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}}$$

### 1.2 Partial Eta Squared ($\eta^2_p$)
For Analysis of Variance (ANOVA), partial eta squared was used to measure the proportion of variance explained by a specific factor (e.g., Identifiability or Model type), excluding variance explained by other factors in the design.

$$\eta^2_p = \frac{SS_{\text{effect}}}{SS_{\text{effect}} + SS_{\text{error}}}$$

---

## 2. Regression Models

### 2.1 Psychophysical Numbing (Logarithmic Decay)
In Experiment 7, we tested the hypothesis that compassion decays logarithmically as the number of victims increases. This was modeled using linear regression on the base-10 logarithm of the victim count:

$$y = \beta_0 + \beta_1 \log_{10}(x) + \epsilon$$

Where:
- $y$ is the donation amount.
- $x$ is the victim count ($1, 10, \dots, 3{,}000{,}000$).
- $\beta_1$ represents the coefficient of numbing (the rate of compassion decay).

### 2.2 Identification Gradient (Linear Trend)
In Experiment 9, a linear trend was tested across 6 levels of identification:

$$y = \beta_0 + \beta_1 \cdot \text{Level} + \epsilon$$

Where $\text{Level} \in \{1, 2, 3, 4, 5, 6\}$ corresponds to the depth of biographical narrative provided.

---

## 3. Mediation Analysis

We employed a dual-mediation framework to test whether the effect of identification ($X$) on donation behavior ($Y$) is mediated by internal affective states: Empathy ($M_1$) and Personal Distress ($M_2$).

### 3.1 Total and Direct Effects
The relationship is defined by the following system of linear equations:

$$M_1 = i_1 + a_1 X + \epsilon_1$$
$$M_2 = i_2 + a_2 X + \epsilon_2$$
$$Y = i_3 + c' X + b_1 M_1 + b_2 M_2 + \epsilon_3$$

Where:
- $a_1, a_2$: The effect of identification on the mediators.
- $b_1, b_2$: The effect of the mediators on donation, controlling for identification.
- $c'$: The **direct effect** of identification on donation.

### 3.2 Indirect Effects
The **indirect effect** through a specific mediator is the product of the corresponding path coefficients:

$$\text{Indirect}_1 = a_1 \times b_1$$
$$\text{Indirect}_2 = a_2 \times b_2$$

The **Total Effect** ($c$) is the sum of the direct and all indirect effects:

$$c = c' + (a_1 b_1) + (a_2 b_2)$$

### 3.3 Proportion Mediated
The proportion of the total effect explained by a mediator is calculated as:

$$P_m = \frac{a_i b_i}{c}$$

---

## 4. Relationship Analyses

### 4.1 Pearson Correlation ($r$)
To quantify the linear relationship between internal emotional ratings (e.g., feelings composite) and donation choices:

$$r = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2 \sum_{i=1}^n (y_i - \bar{y})^2}}$$

### 4.2 Feelings Composite
The internal affective state variable was typically computed as the arithmetic mean of $k$ Likert-scale items:

$$\text{Feelings} = \frac{1}{k} \sum_{j=1}^k \text{Rating}_j$$

For Experiments 8-10, this was split into:
- **Empathy Composite**: Mean of (Sympathetic, Compassion, Tender, Moved, Softhearted).
- **Distress Composite**: Mean of (Worried, Upset, Sad, Disturbed, Troubled).

---

## 5. Significance Testing

### 5.1 $F$-Statistic (ANOVA)
Used to test for interaction effects ($H_0: \mu_{ij} = \mu_{i.} + \mu_{.j} - \mu_{..}$):

$$F = \frac{MS_{\text{between}}}{MS_{\text{within}}}$$

### 5.2 $t$-Statistic (Independent Samples)
Used for pairwise comparisons between Identifiable and Statistical conditions:

$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$
*(Welch's t-test used for unequal variances/sample sizes)*
