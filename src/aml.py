import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def monitor(customers, transactions):
    profiles = {r['customer_id']: r for r in customers}
    by_customer = defaultdict(list)
    for tx in transactions:
        by_customer[tx['customer_id']].append(tx)
    alerts = []
    for customer_id, items in by_customer.items():
        profile = profiles.get(customer_id)
        if not profile:
            continue
        items.sort(key=lambda x: x['timestamp'])
        baseline = float(profile['typical_deposit_cad'])
        for i, tx in enumerate(items):
            amount = float(tx['amount_cad'])
            reasons = []
            if tx['type'] == 'deposit' and amount >= max(3 * baseline, 3000):
                reasons.append('Deposit substantially above stated baseline (illustrative rule)')
            if tx['type'] == 'crypto_withdrawal':
                when = datetime.fromisoformat(tx['timestamp'])
                recent = [p for p in items[:i] if p['type'] == 'deposit' and timedelta(0) <= when - datetime.fromisoformat(p['timestamp']) <= timedelta(hours=24)]
                if recent:
                    reasons.append('Crypto withdrawal within 24 hours of deposit (illustrative rule)')
            if reasons:
                alerts.append({'customer_id':customer_id,'transaction_id':tx['transaction_id'],'timestamp':tx['timestamp'],'amount_cad':tx['amount_cad'],'indicators':reasons,'review_status':'Analyst review required'})
    return alerts

def validate_cases(cases):
    results=[]
    for case in cases:
        issues=[]
        for field in ('case_id','customer_id','transaction_id','transaction_date','reported_amount_cad','source_amount_cad'):
            if not case.get(field, '').strip():
                issues.append(f'Missing {field}')
        try:
            if float(case['reported_amount_cad']) != float(case['source_amount_cad']):
                issues.append('Amount differs from source record')
        except (ValueError, KeyError):
            issues.append('Invalid or unavailable amount')
        try:
            datetime.fromisoformat(case['transaction_date'])
        except (ValueError, KeyError):
            issues.append('Invalid or unavailable transaction date')
        results.append({'case_id':case.get('case_id','UNKNOWN'),'status':'Review required' if issues else 'Checks passed','issues':issues})
    return results

def write_outputs(alerts, checks, output):
    output.mkdir(parents=True, exist_ok=True)
    with open(output/'alerts.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=['customer_id','transaction_id','timestamp','amount_cad','indicators','review_status'])
        writer.writeheader()
        for alert in alerts:
            writer.writerow({**alert,'indicators':'; '.join(alert['indicators'])})
    (output/'validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    lines=['# AML Monitoring — Synthetic Case Summary','','> Demonstration only. Alerts are not determinations of suspicion or regulatory reporting obligations.','',f'**Alerts generated:** {len(alerts)}',f'**Reporting records checked:** {len(checks)}','','## Transaction indicators','']
    for a in alerts:
        lines += [f"- **{a['transaction_id']}** ({a['customer_id']}, CAD {a['amount_cad']}): {'; '.join(a['indicators'])}"]
    lines += ['','## Reporting data checks','']
    for c in checks:
        lines += [f"- **{c['case_id']}**: {c['status']}" + (f" — {'; '.join(c['issues'])}" if c['issues'] else '')]
    lines += ['','## Next step','','An authorized analyst reviews all indicators and discrepancies. This tool neither decides whether reasonable grounds to suspect exist nor files STRs.']
    (output/'case_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    customers=load_csv(ROOT/'data'/'customers.csv')
    transactions=load_csv(ROOT/'data'/'transactions.csv')
    cases=load_csv(ROOT/'data'/'reporting_cases.csv')
    alerts=monitor(customers,transactions)
    checks=validate_cases(cases)
    write_outputs(alerts,checks,ROOT/'output')
    print(f'Generated {len(alerts)} alerts; {sum(c["status"]=="Review required" for c in checks)} reporting records need review.')
    print('See output/alerts.csv, output/validation.json, output/case_summary.md')

if __name__=='__main__':
    main()
