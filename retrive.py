 
import argparse
from pinecone import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore  

from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
  
parser = argparse.ArgumentParser(description="Retriving tool")
parser.add_argument("--Query", help="Search Query")
parser.add_argument("--Open_AI_Key", help="Open AI API Key")
args = parser.parse_args()

query = args.Query
openai_api_key=args.Open_AI_Key


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")



pc = Pinecone(
        api_key='6c0af7a7-1532-4ab0-a8f6-303333b13b23' 
    )
index = pc.Index('chatbot01')

text_field = "text"  
vectorstore = PineconeVectorStore(  
    index, embeddings, text_field  
)  

out = vectorstore.similarity_search(  
    query,  # our search query  
    k=3  # return 3 most relevant docs  
)  

source = "\n".join([x.page_content for x in out])

augmented_prompt=f"""Using the context below, answer the query.

Contexts:
{source}

Query:{query}
"""



llm = ChatOpenAI( model='gpt-3.5-turbo-0613',temperature=0, openai_api_key=openai_api_key)
chain = load_qa_chain(llm, chain_type="stuff")
output = chain.run(input_documents=out, question=query)
print(output)
