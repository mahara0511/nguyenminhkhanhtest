# assistant/nodes/format_output.py
def format_output(state):
    final = state["answer"]

    # Enforce bullet point rule
    lines = final.split("\n")
    if len(lines) > 5:
        final = "\n".join(lines[:5]) + "\n\n(See article for more details.)"

    return {"answer": final}
