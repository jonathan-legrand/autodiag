# %%
from openai import OpenAI
import numpy as np
import pandas as pd

MODEL = "text-embedding-embeddinggemma-300m-qat"
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
def get_embedding(text, model="model-identifier"):
   text = text.replace("\n", " ")
   
   embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
   return np.array(embedding)

df = pd.read_csv("~/Datasets/hack1robo/data.csv", index_col=0)

# %%
desc = df.description.sample(n=1).values[0]
embed = get_embedding(desc)

# %%
embeddings = []
for idx, row in df.iterrows():
   embed = get_embedding(row.description)
   embeddings.append(embed)


# %%
X = np.stack(embeddings)
embedding_cols = [f"x_{i}" for i in range(X.shape[1])]
X_df = pd.DataFrame(X, columns=embedding_cols)
pd.concat((df, X_df), axis=1).to_csv("desc_embedding.csv")
# %%
from sklearn.manifold import TSNE

tsne_res = TSNE(perplexity=10).fit_transform(X)
# %%
import matplotlib.pyplot as plt
import seaborn as sns
plt.subplots(figsize=(10,7))
tsne_df = pd.DataFrame(
   tsne_res,
   index=df.chapter.astype(str),
   columns=("tsne_1", "tsne_2"),
)
sns.scatterplot(
   tsne_df, x="tsne_1", y="tsne_2", hue="chapter", legend="brief"
)
plt.title("Disorder description embedding")
plt.show()
# %%
# Language disorder (F80.2)
#candidate_sentence = "Every day I know what I want to say, but the words just won’t come out right, and it’s so frustrating."

# Dissociative identity disorder (F44.81)
candidate_sentence = "Some days I feel like I’m not the only one living my life, and it’s confusing trying to figure out who’s really in control."

candidate_emb = get_embedding(candidate_sentence)

sims = X @ candidate_emb # Embeddings are L2-normalized
plt.hist(sims.flatten())
plt.title("Distribution of candidate to descriptions similarities ")
plt.xlabel("Cosine similarity")
max_idx = np.argmax(sims.flatten())

print(df.loc[max_idx, "description"])
print(df.loc[max_idx, "code"])

# %%
max_indices = np.argsort(sims)[::-1]

for i in range(5):
   max_idx = max_indices[i]
   print(df.loc[max_idx, "code"] + f" sim = {sims[max_idx]}")
   print(df.loc[max_idx, "description"])
# %%
print(df.loc[max_indices[i], "description"])
# %%
a = get_embedding("Homme")
b = get_embedding("Animal")

a.T @ b
   
