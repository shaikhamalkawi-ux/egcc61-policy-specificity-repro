# GCC AI governance: reviewer reproducibility packet

This is an author-neutral archive for a full-length GCC public-documentary research manuscript under **double-anonymized peer review**. 

## Contents

- `V15_PRIMARY_9x17_MATRIX_LOCKED.csv`: the original nine published-document-by-17-clause E/P/U classification matrix (153 category cells); not recoded.
- `V15_PRIMARY_CHAIN_LOCKED.csv`: six jurisdiction-by-four governance-function category states; not recoded.
- `reproduce_joint_clauses.py`: Python standard-library script for frozen marginal checks, exploratory co-explicitness pairs, leave-one-document-out descriptive replay and derivation audit.
- `derived/`: deterministically generated CSV and JSON outputs from a clean local run.

Run: `python3 reproduce_joint_clauses.py` or `bash run.sh`. No packages or network are needed.

## Important claim boundaries

- E = a documented explicit provision under the operational coding rule; P = partial; U = qualified public evidence not located under the recorded search protocol, **not** proof the institution lacks a rule.
- Paired diagnostics are **post-hoc descriptive** checks, not preregistered tests or estimates of the GCC HE sector.
- The fixed n=9 and six-jurisdiction units are not representative samples for institutional maturity, compliance, student behavior, or implementation quality.
- The complete exact original V15 39-entry source register and several raw third-party policy originals are not fully recovered: replay of data derived from the frozen category matrices is possible; **independent replay of every original source-admission decision is not demonstrated**.
- University-issued policy PDFs are **not redistributed**; issuer addresses and source access boundaries appear in the manuscript's separately submitted Appendix.

## Status and rights

Reviewer-access archive only. No DOI, formal code license, journal acceptance or independent source audit is implied. Any public redistribution should respect source and code licensing; absence of a license is not a grant of reuse rights. This ZIP does not intentionally contain author names, personal affiliations, or private third-party PDFs.

## Additional bounded R2I sensitivity (journal manuscript, post-hoc)

The added `reproduce_exhaustive_broad_subsets.py` derives **all four admissible**
five-document choices under the *existing* one-broad-policy-per-eligible-country
criterion: two broad UAE choices × two broad Saudi choices, with the Qatar,
Bahrain, and Kuwait documents fixed. It excludes the integrity-specific ADU01
and graduate-specific UOS01 **only in this sensitivity**, not from the locked
nine-document primary analysis.

Run: `python3 reproduce_exhaustive_broad_subsets.py`. The generated
`derived/R2I_ExhaustiveBroadCountrySubsets.csv` includes all 17-clause E/P/U
marginals and four paired-explicitness counts per subset;
`derived/R2I_BroadSubsetSummary.json` gives the bounded headline.

Across the four subsets disclosure is explicit in 5/5, joint
disclosure/attribution and assessment/authenticity each range 1/5–2/5,
and broad-only C14/C17 co-explicitness is 0/5. These are within-corpus,
post-hoc composition checks—not independent source verification, population
inference, policy-effectiveness estimates, or proof of institutional omission.

**Documentary source limitation:** the historically used undated UOS01
source archive/identity has not been reconstructed at the byte level, so
its originally reported C14/C17 intersection (1/9) retains a
historical-edition provenance gate. Current live university policy pages cannot
retroactively establish exact archive parity. This public package holds no
third-party university policy PDFs or personally identifying author records.
