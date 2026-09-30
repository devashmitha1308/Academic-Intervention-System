import numpy as np


class BPN:
    def __init__(self, learning_rate=0.5, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs

        self.weights_input_hidden = None
        self.weights_hidden_output = None

        self.bias_hidden = None
        self.bias_output = None

    def sigmoid(self, value):
        return 1 / (1 + np.exp(-value))

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float).reshape(-1, 1)

        np.random.seed(42)

        input_size = X.shape[1]
        hidden_size = 4
        output_size = 1

        self.weights_input_hidden = np.random.uniform(
            -0.5, 0.5, (input_size, hidden_size)
        )

        self.weights_hidden_output = np.random.uniform(
            -0.5, 0.5, (hidden_size, output_size)
        )

        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))

        for epoch in range(self.epochs):

            hidden_input = np.dot(
                X, self.weights_input_hidden
            ) + self.bias_hidden

            hidden_output = self.sigmoid(hidden_input)

            final_input = np.dot(
                hidden_output, self.weights_hidden_output
            ) + self.bias_output

            final_output = self.sigmoid(final_input)

            output_error = y - final_output

            output_delta = (
                output_error
                * final_output
                * (1 - final_output)
            )

            hidden_error = np.dot(
                output_delta,
                self.weights_hidden_output.T
            )

            hidden_delta = (
                hidden_error
                * hidden_output
                * (1 - hidden_output)
            )

            self.weights_hidden_output += (
                self.learning_rate
                * np.dot(hidden_output.T, output_delta)
            )

            self.bias_output += (
                self.learning_rate
                * np.sum(output_delta, axis=0, keepdims=True)
            )

            self.weights_input_hidden += (
                self.learning_rate
                * np.dot(X.T, hidden_delta)
            )

            self.bias_hidden += (
                self.learning_rate
                * np.sum(hidden_delta, axis=0, keepdims=True)
            )

    def predict(self, X):
        X = np.array(X, dtype=float)

        hidden_input = np.dot(
            X, self.weights_input_hidden
        ) + self.bias_hidden

        hidden_output = self.sigmoid(hidden_input)

        final_input = np.dot(
            hidden_output, self.weights_hidden_output
        ) + self.bias_output

        final_output = self.sigmoid(final_input)

        predictions = []

        for value in final_output:
            if value[0] >= 0.5:
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

    model = BPN(
        learning_rate=0.5,
        epochs=1000
    )

    model.fit(X, y)

    predictions = model.predict(X)

    print("BPN Training Completed")
    print("Actual:", y)
    print("Predictions:", predictions)
