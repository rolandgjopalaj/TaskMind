import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import joblib

dataframe = pd.read_csv("dataset.csv")

#custruire una pipeline
##e' fondamentale fare un pipeline e non step separati perche se no si rischia data leakage (La Pipeline garantisce che fit avvenga solo sui dati di train.)
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2), # cattura non solo singole parole ma anche coppie (es. "entro oggi") che spesso portano più segnale delle singole parole isolate.
        min_df=2,  #ignora parole che compaiono una sola volta in tutto il train set
        sublinear_tf=True
    )),
    ("clf", MultinomialNB()) #il migliore trovato
])

#addestrare il modelo finale (dopo che abiamo valutato possiamo addestrarlo su tutto il dataset)
pipeline.fit(dataframe["description"], dataframe["category"])

joblib.dump(pipeline, "category_classifier_model.joblib")
