import numpy as np


class Perceptron:
    def __init__(self, learning_rate=0.1, epochs=100):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0

    def activation(self, value):
        return 1 if value >= 0 else 0

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=int)

        self.weights = np.zeros(X.shape[1])
        self.bias = 0

        for epoch in range(self.epochs):
            errors = 0

            for i in range(len(X)):
                net_input = np.dot(X[i], self.weights) + self.bias
                prediction = self.activation(net_input)
                error = y[i] - prediction

                if error != 0:
                    self.weights += self.learning_rate * error * X[i]
                    self.bias += self.learning_rate * error
                    errors += 1

            if errors == 0:
                break

    def predict(self, X):
        X = np.array(X, dtype=float)
        predictions = []

        for row in X:
            net_input = np.dot(row, self.weights) + self.bias
            predictions.append(self.activation(net_input))

        return np.array(predictions)


if __name__ == "__main__":
    X = np.array([
        [0.8, 0.9, 1],
        [0.7, 0.8, 1],
        [0.5, 0.55, 0],
        [0.4, 0.45, 0]
    ])

    y = np.array([1, 1, 0, 0])

    model = Perceptron(learning_rate=0.1, epochs=100)
    model.fit(X, y)

    predictions = model.predict(X)

    print("Perceptron Training Completed")
    print("Weights:", model.weights)
    print("Bias:", model.bias)
    print("Actual:", y)
    print("Predictions:", predictions)
