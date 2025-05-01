import json

from pathlib import Path
from tqdm.auto import tqdm

def fix_widget_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    widgets_meta = nb.get("metadata", {}).get("widgets")
    if widgets_meta:
        app_json = widgets_meta.get("application/vnd.jupyter.widget-state+json")
        if app_json and "state" not in app_json:
            app_json["state"] = {}
            print(f"Patched 'state' key in: {file_path}")
        else:
            print(f"No patch needed: {file_path}")
    else:
        print(f"No 'widgets' metadata in: {file_path}")
        return

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)


notebooks_dir = Path("./")
for notebook in tqdm(notebooks_dir.glob("*.ipynb"), desc="Fixing notebooks"):
    fix_widget_metadata(notebook)
