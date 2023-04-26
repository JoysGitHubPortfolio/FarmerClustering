#An application to generate data from Aspiring Panda Pilot WHO Farming Project
from matplotlib import pyplot as plt
from MyStatsFunctions import *
from GenerateMyDataFrame import *
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
import numpy as np

# Format the data
theoretical_df = GenerateMyDataFrame("subscriber_yield_export.csv", 1000)
x_data = np.array(theoretical_df["std_unit"])
y_data = np.array(theoretical_df["land_efficiency"])
x_max = max(x_data)
y_max = max(y_data)
X = []
for val1, val2 in zip(x_data, y_data):
    X.append([val1, val2])
X = np.array(X)

# Make a binary classifier using K-nearest neighbour algorithm
kmeans = KMeans(n_clusters = 2)
labels = kmeans.fit_predict(X)
kmeans.fit(X)

# Fit a logistic regression model to the data
logreg = LogisticRegression()
logreg.fit(X, labels)
slope = -logreg.coef_[0][0] / logreg.coef_[0][1]
intercept = -logreg.intercept_ / logreg.coef_[0][1]
xx, yy = np.meshgrid(np.linspace(0, x_max, 100),
                     np.linspace(0, y_max, 100))
Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot the data
divider = False
fig, ax = plt.subplots()
ax.scatter(X[:, 0], X[:, 1], c = labels, cmap = plt.cm.RdBu, alpha = 0.5, edgecolor = 'white')
if divider == True:
    ax2.plot(xx.ravel(), slope * xx.ravel() + intercept, 'b-')
plt.xlabel("Standardized unit of sold quantities (kg)")
plt.ylabel("Land efficiency i.e. ratio of quantity produced to product yield")
plt.show()
