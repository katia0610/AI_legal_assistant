import streamlit as st
import re
from langchain_groq import ChatGroq
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from prompts import prompt
from constants import *

# 🎯 Function to detect Arabic
def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

# ⚡️ Cache embeddings
@st.cache_resource(show_spinner=False)
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=MODEL_EMBEDDING)

# ⚡️ Cache Qdrant client + vectorstore
@st.cache_resource(show_spinner=False)
def load_vectorstore(_embeddings):
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API)
    vectorstore = Qdrant(client=client, collection_name=QDRANT_COLLECTION, embeddings=_embeddings)
    return vectorstore

# ⚡️ Cache LLM
@st.cache_resource(show_spinner=False)
def load_llm():
    return ChatGroq(temperature=0, model_name=LLM_NAME, streaming=True)

# 🔧 Load resources
embeddings = load_embeddings()
vectorstore = load_vectorstore(embeddings)
llm = load_llm()

# 🔗 Setup memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🚀 Streamlit interface
st.title("🧠 AI Legal Assistant")

# 🔗 Session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📝 Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        direction = "rtl" if is_arabic(message["content"]) else "ltr"
        
        # Appliquer style spécifique pour user
        if message["role"] == "user":
            st.markdown(
                f"""
                <div dir='{direction}' style='
                    text-align: justify;
                    padding-bottom: 14px;
                    line-height: 1.6;
                    display: flex;
                    align-items: center;
                '>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Style assistant
            st.markdown(
                f"""
                <div dir='{direction}' style='
                    text-align: justify;
                    line-height: 1.6;
                '>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )


# 📝 Input
user_question = st.chat_input("Posez votre question juridique ici :")

if user_question:
    # 🔗 Append user message to session state and display
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        direction = "rtl" if is_arabic(user_question) else "ltr"
        st.markdown(
            f"""
            <div dir='{direction}' style='
                text-align: justify;
                padding-bottom: 14px;
                line-height: 1.6;
                display: flex;
                align-items: center;
            '>
                {user_question}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 🔗 Retrieve context from vectorstore
    retriever = vectorstore.as_retriever()
    docs = retriever.get_relevant_documents(user_question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 🔗 Build the final prompt using your template
    final_prompt = prompt.format(question=user_question, context=context)

    # 🔗 Streaming response
    with st.chat_message("assistant"):
        response_container = st.empty()
        response_text = ""

        for chunk in llm.stream(final_prompt):
            content = chunk.content or ""
            response_text += content
            direction = "rtl" if is_arabic(response_text) else "ltr"
            response_container.markdown(
                f"<div dir='{direction}' style='text-align: justify;'>{response_text}</div>",
                unsafe_allow_html=True
            )

        # 🔗 Save assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response_text})
