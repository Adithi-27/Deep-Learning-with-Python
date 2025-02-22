# -*- coding: utf-8 -*-
"""backpropagation-regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NHbUBvfd7jP8WhhuyF3K0sLSK7KMLA5_
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BackpropagationRegression:
    def __init__(self, layer_dims=[2,2,1], learning_rate=0.001):
        self.layer_dims = layer_dims
        self.learning_rate = learning_rate
        self.parameters = self.initialize_parameters()
        self.loss_history = []

    def initialize_parameters(self):
        np.random.seed(3)
        parameters = {}
        L = len(self.layer_dims)

        for l in range(1, L):
            parameters['W' + str(l)] = np.random.randn(self.layer_dims[l-1], self.layer_dims[l]) * 0.01
            parameters['b' + str(l)] = np.zeros((self.layer_dims[l], 1))

        return parameters

    def linear_forward(self, A_prev, W, b):
        Z = np.dot(W.T, A_prev) + b
        return Z

    def forward_propagation(self, X):
        A = X
        L = len(self.parameters) // 2

        for l in range(1, L+1):
            A_prev = A
            Wl = self.parameters['W' + str(l)]
            bl = self.parameters['b' + str(l)]
            A = self.linear_forward(A_prev, Wl, bl)

        return A, A_prev

    def update_parameters(self, y, y_hat, A1, X):
        # Compute gradients and update weights
        error = y - y_hat

        # Output layer updates
        self.parameters['W2'][0][0] += self.learning_rate * 2 * error * A1[0][0]
        self.parameters['W2'][1][0] += self.learning_rate * 2 * error * A1[1][0]
        self.parameters['b2'][0][0] += self.learning_rate * 2 * error

        # Hidden layer updates
        self.parameters['W1'][0][0] += self.learning_rate * 2 * error * self.parameters['W2'][0][0] * X[0][0]
        self.parameters['W1'][0][1] += self.learning_rate * 2 * error * self.parameters['W2'][0][0] * X[1][0]
        self.parameters['b1'][0][0] += self.learning_rate * 2 * error * self.parameters['W2'][0][0]

        self.parameters['W1'][1][0] += self.learning_rate * 2 * error * self.parameters['W2'][1][0] * X[0][0]
        self.parameters['W1'][1][1] += self.learning_rate * 2 * error * self.parameters['W2'][1][0] * X[1][0]
        self.parameters['b1'][1][0] += self.learning_rate * 2 * error * self.parameters['W2'][1][0]

    def train(self, X, y, epochs=100):
        for epoch in range(epochs):
            epoch_loss = []
            for i in range(X.shape[0]):
                x_sample = X[i].reshape(-1, 1)
                y_sample = y[i]

                y_hat, A1 = self.forward_propagation(x_sample)
                y_hat = y_hat[0][0]

                self.update_parameters(y_sample, y_hat, A1, x_sample)
                epoch_loss.append((y_sample - y_hat)**2)

            mean_loss = np.mean(epoch_loss)
            self.loss_history.append(mean_loss)
            print(f'Epoch {epoch+1}, Loss: {mean_loss}')

    def predict(self, X):
        predictions = []
        for sample in X:
            x_sample = sample.reshape(-1, 1)
            prediction, _ = self.forward_propagation(x_sample)
            predictions.append(prediction[0][0])
        return np.array(predictions)

    def plot_loss(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.loss_history)
        plt.title('Training Loss over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Mean Squared Error')
        plt.show()

    def performance_metrics(self, X, y):
        predictions = self.predict(X)
        mse = np.mean((y - predictions)**2)
        mae = np.mean(np.abs(y - predictions))
        r2 = 1 - (np.sum((y - predictions)**2) / np.sum((y - np.mean(y))**2))

        print("\nModel Performance:")
        print(f"Mean Squared Error: {mse}")
        print(f"Mean Absolute Error: {mae}")
        print(f"R-squared Score: {r2}")

        plt.figure(figsize=(10, 5))
        plt.scatter(y, predictions, color='blue', label='Actual vs Predicted')
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', label='Perfect Prediction')
        plt.title('Actual vs Predicted Values')
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.legend()
        plt.show()

# Example usage
df = pd.DataFrame([[8,8,4],[7,9,5],[6,10,6],[5,12,7]], columns=['cgpa', 'profile_score', 'lpa'])

X = df[['cgpa', 'profile_score']].values
y = df['lpa'].values

# Train the model
model = BackpropagationRegression(layer_dims=[2,2,1], learning_rate=0.01)
model.train(X, y, epochs=500)

# Plot loss and analyze performance
model.plot_loss()
model.performance_metrics(X, y)