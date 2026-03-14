# Document QA System

A Document Question Answering System built with Transformers and Streamlit, allowing users to upload PDF or TXT files and ask questions about their content. The system can detect chapters and answer questions based on specific sections for more accurate results

Features

Upload PDF or TXT documents.

Automatically splits text into chapters for better QA accuracy.

Ask any question and get relevant answers using a pretrained Transformers QA model (distilbert-base-cased-distilled-squad).

Beautiful and interactive Streamlit UI with styled answers and chapter sidebar.

Works with both short and long documents.

Easy to extend with RAG/FAISS for larger datasets in the future.
