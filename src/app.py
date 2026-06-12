import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from assistente import AssistenteCopa2026, MODELO_IA

st.set_page_config(page_title="Copa 2026 AI", page_icon="⚽")

if "assistente" not in st.session_state:
    st.session_state.assistente = AssistenteCopa2026()
    st.session_state.mensagens = []

assistente = st.session_state.assistente

with st.sidebar:
    st.header("Copa 2026 AI")
    st.write("Assistente sobre a Copa do Mundo FIFA 2026.")
    if assistente.usando_ia():
        st.success(f"Modo: IA generativa ({MODELO_IA}) com busca na web")
    else:
        st.info("Modo: busca local. Configure GEMINI_API_KEY para ativar a IA generativa.")
    st.divider()
    st.caption("Exemplos de perguntas:")
    st.caption("- Qual o grupo do Brasil?")
    st.caption("- Quem sao os favoritos?")
    st.caption("- Quando e onde sera a final?")
    if st.button("Limpar conversa"):
        st.session_state.assistente = AssistenteCopa2026()
        st.session_state.mensagens = []
        st.rerun()

st.title("⚽ Copa 2026 AI")
st.caption("Pergunte sobre selecoes, grupos, jogadores, datas e favoritos da Copa 2026.")

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite sua pergunta sobre a Copa 2026...")
if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = assistente.responder(pergunta)
        st.markdown(resposta)
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
