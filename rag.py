import os

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv(override=True)


# =========================
# ChromaDB
# =========================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="company_documents"
)


# =========================
# Embedding Model
# =========================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================
# Add Documents
# =========================

def add_documents(chunks, source_name):

    if not chunks:
        return 0

    texts = []
    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        texts.append(chunk["text"])

        ids.append(
            f"{source_name}_{chunk['page']}_{index}"
        )

        metadatas.append({
            "source": source_name,
            "page": chunk["page"]
        })

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(texts)


# =========================
# Search Documents
# =========================

def search_documents(question, top_k=5):

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    retrieved = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        retrieved.append({
            "text": document,
            "source": metadata.get(
                "source",
                "Unknown"
            ),
            "page": metadata.get(
                "page",
                "Unknown"
            )
        })

    return retrieved


# =========================
# Generate Answer
# =========================

def generate_answer(question, results):

    if not results:

        return (
            "Mujhe provided documents mein "
            "is question ka relevant answer nahi mila."
        )

    context_parts = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"Page: {result['page']}\n"
            f"Content:\n{result['text']}"
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    prompt = f"""
You are a company document assistant.

Answer the user's question ONLY using the provided
document context.

Do not use outside knowledge.

If the answer is not available in the provided context,
say exactly:

"Mujhe provided documents mein is question ka relevant answer nahi mila."

Always keep the answer clear and concise.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

    # Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    # Generate response
    response = model.invoke(prompt)

    content = response.content

    # Plain text response
    if isinstance(content, str):
        return content

    # List response
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                text_parts.append(item)

        return "\n".join(text_parts)

    return str(content)

# import os

# import chromadb
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
# from langchain_google_genai import ChatGoogleGenerativeAI


# # ============================================================
# # ENVIRONMENT
# # ============================================================

# load_dotenv(override=True)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError(
#         "GEMINI_API_KEY nahi mili. Apni .env file check karein."
#     )


# # ============================================================
# # CHROMADB
# # ============================================================

# chroma_client = chromadb.PersistentClient(
#     path="chroma_db"
# )

# collection = chroma_client.get_or_create_collection(
#     name="company_documents"
# )


# # ============================================================
# # EMBEDDING MODEL
# # ============================================================

# embedding_model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# # ============================================================
# # ADD DOCUMENTS
# # ============================================================

# def add_documents(chunks, source_name):
#     """
#     Document chunks ko embeddings mein convert karke
#     ChromaDB mein store karta hai.
#     """

#     if not chunks:
#         return 0

#     texts = []
#     ids = []
#     metadatas = []

#     for index, chunk in enumerate(chunks):

#         text = chunk.get("text", "").strip()

#         if not text:
#             continue

#         page = chunk.get("page", "Unknown")

#         texts.append(text)

#         ids.append(
#             f"{source_name}_{page}_{index}"
#         )

#         metadatas.append({
#             "source": source_name,
#             "page": page
#         })

#     if not texts:
#         return 0

#     # Generate embeddings
#     embeddings = embedding_model.encode(
#         texts,
#         convert_to_numpy=True
#     ).tolist()

#     # Store in ChromaDB
#     collection.upsert(
#         ids=ids,
#         documents=texts,
#         embeddings=embeddings,
#         metadatas=metadatas
#     )

#     return len(texts)


# # ============================================================
# # SEARCH DOCUMENTS
# # ============================================================

# def search_documents(question, top_k=5):
#     """
#     User question ke liye relevant document chunks
#     semantic search se retrieve karta hai.
#     """

#     question = question.strip()

#     if not question:
#         return []

#     # Question embedding
#     question_embedding = embedding_model.encode(
#         [question],
#         convert_to_numpy=True
#     ).tolist()

#     # ChromaDB search
#     results = collection.query(
#         query_embeddings=question_embedding,
#         n_results=top_k,
#         include=[
#             "documents",
#             "metadatas",
#             "distances"
#         ]
#     )

#     documents = results.get(
#         "documents",
#         [[]]
#     )[0]

#     metadatas = results.get(
#         "metadatas",
#         [[]]
#     )[0]

#     distances = results.get(
#         "distances",
#         [[]]
#     )[0]

#     retrieved = []

#     for document, metadata, distance in zip(
#         documents,
#         metadatas,
#         distances
#     ):

#         if not document:
#             continue

#         metadata = metadata or {}

#         retrieved.append({
#             "text": document,
#             "source": metadata.get(
#                 "source",
#                 "Unknown"
#             ),
#             "page": metadata.get(
#                 "page",
#                 "Unknown"
#             ),
#             "distance": distance
#         })

#     return retrieved


# # ============================================================
# # CHECK WHETHER DOCUMENT RESULTS ARE RELEVANT
# # ============================================================

# def _has_relevant_document(results):
#     """
#     Check karta hai ke retrieved PDF/document results
#     question ke liye sufficiently relevant hain ya nahi.

#     Lower Chroma distance = better similarity.
#     """

#     if not results:
#         return False

#     # Best result
#     best_distance = results[0].get(
#         "distance",
#         999
#     )

#     # Threshold
#     #
#     # all-MiniLM-L6-v2 ke liye ye practical starting
#     # threshold hai. Agar zaroorat ho to isko adjust
#     # kar sakte hain.
#     #
#     # Lower distance means stronger similarity.

#     if best_distance <= 0.90:
#         return True

#     return False


# # ============================================================
# # CONVERT GEMINI RESPONSE TO TEXT
# # ============================================================

# def _response_to_text(content):
#     """
#     Gemini response ko safely plain text mein convert karta hai.
#     """

#     if isinstance(content, str):
#         return content.strip()

#     if isinstance(content, list):

#         text_parts = []

#         for item in content:

#             if isinstance(item, dict):

#                 if item.get("type") == "text":
#                     text_parts.append(
#                         item.get("text", "")
#                     )

#                 elif "text" in item:
#                     text_parts.append(
#                         str(item.get("text", ""))
#                     )

#             elif isinstance(item, str):
#                 text_parts.append(item)

#         return "\n".join(
#             part for part in text_parts if part
#         ).strip()

#     return str(content).strip()


# # ============================================================
# # GEMINI MODEL
# # ============================================================

# def _get_model():
#     """
#     Gemini model create karta hai.
#     """

#     return ChatGoogleGenerativeAI(
#         model="gemini-3.5-flash-lite",
#         google_api_key=GEMINI_API_KEY
#     )


# # ============================================================
# # HYBRID ANSWER GENERATION
# # ============================================================

# def generate_answer(question, results):
#     """
#     HYBRID RAG:

#     1. Agar relevant document/PDF context available hai:
#        -> Answer ONLY from documents.

#     2. Agar relevant document context nahi hai:
#        -> Gemini ki general knowledge se answer.

#     Is tarah chatbot sirf PDF tak limited nahi rahega.
#     """

#     question = question.strip()

#     if not question:
#         return "Please enter a question."


#     # ========================================================
#     # CASE 1: RELEVANT DOCUMENT FOUND
#     # ========================================================

#     if _has_relevant_document(results):

#         context_parts = []

#         for result in results:

#             context_parts.append(
#                 f"Source: {result.get('source', 'Unknown')}\n"
#                 f"Page: {result.get('page', 'Unknown')}\n"
#                 f"Content:\n{result.get('text', '')}"
#             )

#         context = "\n\n---\n\n".join(
#             context_parts
#         )

#         prompt = f"""
# You are a company document assistant.

# The user asked a question about the provided company
# documents.

# Answer the user's question using ONLY the document
# context below.

# Do not add outside information.

# If the answer is not actually available in the document
# context, clearly say that the information was not found
# in the provided documents.

# Keep the answer clear, useful and concise.

# DOCUMENT CONTEXT:
# {context}

# USER QUESTION:
# {question}
# """

#         try:

#             model = _get_model()

#             response = model.invoke(prompt)

#             answer = _response_to_text(
#                 response.content
#             )

#             return answer


#         except Exception as e:

#             return (
#                 "Document answer generate karte waqt "
#                 f"error aaya: {str(e)}"
#             )


#     # ========================================================
#     # CASE 2: NO RELEVANT DOCUMENT
#     # ========================================================

#     general_prompt = f"""
# You are a helpful AI assistant.

# The user's question does not have a sufficiently relevant
# answer in the uploaded company documents.

# Therefore, answer the question using your general knowledge.

# Do NOT pretend that the answer came from the uploaded
# documents.

# Be clear, accurate and concise.

# If the question is asking about a programming concept,
# technology, general knowledge, mathematics, or another topic
# not present in the uploaded documents, answer normally.

# USER QUESTION:
# {question}
# """

#     try:

#         model = _get_model()

#         response = model.invoke(
#             general_prompt
#         )

#         answer = _response_to_text(
#             response.content
#         )

#         return answer


#     except Exception as e:

#         return (
#             "General AI answer generate karte waqt "
#             f"error aaya: {str(e)}"
#         )