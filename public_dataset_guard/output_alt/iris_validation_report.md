<!--
CARDO REI methodology applied to this document.
Reference: [CARDO REI Methodology](PROMPTHOUND-DOCS/CARDO-REI.md)
-->

# Iris Sample Validation Report

## What this tool does
It loads a small public Iris sample, scores each row with a simple rule, and uses a cost-weighted gate to decide whether the rule is worth trusting in this slice.

## Setup
- Dataset: iris_sample.csv
- Rows: 17
- Positive class: virginica
- Score rule: 1.1 * petal_length + 2.0 * petal_width - 0.2 * sepal_width
- Threshold: 8.60
- Cost to act: 8.00
- Cost of missing: 18.00

## Results
- Accuracy: 100.00%
- Precision: 100.00%
- Recall: 100.00%
- True positives: 5
- True negatives: 12
- False positives: 0
- False negatives: 0

## Cost gate
- False alarm rate: 0.00%
- Miss rate: 0.00%
- Expected action waste: $0.00
- Expected miss loss: $0.00
- Decision: HOLD

## Highest scores
- score=10.94 pred=P actual=P species=virginica (6.3, 3.3, 6.0, 2.5)
- score=10.18 pred=P actual=P species=virginica (6.5, 3.0, 5.8, 2.2)
- score=10.09 pred=P actual=P species=virginica (7.1, 3.0, 5.9, 2.1)

## Lowest scores
- score=1.19 pred=N actual=N species=setosa (4.7, 3.2, 1.3, 0.2)
- score=1.22 pred=N actual=N species=setosa (5.0, 3.6, 1.4, 0.2)
- score=1.24 pred=N actual=N species=setosa (5.1, 3.5, 1.4, 0.2)

## Limitations
- This is a small sample, not the full Iris dataset.
- The scoring rule is intentionally simple and not tuned for best accuracy.
- The cost numbers are synthetic and are here to show the decision gate, not to represent a real business case.
- A different threshold would change the confusion matrix and the decision.
- This report is useful for checking the shape of the workflow, not for proving the rule is optimal.
