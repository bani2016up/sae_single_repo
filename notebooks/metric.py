import json

from sklearn.metrics import classification_report


def paragraph_classification_report(
    true_suggestions: list[list[str]],
    pred_suggestions: list[list[str]],
    output_dict: bool = False
) -> str:
    y_true = [1 if len(tr) > 0 else 0 for tr in true_suggestions]
    y_pred = [1 if len(pr) > 0 else 0 for pr in pred_suggestions]
    return classification_report(
        y_true, y_pred,
        target_names=["no_error", "error"],
        digits=3,
        zero_division=0.0,
        output_dict=output_dict
    )


def sentence_classification_report(
    texts: list[str],
    true_suggestions: list[list[str]],
    pred_suggestions: list[list[str]],
    nlp,
    output_dict: bool = False
) -> str:
    y_true, y_pred = [], []
    for text, trues, preds in zip(texts, true_suggestions, pred_suggestions):
        doc = nlp(text)
        for sent in doc.sents:
            sent_text = sent.text
            true_flag = any(err in sent_text for err in trues)
            pred_flag = any(err in sent_text for err in preds)
            y_true.append(1 if true_flag else 0)
            y_pred.append(1 if pred_flag else 0)
    return classification_report(
        y_true, y_pred,
        target_names=["no_error", "error"],
        digits=3,
        zero_division=0.0,
        output_dict=output_dict
    )


def suggestion_level_metrics(
    true_suggestions: list[list[str]],
    pred_suggestions: list[list[str]]
) -> dict:
    tp = fp = fn = 0
    for trues, preds in zip(true_suggestions, pred_suggestions):
        set_true = set(trues)
        set_pred = set(preds)
        tp += len(set_true & set_pred)
        fp += len(set_pred - set_true)
        fn += len(set_true - set_pred)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def parse_suggestions_column(json_str: str) -> list[str]:
    data = json.loads(json_str)
    return [str(item) for item in data]