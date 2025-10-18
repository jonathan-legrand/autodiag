# %%
import numpy as np
import pandas as pd


# %%


rng = np.random.default_rng()
long_desc = pd.read_csv("data/datalong.csv", index_col=0)
# %%

long_scores = long_desc.copy()
long_scores["symptome"] = rng.normal(size=(len(long_desc)))
# %%
import seaborn as sns
import matplotlib.pyplot as plt

sorted_disorders = long_scores.groupby("code").sum().sort_values(
    by="symptome", ascending=False
)
most_likely_disorder = sorted_disorders.index[0]

