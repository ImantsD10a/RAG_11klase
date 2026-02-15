import os
import re

DOCS_DIR = "docs"
TOP_K = 3

# Palīgfunkcijas

def tokenize(text):
    """Sadala tekstu vārdos"""
    return re.findall(r"\w+", text.lower())

def load_documents():
    """Atrod un ielasa visus .txt failus"""
    documents = []

    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DOCS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            fragments = [p.strip() for p in text.split("\n\n") if p.strip()]

            for i, fragment in enumerate(fragments, start=1):
                documents.append({
                    "file": filename,
                    "fragment_id": i,
                    "text": fragment
                })

    return documents

def score_fragment(fragment_text, query_words):
    """Aprēķina keyword overlap punktus"""
    fragment_words = tokenize(fragment_text)
    return sum(1 for w in query_words if w in fragment_words)

# GALVENĀ LOĢIKA

def retrieve_fragments(query, documents):
    query_words = tokenize(query)
    results = []

    for doc in documents:
        score = score_fragment(doc["text"], query_words)
        if score > 0:
            results.append({**doc, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:TOP_K]

def generate_answer(sources):
    """Izveido atbildi tikai no avotiem"""
    if not sources:
        return None

    answer = " ".join(src["text"] for src in sources[:2])
    return answer

# MAIN

def main():
    documents = load_documents()

    query = input("Ievadi jautājumu: ")

    top_fragments = retrieve_fragments(query, documents)

    print("\nTOP 3 fragmenti:")
    for i, frag in enumerate(top_fragments, start=1):
        preview = frag["text"][:120].replace("\n", " ")
        print(f"{i}) {frag['file']} | fragments {frag['fragment_id']} | punkti: {frag['score']}")
        print(f"   → {preview}...\n")

    # 2 dala
    sources = top_fragments[:2]
    answer = generate_answer(sources)

    if answer:
        print("Atbilde:")
        print(answer)
        print("\nAvoti:")
        for s in sources:
            print(f"- {s['file']} | fragments {s['fragment_id']}")
    else:
        print("Nav pietiekamas informācijas dotajos avotos.")

if __name__ == "__main__":
    main()
