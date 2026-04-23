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
        if senha == "freitas123":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# CONEXÃO COM A IA (SISTEMA DE TENTATIVAS)
try:
    API_KEY = st.secrets["CHAVE_NOVA"]
    genai.configure(api_key=API_KEY)
    
    # Lista de nomes possíveis para o modelo (o código tentará um por um)
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    model = None
    
    for name in model_names:
        try:
            temp_model = genai.GenerativeModel(name)
            # Testa se o modelo responde
            temp_model.generate_content("test", generation_config={"max_output_tokens": 1})
            model = temp_model
            break # Se funcionou, para de procurar
        except:
            continue
            
    if model is None:
        st.error("Não foi possível conectar aos modelos do Google. Verifique sua API Key.")
        st.stop()
        
except Exception as e:
    st.error(f"Erro Crítico de Conexão: {e}")
    st.stop()

# INTERFACE
st.sidebar.title("MENU LOGÍSTICO")
opcao = st.sidebar.radio("Ir para:", ["Análise de Custos", "Copiloto IA"])

if opcao == "Análise de Custos":
    st.title("📊 Análise Operacional")
    relato = st.text_area("Descreva os custos ou problemas detectados:")
    if st.button("Analisar"):
        if relato:
            with st.spinner('Analisando estrategicamente...'):
                response = model.generate_content(f"Como estrategista logístico, analise: {relato}")
                st.info(response.text)
        else:
            st.warning("Descreva algo para analisar.")

elif opcao == "Copiloto IA":
    st.title("🤖 Chat Estratégico")
    pergunta = st.chat_input("Pergunte algo...")
    if pergunta:
        st.write(f"**Sua Pergunta:** {pergunta}")
        with st.spinner('Pensando...'):
            try:
                response = model.generate_content(pergunta)
                st.write(f"**IA:** {response.text}")
            except Exception as e:
                st.error(f"Erro ao responder: {e}")
