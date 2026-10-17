#!/usr/bin/env python3
"""Reproduce exploratory document-level co-explicitness checks from the frozen EGCC V15 CSV.

This is a post-hoc descriptive extension, NOT a new university score,
inter-rater result, inferential test, prevalence estimate, or V15 recoding.
Requires only Python standard library. Run from this file's directory:
    python reproduce_joint_clauses.py
"""
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'V15_PRIMARY_9x17_MATRIX_LOCKED.csv'
CHAIN = ROOT / 'V15_PRIMARY_CHAIN_LOCKED.csv'
OUT = ROOT / 'derived'
OUT.mkdir(exist_ok=True)

with DATA.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    columns = reader.fieldnames
assert columns == ['document']+[f'C{i:02d}' for i in range(1,18)]
assert len(rows) == 9 and len({r['document'] for r in rows}) == 9
assert set(v for r in rows for k,v in r.items() if k != 'document') <= {'E','P','U'}
assert {k:sum(r[k]=='E' for r in rows) for k in ['C01','C04','C06','C08','C09','C10','C14','C17']} == {
  'C01':9,'C04':9,'C06':3,'C08':4,'C09':8,'C10':7,'C14':7,'C17':2}
with CHAIN.open(newline='',encoding='utf-8-sig') as f:
    chains=list(csv.DictReader(f))
assert len(chains)==6 and sorted(r['L3'] for r in chains)==['E','P','P','P','U','U']
assert all(r['L4']=='E' for r in chains)

PAIRS=[
    ('C01','C04','Scope + general disclosure (positive control)'),
    ('C04','C06','Disclosure duty + attribution/citation format'),
    ('C07','C08','Assessment controls + authentic process/verification'),
    ('C14','C17','Accountability/due process + detector non-sole-evidence safeguard'),
]
summary=[]; replay=[];loo=[]
for a,b,desc in PAIRS:
    eflags=[]
    for r in rows:
        ae = r[a]=='E';be = r[b]=='E'
        status = 'BOTH_E' if ae and be else 'FIRST_ONLY_E' if ae else 'SECOND_ONLY_E' if be else 'NEITHER_E'
        replay.append({'pair':f'{a}+{b}','description':desc,'document':r['document'],
                       'first_state':r[a],'second_state':r[b],'co_explicit':int(ae and be),'category':status})
        eflags.append(int(ae and be))
    counts={s:sum(v['pair']==f'{a}+{b}' and v['category']==s for v in replay) for s in ['BOTH_E','FIRST_ONLY_E','SECOND_ONLY_E','NEITHER_E']}
    assert sum(counts.values())==9
    leave=[]
    for r,flag in zip(rows,eflags):
        leave.append(sum(eflags)-flag)
        loo.append({'pair':f'{a}+{b}','dropped_document':r['document'], 'remaining_documents':8,
                    'remaining_explicit_pair':sum(eflags)-flag})
    summary.append({'pair':f'{a}+{b}','description':desc, 'both_E':counts['BOTH_E'],
      'first_only_E':counts['FIRST_ONLY_E'],'second_only_E':counts['SECOND_ONLY_E'],
      'neither_E':counts['NEITHER_E'],'n_documents':9,
      'loo_both_min':min(leave),'loo_both_max':max(leave)})
expected={'C01+C04':(9,0,0,0),'C04+C06':(3,6,0,0),'C07+C08':(4,3,0,2),'C14+C17':(1,6,1,1)}
for r in summary:
    assert (r['both_E'],r['first_only_E'],r['second_only_E'],r['neither_E'])==expected[r['pair']]
assert len(replay)==36 and len(loo)==36

def export(name, records):
    with (OUT/name).open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(records[0].keys()));w.writeheader();w.writerows(records)
export('R2_ExploratoryPairSummary.csv',summary)
export('R2_ExploratoryDocumentReplay.csv',replay)
export('R2_ExploratoryLOO.csv',loo)
report={
 'derivation_status':'PASS: R2 exploratory only; frozen V15 untouched',
 'matrix_sha256':hashlib.sha256(DATA.read_bytes()).hexdigest(),
 'chain_sha256':hashlib.sha256(CHAIN.read_bytes()).hexdigest(),
 'source_document_count':9,'clause_count':17,'jurisdictions':6,
 'all_primary_cells':153,'joint_pairs':summary,
 'analytic_constraints':['post-hoc co-presence rather than originally predeclared hypothesis',
 'non-E includes P and U; no policy-absence inference',
 'C14 is broad accountability/procedure, not an appeal-right guarantee',
 'C17 is explicit non-sole-evidence limitation, not detector quality measurement',
 'one-per-jurisdiction and document-type results remain inherited V15 only',
 'leave-one-document-out tests fixed rows but not sampling uncertainty',
 'no observed compliance, legal adequacy, classroom decision or population prevalence'],
}
(OUT/'R2_Reproduction_Audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print('R2 ALL DETERMINISTIC ASSERTIONS PASS')
for x in summary:print(x['pair'],':',x['both_E'], '/', x['n_documents'], 'both E; LOO', x['loo_both_min'], '-', x['loo_both_max'])
