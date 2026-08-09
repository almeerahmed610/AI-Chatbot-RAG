import os
import tempfile

import streamlit as st

from document_processor import extract_text_from_pdf, create_chunks
from rag import add_documents, search_documents, generate_answer


st.set_page_config(
    page_title="Company RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Company RAG Chatbot")
st.write(
    "Upload company documents and ask questions "
    "based on their content."
)


# =========================
# SIDEBAR - DOCUMENT UPLOAD
# =========================

st.sidebar.header("📄 Document Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.sidebar.button("Process Document"):

        with st.spinner("Processing document..."):

            # Temporary PDF file
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            try:
                # 1. Extract text
                pages = extract_text_from_pdf(temp_path)

                if not pages:
                    st.sidebar.error(
                        "PDF mein readable text nahi mila."
                    )

                else:
                    # 2. Create chunks
                    chunks = create_chunks(pages)

                    # 3. Store embeddings + metadata
                    count = add_documents(
                        chunks,
                        uploaded_file.name
                    )

                    st.sidebar.success(
                        f"Document processed successfully! "
                        f"{count} chunks added."
                    )

            finally:
                # Temporary file delete
                if os.path.exists(temp_path):
                    os.remove(temp_path)


# =========================
# CHAT
# =========================

st.header("💬 Ask a Question")

question = st.chat_input(
    "Ask something about the uploaded documents..."
)


if question:

    st.chat_message("user").write(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching documents..."):

            results = search_documents(
                question,
                top_k=5
            )

        if not results:

            st.warning(
                "Mujhe provided documents mein "
                "is question ka relevant answer nahi mila."
            )

        else:

            with st.spinner("Generating answer..."):

                answer = generate_answer(
                    question,
                    results
                )

            st.write(answer)

            st.markdown("### 📚 Sources")

            shown_sources = set()

            for result in results:

                source_key = (
                    result["source"],
                    result["page"]
                )

                if source_key not in shown_sources:

                    st.caption(
                        f"📄 {result['source']} "
                        f"| Page {result['page']}"
                    )

                    shown_sources.add(source_key)