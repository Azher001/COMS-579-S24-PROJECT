 **# COMS-579-S24-PROJECT**

This repository contains Python code for indexing PDF documents using Pinecone, enabling efficient text retrieval.
##CHECKPOINT1:
## Features

- Extracts text from PDFs using PyPDF2.
- Splits text into chunks for efficient indexing.
- Generates text embeddings using Hugging Face model `all-MiniLM-L6-v2`.
- Creates a Pinecone index for fast vector similarity search.
- Preprocesses text by removing special characters, email addresses, newlines, HTML tags, and converting to lowercase.

## Installation

1. Install required libraries:

   ```bash
   pip install langchain_community langchain pypdf sentence-transformers pinecone-client
   ```

2. Obtain a Pinecone API key from [https://www.pinecone.io/](https://www.pinecone.io/) and set it as the `PINECONE_API_KEY` environment variable.

## Usage

1. Run the script:

   ```bash
   python main.py --PDF_FILE=path/to/your/pdf.pdf
   ```

2. Replace `path/to/your/pdf.pdf` with the actual path to your PDF file.

## Index Management

- The index name is `chatbot01`.
- It uses a dimension of 384 with cosine similarity metric.
- To view and manage indexes, create an account on [https://www.pinecone.io/](https://www.pinecone.io/) and use their web interface.
