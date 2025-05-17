from sklearn.linear_model import LogisticRegression
import numpy as np

class MakerTakerModel:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)
        
    def predict_proba(self, features):
        return self.model.predict_proba([features])[0]