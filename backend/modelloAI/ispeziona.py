import pandas as pd

df = pd.read_csv("dataset.csv")

print("\nshape:")
print(df.shape)                    # ti aspetti (400, 2)

print("\nnr per categoria:")
print(df["category"].value_counts())  # deve dare ~100 per categoria

print("\nvalori mancanti:")
print(df.isnull().sum())           # controlla valori mancanti

print("\ndublicati:")
print(df.duplicated(subset="description").sum())  # controlla duplicati


#solo se ci sono duplicati
#df = df.drop_duplicates(subset="text").reset_index(drop=True)