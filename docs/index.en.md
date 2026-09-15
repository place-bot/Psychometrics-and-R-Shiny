# Psychometrics and R Shiny Notes

This site collects notes on psychometrics, Classical Test Theory (CTT), Item Response Theory (IRT), local-dependence modeling, Computerized Adaptive Testing (CAT), Cognitive Diagnosis Models (CDMs), and introductory R Shiny practice.

The material is organized by topic for course review, quick reference, and continued revision. The site is built with **MkDocs + Material** and supports mathematical notation, code blocks, full-text search, and structured navigation.

## Quick links

- [Psychometrics foundations](psychometrics/index.md)
- [Psychological Measurement and Test Development](test-development/index.md)
- [IRT models](irt-models/index.md)
- [IRT estimation and evaluation](irt-estimation/index.md)
- [CTT/IRT application rules](10_rules_ctt_irt/index.md)
- [Cognitive Diagnosis Models (CDMs)](cdm/index.md)
- [Local Dependence Modeling](local-dependence-modeling/index.md)
- [Computerized Adaptive Testing (CAT)](cat/index.md)
- [R Shiny](shiny/index.md)
- [Quality and maintenance](quality/index.md)

## Notation example

A common form of the two-parameter logistic model (2PL) is:

\[
P(X_{ij}=1 \mid \theta_j)
=
\frac{1}{1+\exp[-a_i(\theta_j-b_i)]}
\]

Here, \(\theta_j\) denotes participant \(j\)'s latent trait level, \(a_i\) is the discrimination parameter of item \(i\), and \(b_i\) is its difficulty parameter.
