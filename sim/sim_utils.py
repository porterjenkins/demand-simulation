import numpy as np

def softmax(x):
    p = np.exp(x) / np.exp(x).sum()
    return p