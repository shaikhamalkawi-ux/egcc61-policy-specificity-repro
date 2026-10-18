#!/usr/bin/env python3
"""Bounded exploratory sensitivity: all one-broad-document per-country five-document subsets.

Scientific boundary: uses FROZEN publicly disclosed classifications, with no new
policy admission or recoding. Not a random sample, confidence interval, or
external confirmation of primary source editions.
"""
from pathlib import Path
from itertools import product
import csv, json

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'V15_PRIMARY_9x17_MATRIX_LOCKED.csv'
OUT=ROOT/'derived'
OUT.mkdir(exist_ok=True)
with SRC.open(encoding='utf-8-sig',newline='') as handle:
    data=list(csv.DictReader(handle))
expected=['ADU01','AUS01','UAEU01','UOS01','PNU01','QATU01','UOB01','KU01','KAU01']
assert len(data)==9 and {d['document'] for d in data}==set(expected)
records={r['document']:r for r in data}
clause_cols=[f'C{i:02d}' for i in range(1,18)]
assert all(set(records[k][c] for k in expected)<={'E','P','U'} for c in clause_cols)

# Original broad/specialized classification: ADU01 integrity-specific,
# UOS01 graduate-specific. All admissible country-balanced broad selections
# thus form 2 UAE x 2 Saudi options x 3 fixed singleton jurisdictions.
uae=('AUS01','UAEU01')
saudi=('PNU01','KAU01')
fixed=('QATU01','UOB01','KU01')
rows=[]
for u,s in product(uae,saudi):
    ids=(u,s,*fixed)
    row={'UAE_broad':u,'Saudi_broad':s,'Qatar':'QATU01','Bahrain':'UOB01','Kuwait':'KU01','n':len(ids)}
    for c in clause_cols:
        for status in ('E','P','U'):
            row[f'{c}_{status}']=sum(records[id][c]==status for id in ids)
    for label,a,b in (('C01_C04','C01','C04'),('C04_C06','C04','C06'),('C07_C08','C07','C08'),('C14_C17','C14','C17')):
        row[f'{label}_both_E']=sum(records[id][a]=='E' and records[id][b]=='E' for id in ids)
    rows.append(row)
assert len(rows)==4 and all(x['n']==5 for x in rows)
assert all(x['C04_E']==5 and x['C01_E']==5 for x in rows)
assert sorted({x['C04_C06_both_E'] for x in rows})==[1,2]
assert sorted({x['C07_C08_both_E'] for x in rows})==[1,2]
assert all(x['C14_C17_both_E']==0 for x in rows)
# The previously displayed A7 five-country vector corresponds to AUS+KAU;
# the full E/P/U vectors are verified separately against the actual A7 table.
orig=next(x for x in rows if x['UAE_broad']=='AUS01' and x['Saudi_broad']=='KAU01')
assert orig['C06_E']==2 and orig['C08_E']==2 and orig['C17_E']==1 and orig['C17_P']==1

names=list(rows[0])
with (OUT/'R2I_ExhaustiveBroadCountrySubsets.csv').open('w',newline='',encoding='utf-8') as handle:
    dw=csv.DictWriter(handle,fieldnames=names);dw.writeheader();dw.writerows(rows)
summary={
  'design':'All four admissible one-broad-per-eligible-jurisdiction compositions from the frozen nine-document matrix, excluding the specialized integrity and graduate texts',
  'combinations':len(rows),
  'reused_source_matrix':'V15_PRIMARY_9x17_MATRIX_LOCKED.csv',
  'one_country_baseline':['AUS01','KAU01','QATU01','UOB01','KU01'],
  'E_C04_each':[x['C04_E'] for x in rows],
  'both_E_C04_C06':[x['C04_C06_both_E'] for x in rows],
  'both_E_C07_C08':[x['C07_C08_both_E'] for x in rows],
  'both_E_C14_C17':[x['C14_C17_both_E'] for x in rows],
  'status':'descriptive post-hoc sensitivity, no new coded judgments or representativeness claims',
  'caveat':'UOS01 is graduate-specific, excluded by the broad-policy admissibility criterion and still has a historical source-identity gate.'
}
(OUT/'R2I_BroadSubsetSummary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('R2I FOUR-SUBSET SENSITIVITY PASS')
print(json.dumps({'n':len(rows),'disclosure':[r['C04_E'] for r in rows],
    'disclosure_attribution':[r['C04_C06_both_E'] for r in rows],
    'assessment_authenticity':[r['C07_C08_both_E'] for r in rows],
    'due_process_detector':[r['C14_C17_both_E'] for r in rows]}))
