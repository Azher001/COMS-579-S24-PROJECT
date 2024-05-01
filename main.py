import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, PodSpec
import time
import hashlib
import re
import unicodedata
import PyPDF2
index_name = 'chatbot01'
title = ''
index = None

def process_pdf(file):
    loader = PyPDFLoader(file_path=file)
    documents = loader.load()
    return documents

def preprocess_and_split(documents, chunk_size=500, chunk_overlap=125):
    text_chunks = []
    for doc in documents:
        text = "".join(doc.page_content)
        preprocessed_text = text_preprocessing(text)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " ", ""])
        chunks = text_splitter.split_text(preprocessed_text)
        text_chunks.extend(chunks)
    return text_chunks

def generate_embeddings(text_chunks, model_name="all-MiniLM-L6-v2"):
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    text_embeddings = embeddings.embed_documents(text_chunks)
    return text_embeddings

def generate_id(text):
    text_chunk = "".join(text)
    text_chunk = text_chunk.lower().strip()
    hash_object = hashlib.sha256(text_chunk.encode('utf-8'))
    hash_value = hash_object.hexdigest()
    return hash_value[:16]

def text_preprocessing(text):
    text = str(text).lower()
    text = re.sub(r'\S*@\S*\s?', ' ', text)
    text = re.sub(r'<.*?>', ' ', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def create_index():
    pc = Pinecone(
        api_key='6c0af7a7-1532-4ab0-a8f6-303333b13b23' 
    )
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric='cosine',
            spec=PodSpec(environment='gcp-starter')
        )
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    index = pc.Index(index_name)
    time.sleep(1)
    return index

def process_and_index_pdf(pdf_file):
    document = process_pdf(pdf_file)
    text_chunks = preprocess_and_split(document)
    
    texts = []
    metadatas = [] 
    for i, chunk in enumerate(text_chunks):
        record_metadatas = [{
            "text": chunk,
            "source": title
        }]
        texts.extend(chunk)
        metadatas.extend(record_metadatas) 
        ids = generate_id(texts)
        embeds = generate_embeddings(texts)
        index.upsert(vectors=zip(ids, embeds, metadatas))
        texts = []
        metadatas = []
    # Calculate and print percentage completion
        completion_percentage = ((i + 1) / len(text_chunks)) * 100
        print(f"Progress: {completion_percentage:.2f}% completed")

def get_pdf_title(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if pdf_reader.metadata.title:
                return pdf_reader.metadata.title
            else:
                print("Title not found in PDF metadata.")
                return 'None'
    except Exception as e:
        print("Error:", e)
        return 'None'

def upload_file(file_path):
    global title
    global index
    title = get_pdf_title(file_path)
    index = create_index()
    process_and_index_pdf(file_path)
    print("PDF indexing complete!")
    return "PDF indexing complete!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Indexing Tool")
    parser.add_argument("--PDF_FILE", help="Path to the PDF file")
    args = parser.parse_args()

    pdf_file = args.PDF_FILE
    upload_file(pdf_file)


#python3 practice.py --pdf_file=research_paper.pdf

#Download library
  #pip install langchain_community
  #pip install langchain --upgrade
  #pip install pypdf
  # pip install --upgrade --quiet  sentence_transformers > /dev/null
  #pip install pinecone-client

