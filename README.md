# Medical-Chatbot-using-Gen-AI-

🟪 1. Data Ingestion
🔹 Input:
Data/Medical Book.pdf

🔹 Code:
python
Copy
Edit
loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
🔹 Outcome:
Full text extracted from PDFs

🟦 2. Text Chunking
🔹 Code:
python
Copy
Edit
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
text_chunks = text_splitter.split_documents(documents)
🔹 Outcome:
Long text is broken into overlapping, manageable pieces (for better LLM comprehension)

🟩 3. Embedding (Vectorization)
🔹 Code:
python
Copy
Edit
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
🔹 What This Does:
Converts each chunk into a high-dimensional numeric vector

These vectors capture semantic meaning (so similar chunks are close in vector space)

🟨 4. Vector Database Storage (Pinecone)
🔹 Create Pinecone Index:
python
Copy
Edit
pc.create_index(name=index_name, dimension=384, metric="cosine", ...)
🔹 Store Vectors:
python
Copy
Edit
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)
🔹 Outcome:
All chunks now live in Pinecone as vectors → ready for similarity search!

🟧 5. Retrieval (from Vector DB)
🔹 Code:
python
Copy
Edit
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
🔹 What This Does:
When a user asks a question, this fetches top-k most semantically similar chunks

🟥 6. LLM Response (Question Answering)
🔹 Setup Prompt:
python
Copy
Edit
prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
🔹 Chain the LLM:
python
Copy
Edit
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
🔹 What This Does:
Combines your prompt + retrieved context + question → sends to LLM

Returns a natural language answer

🌐 7. Flask App Integration (Frontend)
🔹 Code:
python
Copy
Edit
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    response = rag_chain.invoke({"input": msg})
    return f"Dr. Bot: {response['answer']}"
🔹 Outcome:
Chat interface in browser where users can type medical questions

Response shown via /get endpoint using chat.html

