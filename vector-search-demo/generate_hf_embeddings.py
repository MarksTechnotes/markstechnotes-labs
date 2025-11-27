# Install required packages first:
# pip install pandas sentence-transformers

import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import json

# -----------------------------
# 1. Load CSV
# -----------------------------
# Automatically use the script's folder as base path
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "amazon.csv")

df = pd.read_csv(csv_path)

# -----------------------------
# 2. Combine text fields
# -----------------------------
def create_text(row):
    return f"{row['product_name']} {row.get('about_product', '')} " \
           f"{row.get('review_title', '')} {row.get('review_content', '')}"

df["embedding_text"] = df.apply(create_text, axis=1)

# -----------------------------
# 3. Load Hugging Face embedding model
# -----------------------------
# You can change the model to any sentence-transformers model you like
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# -----------------------------
# 4. Generate embeddings
# -----------------------------
embeddings = model.encode(df["embedding_text"].tolist(), show_progress_bar=True)
df["embedding_vector"] = embeddings.tolist()  # store as list for JSON export

# -----------------------------
# 5. Save embeddings to JSON
# -----------------------------
output_file = os.path.join(script_dir, "amazon_with_embeddings.json")
df.to_json(output_file, orient="records")

print(f"Done! Embeddings saved to {output_file}")
