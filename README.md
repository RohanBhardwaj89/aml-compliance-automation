# AML Transaction Monitoring & Reporting Automation

A small, dependency-free Python portfolio demonstration inspired by practical AML operations in banking and virtual currency services. Uses **100% synthetic data**.

## What it does

1. **Transaction monitoring:** flags deposits that materially exceed a customer's illustrative baseline and cryptocurrency withdrawals occurring within 24 hours of a deposit.
2. **Reporting data validation:** checks missing case fields, malformed dates, and differences between reported and source amounts.
3. **Case summary generation:** writes an explainable Markdown review report, alert CSV, and JSON validation results.

## Quick start

Requires Python 3.9+. From the project root:

```bash
python -m src.aml
python -m unittest discover -s tests -v
```

Inspect `output/alerts.csv`, `output/validation.json`, and `output/case_summary.md`.

## Example results

The sample data produces two alerts for fictional customer C001 (unusually large deposit and rapid cryptocurrency withdrawal), and flags two of three sample reporting records for manual review (amount mismatch and missing date).

## How this relates to AML operations

This prototype shows how simple automation can help analysts identify unusual activity, reconcile source information with reporting records, and prepare review packages. The rules are transparent and easy to test. A future iteration could support configurable scenarios, audit logging, approval workflows, and visualization.

## Important limitations

- **Not affiliated with or connected to Questrade, Coinsquare, or FINTRAC.** No real customer data, credentials, or production systems are used.
- Thresholds are **illustrative heuristics**, not regulatory thresholds, Questrade rules, or sufficient evidence of money laundering.
- Alerts do **not** establish reasonable grounds to suspect. An analyst must review the context and decide on escalation under applicable policies.
- The validation checks are **not** FINTRAC's official STR schema and cannot guarantee regulatory completeness.
- The tool does **not** submit STRs, contact customers, freeze accounts, or make automated reporting decisions.
- This educational prototype does not include production-grade security, access control, privacy safeguards, or complete input validation.

## Repository structure

- `data/`: synthetic CSV inputs
- `src/aml.py`: monitoring, validation, and reporting functions
- `tests/`: unit tests
- `output/`: generated demonstration outputs

## Interview walkthrough (30 seconds)

"In previous AML operations I prepared and submitted STRs through FINTRAC's platform. I built a small Python proof of concept that checks synthetic transactions for unusual patterns, reconciles reporting data against source records, and generates a case summary for analyst review. It demonstrates how automation could reduce repetitive checks while leaving investigative and reporting decisions to compliance professionals."
