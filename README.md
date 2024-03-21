 **# COMS-579-S24-PROJECT**

This repository contains Python code for indexing PDF documents using Pinecone, enabling efficient text retrieval.

## Overview

This tool employs Pinecone, a vector database, for seamless text retrieval from PDFs. It leverages Language Chain for language modeling capabilities and integrates with Pinecone for indexing and searching.

**Key Features:**

- Indexes PDF content for efficient text retrieval
- Employs language models for text representation
- Utilizes Pinecone for vector database operations
- Provides a user-friendly command-line interface

## Installation

1. Install required libraries:

  ```bash
  pip install langchain_community langchain pypdf sentence-transformers pinecone-client
  ```

2. Obtain a Pinecone API key from Pinecone: [https://www.pinecone.io/](https://www.pinecone.io/) and replace the placeholder in the code with your actual key.

## Usage

1. Run the code:

  ```bash
  python practice.py --PDF_FILE=<path_to_your_pdf>
  ```

2. Replace example.py with the python file name and replace <path_to_your_pdf>
with the actual path to the PDF you want to index.

## Code Structure

**Key Functions:**

- `process_pdf(file)`: Loads a PDF using PyPDFLoader.
- `split_docs(documents, chunk_size, chunk_overlap)`: Splits text into chunks for embedding generation.
- `generate_embeddings(text_chunks, model_name)`: Produces text embeddings using HuggingFaceEmbeddings.
- `generate_id(text)`: Generates unique IDs for text chunks via a hash function.
- `text_preprocessing(texts)`: Preprocesses text (lowercasing, removing "@" mentions, etc.).
- `create_index()`: Creates a Pinecone index if it doesn't exist.
- `process_and_index_pdf(pdf_file)`: Orchestrates PDF processing, embedding generation, and Pinecone uploads.

## Steps Involved:

1. Parsing command-line arguments for the PDF file path.
2. Establishing a connection with a Pinecone index, creating it if necessary.
3. Processing the PDF:
   - Loading text using PyPDFLoader.
   - Splitting text into chunks.
   - Preprocessing text.
   - Generating embeddings.
   - Creating unique IDs for chunks.
4. Uploading data to the Pinecone index.
5. Displaying a success message.
