# TaskMind

Un'app per gestire attività ("task") scritte in linguaggio naturale. L'utente scrive cosa deve fare, e il sistema capisce da solo a che **categoria** appartiene il task (lavoro, personale, studio, urgente).

## Come funziona, in breve

1. L'utente crea un task con un titolo e una descrizione (es. *"Preparare la presentazione per il cliente entro venerdì"*).
2. Il task viene salvato in un database.
3. Quando lo si aggiorna, il testo della descrizione viene passato a un modello di intelligenza artificiale, che restituisce la categoria giusta.
4. Il task viene aggiornato nel database con la categoria trovata.

## Le due strade per la classificazione

Nel progetto ci sono **due modi diversi** per classificare un task, entrambi implementati in `ai_service.py`:

- **`classify_task_AI`** → usa un LLM (Llama 3.2, eseguito in locale con Ollama). Gli si manda un prompt che chiede di rispondere con categoria e priorità in formato JSON.
- **`classify_task_MyAiModel`** → usa un modello di machine learning **allenato da me**, salvato come file `.joblib`. Non chiama nessun servizio esterno: la previsione è immediata e gira in locale.

Nel backend (`main.py`) è quest'ultimo quello attualmente in uso, perché è più veloce e non dipende da un modello LLM in esecuzione.

## Come è stato creato il modello personalizzato

Questa è la parte in più rispetto all'idea di partenza: invece di affidarsi solo a un LLM esterno, ho costruito un classificatore addestrato su dati creati apposta.

1. **Generazione dei dati** – Ho usato Claude per generare, categoria per categoria, un centinaio di esempi realistici di task scritti come li scriverebbe davvero una persona (frasi corte e lunghe, imperative e colloquiali, con e senza parole esplicite come "lavoro").

   Esempio di prompt usato (uno per ogni categoria, qui quello per "lavoro"):

   > Genera 100 esempi realistici di task/attività scritti in linguaggio naturale italiano che una persona potrebbe scrivere in un'app di task management, tutti appartenenti alla categoria "lavoro" (attività professionali, ufficio, riunioni, progetti, colleghi, clienti, scadenze lavorative).
   >
   > Requisiti importanti per la varietà:
   > - Mescola frasi brevi (4-6 parole) e più lunghe (15-25 parole)
   > - Alcuni in forma imperativa ("Preparare il report"), altri come promemoria ("Devo finire...", "Ricordarmi di..."), altri più colloquiali
   > - Includi diversi contesti: riunioni, email, scadenze, presentazioni, colleghi, capo, clienti, progetti IT, amministrazione, viaggi di lavoro
   > - NON iniziare sempre le frasi allo stesso modo
   > - NON usare sempre la parola "lavoro" o "ufficio" esplicitamente nel testo (deve essere implicito dal contesto, come nella realtà)
   > - Alcuni con dettagli specifici (nomi progetto fittizi, orari, giorni della settimana), altri più generici
   > - Evita ripetizioni tra un esempio e l'altro
   >
   > Output SOLO in formato CSV, senza intestazione, senza spiegazioni, senza testo prima o dopo. Formato di ogni riga:
   > `"testo del task",lavoro`
   >
   > Genera esattamente 100 righe.

   Lo stesso prompt è stato ripetuto cambiando solo la categoria finale (`personale`, `studio`, `urgente`), per generare un dataset bilanciato.

2. **Unione dei dati** (`merge_csv.py`) – Tutti i file CSV generati (uno per categoria) vengono uniti in un unico dataset e poi mescolati, così le categorie non restano a blocchi separati.
3. **Controllo qualità del dataset** (`ispeziona.py`) – Verifico che il dataset abbia il numero di righe atteso, che le categorie siano bilanciate, che non ci siano valori mancanti o righe duplicate.
4. **Confronto tra modelli** (`confront_training.py`) – Ho provato tre algoritmi diversi (Regressione Logistica, SVM lineare, Naive Bayes) usando TF-IDF per trasformare il testo in numeri, valutandoli con cross-validation e guardando anche gli errori di classificazione.
5. **Addestramento del modello finale** (`train_model.py`) – Una volta scelto l'algoritmo migliore (Naive Bayes), l'ho allenato su tutto il dataset e salvato in un file `.joblib`, pronto per essere usato dal backend.

## Il backend (API)

Costruito con **FastAPI** (`main.py`), con queste operazioni:

| Metodo | Endpoint | Cosa fa |
|---|---|---|
| GET | `/tasks` | restituisce tutti i task |
| POST | `/tasks` | crea un nuovo task |
| PUT | `/tasks/{id}` | classifica il task con l'AI e aggiorna categoria/priorità |
| DELETE | `/tasks/{id}` | elimina un task |

Il database (`database.py`) è una semplice tabella SQLite con titolo, descrizione, categoria, priorità e stato di completamento.

## Come avviare il progetto

```
source venv/bin/activate
uvicorn main:app --reload     # avvia il server API
ollama serve                  # se si vuole usare la classificazione via LLM
```

## Struttura dei file

- `main.py` – API e logica delle richieste
- `database.py` – connessione e creazione del database
- `ai_service.py` – le due funzioni di classificazione (LLM e modello proprio)
- `merge_csv.py` – unisce i CSV generati in un unico dataset
- `ispeziona.py` – controlla la qualità del dataset
- `confront_training.py` – confronta diversi algoritmi di classificazione
- `train_model.py` – allena e salva il modello finale

## Prossimi passi possibili

- Aggiungere un frontend React per interagire con l'app senza usare direttamente le API.
- Scrivere test automatici con `pytest` per il backend.
- Aggiungere anche la stima della **priorità** al modello personalizzato (per ora prevede solo la categoria).
- Provare a mettere online il progetto (es. Azure) per avere un'esperienza pratica di deploy.