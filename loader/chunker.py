import re

def chunk_markdown(text: str, max_chars=800, overlap=200):

    def has_heading(t):
        return bool(re.search(r"^#{2,3}\s", t, flags=re.MULTILINE))

    def chunk_by_heading(t):
        parts = re.split(r"(?=^#{2,3}\s)", t, flags=re.MULTILINE)
        return [p.strip() for p in parts if p.strip()]

    def recursive_chunk(t, max_chars, overlap):
        chunks = []
        start = 0
        length = len(t)
        while start < length:
            end = min(start + max_chars, length)
            chunk = t[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if(end >= length):
                break
            start = end - overlap
        return chunks

    if has_heading(text):
        raw = chunk_by_heading(text)        
        final = []
        for c in raw:
            if len(c) > max_chars:
                final.extend(recursive_chunk(c, max_chars, overlap))
            else:
                final.append(c)
        return final

    return recursive_chunk(text, max_chars, overlap)
