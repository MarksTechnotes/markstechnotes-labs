# Vector Search Demo

This demo shows how to:

- Encode text into vectors using Hugging Face `SentenceTransformer`
- Store and query vectors in Oracle Autonomous Database (26ai)
- Perform hybrid vector + relational search

## Setup

1. Fill in your credentials in  `.env` 
2. Install dependencies:

```bash
pip install oracledb sentence-transformers python-dotenv
