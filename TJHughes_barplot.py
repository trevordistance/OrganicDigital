import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(10, 10))

import pandas as pd

ratings = pd.read_csv('OrganicDigital/TJHughes.csv')

sns.set_color_codes("pastel")
sns.barplot(x="Store", y="Rating", data=ratings,
            label="Total", color="b")
