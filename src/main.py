import pandas as pd
from extractor import extract_order
from evaluator import flatten_predictions, compute_metrics

def load_messages(path):
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def main():
    messages = load_messages("data/messages.txt")
    gt_df = pd.read_csv("data/ground_truth.csv")

    predictions = []

    print("🔍 Extracting orders...\n")
    for i, msg in enumerate(messages):
        result = extract_order(msg)
        predictions.append(result)
        print(f"[{i}] {result}")

    pred_df = flatten_predictions(predictions)

    precision, recall, f1 = compute_metrics(pred_df, gt_df)

    print("\n📊 Evaluation Results:")
    print(f"Precision: {precision:.2f}")
    print(f"Recall:    {recall:.2f}")
    print(f"F1-score:  {f1:.2f}")


if __name__ == "__main__":
    main()