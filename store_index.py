from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extract_data = load_pdf_file(data='Data/')
text_chunks = text_split(extract_data)
embeddings = download_hugging_face_embeddings()

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name and spec
index_name = "medicalbot"

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Embed each chunk and upsert the embeddings into your Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)