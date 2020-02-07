# load data from file to DataFrame
import pandas as pd

df = pd.read_csv (r'OrganicDigital/export.csv')
print (df)

import matplotlib.pyplot as plt

labels = 'Birkenhead', 'Bootle', 'Bradford', 'Bury', 'Cannock'
sizes = [233, 60, 22, 493, 204]
colors = ['green', 'green', 'orange', 'orange', 'orange']
explode = (0.05, 0.05, 0.05, 0.05, 0.05)
patches, texts = plt.pie(sizes, colors=colors, labels=labels, shadow=False, startangle=90, wedgeprops={"edgecolor":"k", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True})
plt.axis('equal')
plt.tight_layout()
plt.show()
