# 🤖 AI Chatbot RAG

### Hybrid Retrieval-Augmented Generation Chatbot for Document-Based Question Answering

An intelligent AI chatbot that allows users to upload PDF documents and ask questions about their content. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate clear answers using Google Gemini.

---

## 📌 Project Overview

**AI Chatbot RAG** is a document-based question-answering system designed to make information retrieval from company documents faster and easier.

Instead of manually searching through lengthy documents, users can upload a PDF and ask questions in natural language. The system processes the document, converts its content into embeddings, stores those embeddings in a vector database, and retrieves the most relevant information when a question is asked.

The retrieved information is then provided to Google Gemini to generate the final answer.

---

## ✨ Key Features

- 📄 PDF document upload
- 🔍 Semantic document search
- 🧠 Retrieval-Augmented Generation (RAG)
- 🤖 Google Gemini AI integration
- 🗃️ ChromaDB vector database
- 🔤 Sentence Transformers embeddings
- 📚 Document source and page references
- 💬 Natural-language question answering
- 🌐 Interactive Streamlit web interface
- 🔐 Environment-based API key configuration
- ⚡ Fast retrieval from processed documents

---

## 🏗️ System Architecture

```text
                  ┌─────────────────────┐
                  │    User Uploads     │
                  │    PDF Document     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Document Processor  │
                  │ Text Extraction &   │
                  │ Chunking             │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Sentence            │
                  │ Transformers        │
                  │ Embedding Model     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      ChromaDB       │
                  │   Vector Database   │
                  └──────────┬──────────┘
                             │
                             │ Semantic Search
                             ▼
                  ┌─────────────────────┐
                  │ Relevant Document   │
                  │ Chunks Retrieved    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Google Gemini    │
                  │   Answer Generator  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Final Answer     │
                  │   Shown to User     │
                  └─────────────────────┘
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Streamlit** | Web application interface |
| **ChromaDB** | Local vector database |
| **Sentence Transformers** | Text embeddings |
| **Google Gemini** | AI answer generation |
| **LangChain Google GenAI** | Gemini integration |
| **PyMuPDF** | PDF text extraction |
| **python-dotenv** | Environment variable management |

---

## 📂 Project Structure

```text
AI-Chatbot-RAG/
│
├── app.py
├── rag.py
├── document_processor.py
├── requirements.txt
├── .gitignore
├── documents/
└── README.md
```

---

## 📄 File Description

### `app.py`

Contains the Streamlit web application and user interface.

### `rag.py`

Contains the RAG pipeline including:

- Document embeddings
- ChromaDB storage
- Semantic search
- Relevant document retrieval
- Gemini answer generation

### `document_processor.py`

Handles PDF document processing, text extraction, and document preparation.

### `requirements.txt`

Contains the Python dependencies required to run the project.

### `documents/`

Directory used for project documents.

### `.gitignore`

Prevents sensitive files and local generated files from being uploaded to GitHub.

---

## 🔄 How the RAG Pipeline Works

### 1. Upload Document

The user uploads a PDF document through the Streamlit interface.

### 2. Process Document

The system extracts text from the uploaded PDF and divides it into manageable chunks.

### 3. Generate Embeddings

Each document chunk is converted into a numerical vector using the Sentence Transformers embedding model.

### 4. Store in ChromaDB

The generated embeddings and document information are stored in ChromaDB.

### 5. Ask a Question

The user enters a question about the uploaded document.

### 6. Semantic Search

The question is converted into an embedding and compared with stored document embeddings.

### 7. Retrieve Relevant Information

The most relevant document chunks are retrieved from ChromaDB.

### 8. Generate Answer

The retrieved context is provided to Google Gemini, which generates the final answer.

### 9. Display Result

The answer is displayed in the Streamlit chatbot interface along with document source information.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/almeerahmed610/AI-Chatbot-RAG.git
```

Move into the project directory:

```bash
cd AI-Chatbot-RAG
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

Create a `.env` file in the project root directory.

Add your Google Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### ⚠️ Security Warning

Never upload your real API key to GitHub.

The `.gitignore` file should prevent the `.env` file from being uploaded.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

After starting the application, open:

```text
http://localhost:8501
```

---

## 💬 Example Usage

### Step 1

Upload a PDF document.

### Step 2

Click **Process Document**.

### Step 3

Ask a question about the uploaded document.

Example:

```text
What problems are mentioned in traditional hospital management?
```

### Step 4

The chatbot retrieves relevant information and generates an answer.

---

## 📚 Example Use Cases

This system can be used for:

- 🏥 Hospital documentation
- 🏢 Company policies
- 📑 Business reports
- 🎓 Academic documents
- 📖 Research papers
- 📋 Project documentation
- 👨‍💼 HR documents
- 📊 Company reports
- 📄 Technical documentation

---

## 🔐 Security

Sensitive credentials are stored using environment variables.

The following files and directories should not be committed to GitHub:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
chroma_db/
```

---

## ⚠️ Limitations

- Answer quality depends on the uploaded document.
- Very large documents may require additional processing time.
- AI-generated answers require a valid Gemini API key.
- ChromaDB is configured as a local vector database.
- The application is primarily designed for document-based question answering.

---

## 🔮 Future Improvements

Possible future improvements include:

- 🌐 Cloud deployment
- 🗄️ Cloud-based vector database
- 👥 User authentication
- 📚 Multiple document collections
- 🧾 Support for additional document formats
- 💾 Chat history
- 🎤 Voice-based questions
- 🌍 Multilingual support
- 📊 Document analytics
- 🔎 Advanced hybrid retrieval
- ⚡ Improved response performance

---

## 👨‍💻 Project Information

| Property | Details |
|---|---|
| **Project Name** | AI Chatbot RAG |
| **Project Type** | Retrieval-Augmented Generation Application |
| **Interface** | Streamlit |
| **Vector Database** | ChromaDB |
| **Embedding Model** | Sentence Transformers |
| **Generative AI** | Google Gemini |
| **Programming Language** | Python |

---

## 📜 License

This project is created for educational and academic purposes.

---

## ⭐ Acknowledgement

This project demonstrates the practical implementation of:

- Retrieval-Augmented Generation
- Vector databases
- Semantic search
- Text embeddings
- Generative AI
- Document processing
- AI-powered question answering

---

## 🚀 Conclusion

**AI Chatbot RAG** provides an intelligent way to interact with documents using modern Artificial Intelligence and Retrieval-Augmented Generation technologies.

Instead of manually searching through documents, users can simply ask questions and receive relevant answers through an easy-to-use chatbot interface.

---

### 🤖 AI Chatbot RAG

**Turning Documents into Intelligent Conversations.**
