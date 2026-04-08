import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Sample dataset
# Time vs Usage
time = np.array([[9],[10],[11],[12],[1],[2],[3],[4],[5]])
usage = np.array([20,35,50,80,60,45,40,30,25])

model = LinearRegression()
model.fit(time, usage)

# Save Model
pickle.dump(model, open("model.pkl","wb"))

print("Model Trained Successfully")
