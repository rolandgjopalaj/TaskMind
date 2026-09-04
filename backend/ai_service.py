import json
import ollama
import joblib
import logging

MODEL_NAME = "llama3.2"

MODEL_PATH = "modelloAI/category_classifier_model.joblib"

logger = logging.getLogger(__name__)

_myAiModel = None
_model_load_error = None

def _get_model():
    global _myAiModel, _model_load_error
    if _myAiModel is None and _model_load_error is None:
        try:
            _myAiModel = joblib.load(MODEL_PATH)
        except (FileNotFoundError, OSError, Exception) as e:
            _model_load_error = str(e)
            logger.error(f"Impossibile caricare il modello AI: {e}")
    return _myAiModel


def classify_task_MyAiModel(description: str) -> dict:
    if not description or not description.strip():
        return {"category": "personale", "priority": "", "error": "descrizione vuota"}

    model = _get_model()
    if model is None:
        return {"category": "personale", "priority": "", "error": "modello non disponibile"}

    try:
        category = model.predict([description])
        return {"category": str(category[0]), "priority": ""}
    except Exception as e:
        logger.error(f"Errore durante la classificazione: {e}")
        return {"category": "personale", "priority": "", "error": "classificazione fallita"}



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
