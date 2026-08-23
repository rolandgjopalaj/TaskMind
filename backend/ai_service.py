import json
import ollama

MODEL_NAME = "llama3.2"


def classify_task_AI(description: str) -> dict:
    prompt = f"""Classifica il seguente task in:
- una categoria tra: lavoro, personale, studio, urgente
- una priorità tra: bassa, media, alta

Task: "{description}"

Rispondi SOLO con un oggetto JSON in questo formato esatto, senza altro testo, senza markdown, senza spiegazioni:
{{"category": "...", "priority": "..."}}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={"temperature": 0}
    )

    raw_text = response["message"]["content"].strip()

    try:
        result = json.loads(raw_text)
        return {
            "category": result.get("category", "personale"),
            "priority": result.get("priority", "media"),
        }
    except json.JSONDecodeError:
        return {"category": "personale", "priority": "media"}
