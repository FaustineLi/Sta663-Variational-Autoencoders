import numpy as np

class Network:

    def __init__(self, dimensions, params):
        '''intializes weights matrix and parameters'''

        # initialize weights of network
        self.weights = {}
        for i in range(len(dimensions)-1):
            self.weights[i] = np.random.uniform(-0.1, 0.1, 
                    (dimensions[i], dimensions[i+1]))

        # hyperparameters
        self.alpha = params['alpha']
        self.iter = params['iter']
        self.activation = params['activation']
        self.grad_activation = params['grad_activation']
        self.loss = params['loss']
        self.grad_loss = params['grad_loss']
        self.batch_size = params['batch_size']

    def _feedforward(self, X):
        '''feedforward update step'''
        self.z = {}
        self.z_act = {0: X}

        for i in range(len(self.weights)):
            self.z[i] = self.z_act[i] @ self.weights[i]
            self.z_act[i+1] = self.activation(self.z[i])
        return self.z_act[i+1]

    def _backprop(self, X, y, yhat):
        '''back-propagation algorithm'''
        n = len(self.weights)
        delta = - self.grad_loss(y, yhat) * self.grad_activation(self.z[n-1])
        grad_weights = {n-1: self.z_act[n-1].T @ delta}

        for i in reversed(range(len(self.weights)-1)):
            delta = delta @ self.weights[i+1].T * self.grad_activation(self.z[i])
            grad_weights[i] = self.z_act[i].T @ delta

        return grad_weights

    def train(self, X, y):
        '''trains model using stochastic gradient descent'''
        X_batch = X
        y_batch = y

        for i in range(self.iter):

            if self.batch_size > 0 and self.batch_size < X.shape[0]:
                k = np.choice(range(X.shape[0]), self.batch_size, replace=False)
                X_batch = X[k,:]
                y_batch = y[k,:]

            yhat = self._feedforward(X_batch)
            grad_weights = self._backprop(X_batch, y_batch, yhat)

            for j in range(len(self.weights)):
                self.weights[j] -= self.alpha * grad_weights[j]

    def predict(self, X):
        '''predicts on trained model'''
        for i in range(len(self.weights)):
            z = z_act @ self.weights[i]
            z_act = self.activation(z)
        return z_act
