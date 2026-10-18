# R2J — source-rule corrected documentary classification replay

This repository retains an original historical nine-document ×17-clause (153-cell) E/P/U classification alongside a **single corrected cell**: KU01/C04 `E` → `P`. The official November 2024 Kuwait University text makes faculty requests for disclosure detail discretionary, so that wording does not satisfy the article's explicit disclosure-duty threshold (E). A qualified rule left to instructor discretion is P.

The source-corrected matrix is `R2J_PRIMARY_9x17_CORRECTED.csv`; the untouched historical matrix is `V15_PRIMARY_9x17_ORIGINAL_HISTORY.csv`. Run:

```sh
python3 reproduce_r2j.py
```

No third-party libraries or internet requests are needed. Machine-generated R2J results are in `derived_R2J/` and include 17 clause E/P/U counts, four pair partitions, nine leave-one-document-out calculations, and four complete five-document alternative country-balanced compositions.

**Corrected descriptive counts:** C04 E/P/U 8/1/0. Jointly explicit C01/C04 8/9, C04/C06 3/9, C07/C08 4/9 and C14/C17 1/9 (conditional on unresolved historical UOS01 source parity). In the one-broad-document-per-country subset and each of four eligible alternative country compositions, C04 E/P/U 4/1/0. The six-country L1–L4 map and all other 152 classification cells remain unchanged.

The historical `reproduce_joint_clauses.py` available separately is intentionally unchanged and reproduces original, **superseded** V15 counts. Do not run it expecting the corrected R2J counts. The R2J source audit distinguishes full first-party text from first-party index links and inheritable but unverified source classifications. In particular, original historic UOS01 and the complete 39-record source register remain unavailable, as do source-originals sufficient to fully verify UOB01 and KAU01; **do not claim full 153-cell independent recoding**.

PNU01 explicitly restricts faculty use of AI-content detectors but the original C17 criterion narrowly requires a limit on treating automated detection as sole/conclusive **disciplinary evidence**; its historical C17 U is retained, with that protective provision separately explained. No human participant study, independent coder agreement or causal outcome measurement was performed. This repository intentionally does not redistribute university-issued PDF policy files or identify the author for reviewer-anonymity purposes.
