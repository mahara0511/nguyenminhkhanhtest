def build_prompt(state):
    context = "\n---\n".join(state["retrieved_chunks"])

    urls = []
    seen = set()
    for m in state.get("retrieved_metadata", []):
        url = m.get("url")
        if url and url not in seen:
            seen.add(url)
            urls.append(url)
        if len(urls) == 3:
            break

    cited_block = "\n".join(f"- {u}" for u in urls) if urls else "None"
    first_url = urls[0] if urls else "None"

    prompt = f"""
You are OptiBot, the customer-support bot for OptiSigns.com.
Use ONLY the content inside DOCUMENTS.
Never hallucinate or guess.

=== DOCUMENTS ===
{context}

=== QUESTION ===
{state['query']}

=== CITED URLS ===
{cited_block}

Now follow ALL rules below and produce the answer:

=== MANDATORY RULES ===
1. Your answer MUST contain **no more than 5 bullet points**.
2. Your answer MUST include **at least one URL** from CITED URLS {cited_block}.
3. DO NOT mention DOCUMENTS, CITED URLS, or rules.
4. Output MUST be ONLY bullet points + final line.
5. NO extra text outside bullet points.

=== FINAL LINE (MANDATORY) ===


Begin your answer now.
"""
    # print(prompt)
    return {"prompt": prompt}
