import os
import oracledb
import json
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

username = os.getenv("ADB_USERNAME")
password = os.getenv("ADB_PASSWORD")
dsn = os.getenv("ADB_DSN")

# Load embedding model and encode the query text into a 768-dimensional vector
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
query_text = "wireless headphones with noise cancellation"
query_embedding = model.encode(query_text).tolist()


print("oracledb loaded successfully!")
print("Running in thick mode?" , oracledb.is_thin_mode == False)


# Connection details for Oracle Autonomous Database (26ai)
username = "ADMIN"
password = "WelCome123##"

dsn = """(description=
             (retry_count=20)
             (retry_delay=3)
             (address=(protocol=tcps)(port=1521)(host=adb.us-phoenix-1.oraclecloud.com))
             (connect_data=(service_name=g4fd273ce522b7b_reviews26ai_tp.adb.oraclecloud.com))
             (security=(ssl_server_dn_match=yes))
          )"""

# Connect to the database
conn = oracledb.connect(
    user=username,
    password=password,
    dsn=dsn
)
print("Connected!")

# Validate embedding dimension (must match column definition)
if len(query_embedding) != 768:
    raise ValueError(f"Query vector has {len(query_embedding)} elements, must be 768.")
print(len(query_embedding))
cursor = conn.cursor()

# Convert Python list → JSON-like string [0.1, 0.2, ...] required by TO_VECTOR()
vector_str = json.dumps(query_embedding)  # produces [0.01,0.2,...]'
print(vector_str)

# Minimal SQL to test TO_VECTOR()
# sql = f"SELECT TO_VECTOR('{vector_str}') AS q FROM dual"
# print("Yes!")

# Build SQL query:
#  - Convert the embedding to an Oracle VECTOR using TO_VECTOR()
#  - Compute similarity using VECTOR_DISTANCE()
#  - Join PRODUCT_VECTORS with product metadata (materialized view)
sql = f"""
WITH query AS (
  SELECT TO_VECTOR('{vector_str}') AS q FROM dual
)
SELECT v.PRODUCT_ID,
       m.PRODUCT_NAME,
       v.REVIEW_ID,
       VECTOR_DISTANCE(v.EMBEDDING_VECTOR, q, COSINE) AS similarity
FROM PRODUCT_VECTORS v
JOIN PRODUCT_METADATA_MV m
  ON v.PRODUCT_ID = m.PRODUCT_ID, query
ORDER BY similarity ASC
FETCH FIRST 10 ROWS ONLY
"""

cursor.execute(sql)
results = cursor.fetchall()

# Display top results
for row in results:
    print(row)




