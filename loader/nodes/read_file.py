# nodes/read_files.py
def read_file(state):
    path = state["current_file"]
    with open(path, "r", encoding="utf-8") as f:
        return {"file_text": f.read()}
