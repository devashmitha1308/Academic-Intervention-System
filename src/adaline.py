import numpy as np


class ADALINE:
    def __init__(self, learning_rate=0.01, epochs=100):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        self.weights = np.zeros(X.shape[1])
        self.bias = 0

        for epoch in range(self.epochs):
            net_input = np.dot(X, self.weights) + self.bias
            errors = y - net_input

            self.weights += self.learning_rate * np.dot(X.T, errors)
            self.bias += self.learning_rate * np.sum(errors)

    def predict(self, X):
        X = np.array(X, dtype=float)

        net_input = np.dot(X, self.weights) + self.bias

        predictions = []

        for value in net_input:
            if value >= 0.5:
                predictions.append(1)
            else:
                predictions.append(0)

        return np.array(predictions)


if __name__ == "__main__":
    X = np.array([
        [0.8, 0.9, 1],
        [0.7, 0.8, 1],
        [0.5, 0.55, 0],
        [0.4, 0.45, 0]
    ])

    y = np.array([1, 1, 0, 0])

    model = ADALINE(learning_rate=0.01, epochs=100)

    model.fit(X, y)

    predictions = model.predict(X)

    print("ADALINE Training Completed")
    print("Weights:", model.weights)
    print("Bias:", model.bias)
    print("Actual:", y)
    print("Predictions:", predictions)
