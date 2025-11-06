from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

#Extract the data
def load_data(file_path):
    loader = DirectoryLoader(file_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


#create text chunks
def create_text_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    texts = text_splitter.split_documents(documents)
    return texts


#dowload embedding model
def get_embedding_model():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")
    return embeddings


