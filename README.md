# 🧠 AI Legal Assistant

An intelligent legal assistant chatbot built to answer questions about **Algerian laws**, including the penal code and civil code.

---

## 🚀 **Features**

✅ Retrieves and analyzes legal texts to provide clear and structured answers.
✅ Uses **Hugging Face embeddings** for text vectorization and **Qdrant** as the vector store.
✅ Powered by a **Groq LLM** for fast, accurate responses.
✅ Built with **Streamlit** for an interactive and simple user interface.
✅ Maintains conversation history to support multi-turn legal queries.

---

## 💡 **Advantages**

This assistant helps **students, legal professionals, and citizens** quickly find information in the Algerian legal codes without searching manually through lengthy documents. It can be integrated into internal tools or public platforms to simplify legal research and improve access to justice-related information.

---

## ⚠️ **Current Status**

This is a **proof of concept (PoC)**.
Currently, only the penal and civil code has been integrated into the database. Adding the complete set of Algerian laws is planned for future development to make it a comprehensive legal assistant.

---

## 🛠️ **Tech Stack**

* **LangChain** for retrieval-augmented generation
* **Groq LLM** for inference
* **Hugging Face Embeddings**
* **Qdrant** as vector database
* **Streamlit** for the frontend interface

---

## ⚙️ **Installation**

```bash
git clone https://github.com/katia0610/AI_legal_assistant
cd AI_legal_assistant
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 🔑 **Configuration**

Create a `.env` file with:

```
GROQ_API_KEY=your_groq_api_key
QDRANT_API=your_qdrant_api_key
QDRANT_URL=https://your_qdrant_instance

```

---

## ▶️ **Run the application**

```bash
streamlit run app.py
```

---

## 📂 **Project structure**

```
AI_legal_assistant/
├── app.py
├── constants.py
├── prompts.py
├── clean_code_penal.py
├── extract_text.py
├── remove.py
├── store_lois.py
├── output/
│   ├── code_penal_extrait.txt
│   ├── code_penal_extrait_clean.txt
│   └── ...
└── requirements.txt
```

---

## 📝 **Author**

Katia Bair

---
