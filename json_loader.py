import json


def json_saver(items, path):
    """Saving data to json"""
    try:
        with open(path, "w", newline="", encoding="utf-8") as file:
            json.dump(items, file, indent=3, ensure_ascii=False)
        print(f"The information was written to the {path} successfully")
    except Exception as e:
        print(e)
