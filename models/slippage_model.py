from sklearn.linear_model import LinearRegression
import numpy as np

class SlippageModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, features):
        return self.model.predict([features])[0]