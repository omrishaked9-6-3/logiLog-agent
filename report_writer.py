import json

def write_report(alerts, output_path):
    """
    Saves the final list of interpreted alerts to a JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2, ensure_ascii=False)
