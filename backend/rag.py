import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as Pine
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2

load_dotenv(override=True)
OPENAI_KEY=os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
parser = StrOutputParser()

pc=Pinecone(api_key=PINECONE_API_KEY)
index=pc.Index("tax")
embeddings = OpenAIEmbeddings( model="text-embedding-3-small", openai_api_key=OPENAI_KEY)
vectorstore=PineconeVectorStore(index, embeddings)

messages=[{
             'role': 'system',
                'content': f""""You are a tax agent and your job is to help answe the user's query based on the provided context
                """
            }]

client=OpenAI(api_key=OPENAI_KEY)

def load_data():
    """
    Loads PDF, splits into chunks, creates embeddings and uploads to Pinecone.
    
    Args:
        pdf_path: Path to PDF file
        index_name: Pinecone index name
        openai_key: OpenAI API key
    """
    # Extract text from PDF
    pdf_path = "publications/p15.pdf"
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() + '\n\n'

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.create_documents([text])

    # Create embeddings and upload to Pinecone
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_KEY
    )
    batch_size=100
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name="tax",
        embedding=embeddings
    )

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vectorstore.add_documents(batch)

    print("Data loaded successfully")
    
def get_relevant_info(query):
    context=vectorstore.similarity_search(query, k=6)
    formatted_user_query = f"""
        This is the User's Query:\n
        {query}
        This is the context retrieved:\n
        {context}
    
    """
    messages.append(
            {
                'role': 'user',
                'content': formatted_user_query
            })
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    out = response.choices[0].message.content
    print(out)
    return out



if __name__=="__main__":
    query="What are exemptions?"
    output=get_relevant_info(query)
    print(output)
    # load_data()