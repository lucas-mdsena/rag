import streamlit as st

from src import RAGManager



rag_manager = RAGManager()

st.title("Assistente de IA Jurídico")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
with st.chat_message("assistant"):
    st.markdown(f"Olá! Como posso ajudar?")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Insira sua pergunta aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = rag_manager.retrieve_and_generate(prompt)

    # AI response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
