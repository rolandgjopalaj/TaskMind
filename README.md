# TaskMind
Un'app di gestione attività dove l'utente scrive un task in linguaggio naturale, e un modello AI lo categorizza e riassume automaticamente

##Istruzioni
uvicorn main:app --reload     //per attivare il server in ascolto
ollama serve                  //per attivare il modello ai llama


##Training del modello 
i dati sono stati generati da claude con quest0 prompt (per ogni categoria):
Genera 100 esempi realistici di task/attività scritti in linguaggio naturale italiano che una persona potrebbe scrivere in un'app di task management, tutti appartenenti alla categoria "lavoro" (attività professionali, ufficio, riunioni, progetti, colleghi, clienti, scadenze lavorative).
Requisiti importanti per la varietà:
- Mescola frasi brevi (4-6 parole) e più lunghe (15-25 parole)
- Alcuni in forma imperativa ("Preparare il report"), altri come promemoria ("Devo finire...", "Ricordarmi di..."), altri più colloquiali
- Includi diversi contesti: riunioni, email, scadenze, presentazioni, colleghi, capo, clienti, progetti IT, amministrazione, viaggi di lavoro
- NON iniziare sempre le frasi allo stesso modo
- NON usare sempre la parola "lavoro" o "ufficio" esplicitamente nel testo (deve essere implicito dal contesto, come nella realtà)
- Alcuni con dettagli specifici (nomi progetto fittizi, orari, giorni della settimana), altri più generici
- Evita ripetizioni tra un esempio e l'altro
Output SOLO in formato CSV, senza intestazione, senza spiegazioni, senza testo prima o dopo. Formato di ogni riga:
"testo del task",lavoro
Genera esattamente 100 righe.

###successivamente si usa lo script merge_csv.py per fare il merge di tutti i dataset generati e infine si ispeziona il dataset completo con ispeziona.py