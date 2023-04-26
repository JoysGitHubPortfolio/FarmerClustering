#An application to generate data from Aspiring Panda Pilot WHO Farming Project
from matplotlib import pyplot as plt
from MyStatsFunctions import *
from GenerateMyDataFrame import *
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
import numpy as np

theoretical_df = GenerateMyDataFrame("subscriber_yield_export.csv", 1000)

# Plot the data and observe trends
fig, ax = plt.subplots(figsize=(1,1))
for n, grp in theoretical_df.groupby("district_name"):
    ax.scatter(x = "std_unit", y = "land_efficiency", data=grp, label=n, alpha = 0.25)
ax.legend(title="Label")
plt.xlabel("Standardized unit of sold quantities (kg)")
plt.ylabel("Land efficiency i.e. ratio of quantity produced to product yield")
plt.show()
