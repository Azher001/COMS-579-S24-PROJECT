import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, PodSpec
import time
import hashlib
import re
import unicodedata

index_name = 'chatbot01'

def process_pdf(file):
    loader = PyPDFLoader(file_path=file)
    documents = loader.load()
    return documents


def split_docs(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " ", ""])
    docs = text_splitter.split_documents(documents)
    return docs


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

def text_preprocessing(texts):
    text = "".join(texts)
    text = str(text).lower()
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\n', '', text) 
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
    chunks = split_docs(document)
    texts = []
    metadatas = [] 
    for i, chunk in enumerate(chunks):
        record_texts = text_preprocessing(chunk.page_content)
        record_metadatas = [{
            "text": record_texts,
            "source": chunk.metadata.get('source')
        }]
        texts.extend(record_texts)
        metadatas.extend(record_metadatas) 
        ids = generate_id(texts)
        embeds = generate_embeddings(texts)
        index.upsert(vectors=zip(ids,embeds, metadatas))
        texts = []
        metadatas = []  


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Indexing Tool")
    parser.add_argument("--PDF_FILE", help="Path to the PDF file")
    args = parser.parse_args()

    pdf_file = args.PDF_FILE
    index = create_index()
    process_and_index_pdf(pdf_file)
    print("PDF indexing complete!")


#python3 practice.py --PDF_FILE pdf_path

#Download library
  #pip install langchain_community
  #pip install langchain --upgrade
  #pip install pypdf
  # pip install --upgrade --quiet  sentence_transformers > /dev/null
  #pip install pinecone-client
