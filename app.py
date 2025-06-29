import streamlit as st
import re
from langchain_groq import ChatGroq
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
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

# 🔗 Setup memory in session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="input",
        output_key="output",
        return_messages=True
    )

memory = st.session_state.memory

# 🚀 Streamlit interface
st.title("🧠 AI Legal Assistant")

# 🔗 Session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📝 Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        direction = "rtl" if is_arabic(message["content"]) else "ltr"
        
        # Style for user vs assistant
        style = (
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
            """ if message["role"] == "user" else
            f"""
            <div dir='{direction}' style='
                text-align: justify;
                line-height: 1.6;
            '>
                {message["content"]}
            </div>
            """
        )
        st.markdown(style, unsafe_allow_html=True)

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


    # 🔗 Format conversation history for the prompt
    history = memory.load_memory_variables({}).get("chat_history", [])
    conversation_history = ""

    # Format if history is a list of messages
    if isinstance(history, list):
        for msg in history:
            role = "User" if msg.type == "human" else "Assistant"
            conversation_history += f"{role}: {msg.content}\n"
    else:
        conversation_history = history

    # 🔗 Retrieve context from vectorstore
    retriever = vectorstore.as_retriever()
    docs = retriever.get_relevant_documents(user_question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 📝 Before building final_prompt, print memory
    print("==== MEMORY VARIABLES ====")
    print(memory.load_memory_variables({}))

   
    # 🔗 Build the final prompt with conversation history
    final_prompt = f"""
    Tu es un expert juridique qui répond de manière claire, structurée et complète.

    Le contexte fourni ci-dessous est toujours en français. La question de l'utilisateur peut être en arabe ou en français.

    Voici tes instructions :

    - Lis la question et détecte automatiquement sa langue.
    - Si la question est en arabe, réponds en arabe.
    - Si la question est en français, réponds en français.
    - Ne traduis pas le contexte, utilise-le tel quel pour construire la réponse, mais écris la réponse finale uniquement dans la langue de la question.
    - Si la réponse n’est pas explicitement dans le contexte, dis : "Désolé, je n'ai pas trouvé cette information dans le contexte fourni."
    - Si la question de l'utilisateur fait référence à une réponse ou un sujet déjà évoqué précédemment, utilise l'historique de la conversation pour comprendre et répondre correctement.
    - Avant de répondre, vérifie toujours l'historique de la conversation pour voir si une question similaire a déjà été posée et, si c'est le cas, utilise la même réponse ou adapte-la si nécessaire.
    - Si une information utile a déjà été mentionnée dans la conversation, utilise-la pour enrichir ta réponse actuelle même si elle n'est pas présente dans le contexte fourni.

    Historique de la conversation :
    {conversation_history}

    Voici la question : {user_question}

    Voici le contexte extrait de la base de données :
    {context}

    Réponds maintenant selon ces instructions.
    """



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

        # 🔗 Update memory with this turn
        memory.save_context({"input": user_question}, {"output": response_text})
