#!/usr/bin/env python3
"""Exact R2J source-rule correction rerun; original V15 file is retained unchanged."""
from pathlib import Path
from collections import Counter
from itertools import product
import csv,json,hashlib,sys
ROOT=Path(__file__).resolve().parent
MAIN=ROOT/'R2J_PRIMARY_9x17_CORRECTED.csv'
OLD=ROOT/'V15_PRIMARY_9x17_ORIGINAL_HISTORY.csv'
CHAIN=ROOT/'V15_PRIMARY_CHAIN_UNCHANGED.csv'
OUT=ROOT/'derived_R2J';OUT.mkdir(exist_ok=True)
CLAUSES=[f'C{i:02d}' for i in range(1,18)]
def load(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
old=load(OLD);rows=load(MAIN)
assert len(rows)==len(old)==9
assert [r['document'] for r in rows]==[r['document'] for r in old]
assert sum(rows[i][c]!=old[i][c] for i in range(9) for c in CLAUSES)==1
assert [(x['document'],c,old[i][c],x[c]) for i,x in enumerate(rows) for c in CLAUSES if x[c]!=old[i][c]]==[('KU01','C04','E','P')]
assert all(set(r[c] for r in rows)<={'E','P','U'} for c in CLAUSES)
state=[{'clause':c,**{f'{s}_count':sum(r[c]==s for r in rows) for s in ('E','P','U')}} for c in CLAUSES]
assert next(x for x in state if x['clause']=='C04')=={'clause':'C04','E_count':8,'P_count':1,'U_count':0}
assert next(x for x in state if x['clause']=='C17')=={'clause':'C17','E_count':2,'P_count':1,'U_count':6}
def partition(data,a,b):
 vals=[(r[a]=='E',r[b]=='E') for r in data]
 return [sum(z==(True,True) for z in vals),sum(z==(True,False) for z in vals),sum(z==(False,True) for z in vals),sum(z==(False,False) for z in vals)]
PAIRS=[('C01_C04','C01','C04'),('C04_C06','C04','C06'),('C07_C08','C07','C08'),('C14_C17','C14','C17')]
P=[]
for name,a,b in PAIRS:
 counts=partition(rows,a,b)
 P.append(dict(pair=name,both_E=counts[0],first_only_E=counts[1],second_only_E=counts[2],neither_E=counts[3]))
assert [(x['both_E'],x['first_only_E'],x['second_only_E'],x['neither_E']) for x in P]==[(8,1,0,0),(3,5,0,1),(4,3,0,2),(1,6,1,1)]
loo=[]
for dropped in rows:
 keep=[r for r in rows if r['document']!=dropped['document']]
 rec={'dropped':dropped['document']}
 for name,a,b in PAIRS:rec[name+'_both_E']=partition(keep,a,b)[0]
 loo.append(rec)
assert [min(x['C01_C04_both_E'] for x in loo),max(x['C01_C04_both_E'] for x in loo)]==[7,8]
assert [min(x['C04_C06_both_E'] for x in loo),max(x['C04_C06_both_E'] for x in loo)]==[2,3]
assert [min(x['C07_C08_both_E'] for x in loo),max(x['C07_C08_both_E'] for x in loo)]==[3,4]
assert [min(x['C14_C17_both_E'] for x in loo),max(x['C14_C17_both_E'] for x in loo)]==[0,1]
by={r['document']:r for r in rows}
subids=['AUS01','KAU01','QATU01','UOB01','KU01']
five=[by[i] for i in subids]
assert [sum(r['C04']==x for r in five) for x in ('E','P','U')]==[4,1,0]
assert [(sum(r['C04']==s for r in rows if r['document'] not in ('ADU01','UOS01'))) for s in ('E','P','U')]==[6,1,0]
wide=[]
for u,s in product(('AUS01','UAEU01'),('PNU01','KAU01')):
 chosen=[by[i] for i in (u,s,'QATU01','UOB01','KU01')]
 rec={'UAE_broad':u,'Saudi_broad':s,'C04_E':sum(r['C04']=='E' for r in chosen),'C04_P':sum(r['C04']=='P' for r in chosen)}
 for name,a,b in PAIRS:rec[name+'_both_E']=partition(chosen,a,b)[0]
 wide.append(rec)
assert len(wide)==4 and all(x['C04_E']==4 and x['C04_P']==1 and x['C14_C17_both_E']==0 for x in wide)
assert sorted(set(x['C04_C06_both_E'] for x in wide))==[1,2]

def export(name,recs):
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(recs[0]),lineterminator='\n');w.writeheader();w.writerows(recs)
export('R2J_ClauseEPUMarginals.csv',state)
export('R2J_FourPairPartitions.csv',P)
export('R2J_NineLeaveOneOut.csv',loo)
export('R2J_FourCountryBalancedCompositions.csv',wide)
with CHAIN.open(newline='',encoding='utf-8-sig') as f:ch=list(csv.DictReader(f))
assert len(ch)==6 and all(len({v for k,v in r.items() if k.lower() not in ('state','country','gcc_state','jurisdiction')}-{'E','P','U'})==0 for r in ch)
summary={'n':9,'clauses':17,'states':153,'corrected_cells':1,
'C04_EPU':[8,1,0],'C17_EPU':[2,1,6],
'pairs':P,'C01_C04_LOO_range':[7,8],
'five_broad_C04_EPU':[4,1,0],
'four_balanced_composition_C04_EPU':[[4,1,0] for _ in range(4)],
'limits':'One source-aligned KU01 C04 E to P correction; prior V15 retained. No source-vintage proof for UOS01.'}
(OUT/'R2J_ExactSummary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('R2J SOURCE-CORRECTED ONE-CELL REPRODUCTION PASS: 153 cells / 1 change; 8/1/0 disclosure; four pairing partitions and LOO verified')
