import pandas as pd

def normalize(text):
    return text.lower().rstrip('s')  # simple singularization


def flatten_predictions(predictions):
    rows = []
    for msg_id, pred in enumerate(predictions):
        person = pred.get("person", "").strip()

        for item in pred.get("expenses", []):
            rows.append({
                "message_id": msg_id,
                "person": person,
                "item_name": item.get("name", "").lower(),
                "amount": int(item.get("amount", 0))
            })

    return pd.DataFrame(rows)


def compute_metrics(pred_df, gt_df):
    pred_set = set(tuple(x) for x in pred_df.values)
    gt_set = set(tuple(x) for x in gt_df.values)

    tp = len(pred_set & gt_set)
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    precision = tp / (tp + fp) if tp else 0
    recall = tp / (tp + fn) if tp else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

    return precision, recall, f1