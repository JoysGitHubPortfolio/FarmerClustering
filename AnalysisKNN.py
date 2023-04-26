#An application to generate data from Aspiring Panda Pilot WHO Farming Project
from matplotlib import pyplot as plt
from MyStatsFunctions import *
from GenerateMyDataFrame import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
import numpy as np

theoretical_df = GenerateMyDataFrame("subscriber_yield_export.csv", 1000)

# Make a binary classifier using K-nearest neighbour algorithm
x_data = np.array(theoretical_df["std_unit"])
y_data = np.array(theoretical_df["land_efficiency"])
x_max = max(x_data)
X = []
for val1, val2 in zip(x_data, y_data):
    X.append([val1, val2])
X = np.array(X)

kmeans = KMeans(n_clusters = 2)
kmeans.fit(X)
y = kmeans.labels_

clf = KNeighborsClassifier(n_neighbors = 3)
clf.fit(X, y)

xx, yy = np.meshgrid(np.linspace(0, x_max, 500), np.linspace(0, 1, 500))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

fig, ax = plt.subplots()
ax.contourf(xx, yy, Z, cmap = plt.cm.RdBu, alpha = 0.6)
ax.scatter(X[:,0], X[:,1], c = y, cmap = plt.cm.RdBu, alpha = 0.5, edgecolor = "white")
plt.xlabel("Standardized unit of sold quantities (kg)")
plt.ylabel("Land efficiency i.e. ratio of quantity produced to product yield")
plt.show()
