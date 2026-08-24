import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
import numpy as np

dataframe = pd.read_csv("dataset.csv")

#dividere i dati in training set e in test set
X_train, X_test, y_train, y_test = train_test_split(
    dataframe["description"], dataframe["category"],
    test_size=0.2, # 20% dei dati per il test
    stratify=dataframe["category"], #per mantenere le proporzioni tra le categorie
    random_state=42 
)

#Provare a confrontare i diversi classificatori
for name, clf in [("LogReg", LogisticRegression(max_iter=1000, class_weight="balanced")),
                   ("LinearSVC", LinearSVC(class_weight="balanced")),
                   ("NaiveBayes", MultinomialNB())]:
    print(f"\n\n##########################\nLe metriche per: {name}")
    pipeline = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=2)), ("clf", clf)])

    scores = cross_val_score(pipeline, dataframe["description"], dataframe["category"], cv=5, scoring="f1_macro")
    print(f"{name}: {scores.mean():.3f} ± {scores.std():.3f}")

    pipeline.fit(X_train, y_train)

    #test di predict
    y_pred = pipeline.predict(X_test)

    #visualizzare il paragone
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred, labels=pipeline.classes_))
    print(pipeline.classes_)  # per leggere la confusion matrix correttamente

    errors = X_test[y_test != y_pred]
    errors_df = pd.DataFrame({"text": errors, "vero": y_test[errors.index], "predetto": y_pred[y_test.index.get_indexer(errors.index)]})
    print(errors_df)


    