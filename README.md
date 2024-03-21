# COMS-579-S24-PROJECT

PDF Indexing Tool
This Python code indexes PDF documents using Pinecone for efficient text retrieval.
1) Install required libraries:
Bash
pip install langchain_community langchain pypdf sentence-transformers pinecone-client

2)Obtain a Pinecone API key from https://www.pinecone.io/ and replace the placeholder in the code with your actual key.
Run the code:
Replace example.py with the python file name and replace <path_to_your_pdf>
with the actual path to the PDF you want to index.
Bash
python example.py --PDF_FILE= <path_to_your_pdf>

Code Structure
Key Functions:
process_pdf(file): Loads a PDF using PyPDFLoader.
split_docs(documents, chunk_size, chunk_overlap): Splits text into chunks for embedding.
generate_embeddings(text_chunks, model_name): Generates text embeddings with HuggingFaceEmbeddings.
generate_id(text): Creates unique IDs for text chunks using a hash function.
text_preprocessing(texts): Preprocesses text (lowercasing, removing "@" mentions, etc.).
create_index(): Creates a Pinecone index if it doesn't exist.
process_and_index_pdf(pdf_file): Processes PDF content, generates embeddings, and uploads to Pinecone.
Steps:
Parses command-line arguments for PDF file path.
Creates or connects to a Pinecone index.
Processes the PDF:
Loads text using PyPDFLoader.
Splits text into chunks.
Preprocesses text.
Generates embeddings.
Creates unique IDs for chunks.
Uploads data to the Pinecone index.
Prints a success message.

