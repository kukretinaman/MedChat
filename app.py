from flask import Flask, render_template, jsonify, request
from src.helper import get_embedding_model
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

embeddings = get_embedding_model()

#initialize pinecone
pc = Pinecone(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
index_name = "medchat"

#loading existing index
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings)

#prompt creation
PROMPT=PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}

#llm and chain setup
llm=CTransformers(
    model="model/llama-2-7b-chat.ggmlv3.q4_0.bin", 
    model_type="llama", 
    config={
        "temperature": 0.8,
        "max_new_tokens": 512,
    }
)

#create retrieval qa chain
qa=RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k":2}),
    chain_type_kwargs=chain_type_kwargs
)


@app.route("/")
def index():
    return render_template("chat.html")

@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json() or {}
    user_msg = payload.get('message', '')
    # Replace this with your real assistant call / logic:
    result=qa({"query": user_msg})
    # print("\nHelpful Answer:\n", result['result'], "\n")
    reply = f"I heard: {result['result']}" if user_msg else "Say something!"
    return jsonify({'reply': reply})

if __name__ == "__main__":
    app.run(debug=True)