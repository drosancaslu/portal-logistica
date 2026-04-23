import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal de Inteligência Logística", layout="wide")

# LOGIN SIMPLES
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("Acesso Restrito - Consultoria IA")
    senha = st.text_input("Introduza a Chave de Acesso:", type="password")
    if st.button("Entrar"):
        if senha == "freitas123": # Esta é a senha que você dará ao cliente
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# CONEXÃO COM A IA (Lendo dos Secrets do Streamlit)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
   model = genai.GenerativeModel('models/gemini-1.5-flash')
except:
    st.error("Erro: API Key não configurada nos Secrets do Streamlit.")
    st.stop()

# INTERFACE
st.sidebar.title("MENU LOGÍSTICO")
opcao = st.sidebar.radio("Ir para:", ["Análise de Custos", "Copiloto IA"])

if opcao == "Análise de Custos":
    st.title("📊 Análise Operacional")
    st.write("Diga à IA os gastos do mês para receber um diagnóstico.")
    relato = st.text_area("Descreva os custos ou problemas detectados:")
    if st.button("Analisar"):
        response = model.generate_content(f"Como estrategista logístico, analise: {relato}")
        st.info(response.text)

elif opcao == "Copiloto IA":
    st.title("🤖 Chat Estratégico")
    pergunta = st.chat_input("Pergunte algo...")
    if pergunta:
        st.write(f"**Pergunta:** {pergunta}")
        response = model.generate_content(pergunta)
        st.write(f"**IA:** {response.text}")
