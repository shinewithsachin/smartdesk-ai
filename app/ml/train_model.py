import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier

df = pd.read_csv("app/ml/dataset.csv")

X = df['description']
y = df[['category', 'priority']]


pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', MultiOutputClassifier(RandomForestClassifier(n_estimators=100)))
])

print("Training model...")
pipeline.fit(X, y)

joblib.dump(pipeline, "app/ml/ticket_classifier.joblib")
print("Model saved to app/ml/ticket_classifier.joblib")