import pandas as pd
import glob

#inserisce tutti i path files in una lista
file_paths = glob.glob("task_*.csv")

#legge tutti i file e li inserisce in una lista
dataframes = [pd.read_csv(f, header=None, names=["description", "category"]) for f in file_paths]

dataframes_unito = pd.concat(dataframes, ignore_index=True)

#mescolare i dati (perche' ora sono a blocchi divisi in categorie) serve per un training migliore
dataframes_unito = dataframes_unito.sample(frac=1, random_state=42).reset_index(drop=True)


#salvataggio
dataframes_unito.to_csv("dataset.csv", index=False)