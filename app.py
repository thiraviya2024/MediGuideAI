import streamlit as st
from datetime import datetime

from utils.pdf_reader import read_pdf
from utils.rag import create_vectorstore
from utils.ai_helper import ask_ai


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🏥",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color:#f4f7fc;
}

h1,h2,h3 {
    color:#2563eb;
}

.stButton>button {

    width:100%;
    background:#2563eb;
    color:white;
    border-radius:12px;
    height:45px;
    font-size:16px;

}

.stButton>button:hover {

    background:#1d4ed8;

}


.chat-box {

    padding:15px;
    border-radius:10px;
    background:white;
    margin-bottom:10px;

}

</style>
""", unsafe_allow_html=True)



# ---------------- SESSION STORAGE ----------------


if "text" not in st.session_state:
    st.session_state.text = ""


if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



# ---------------- HEADER ----------------


st.markdown("# 🏥 MediGuide AI")

st.caption(
    "🤖 Agentic Hospital Document Assistant"
)


st.divider()



# ---------------- DASHBOARD ----------------


st.markdown("## 📊 Dashboard")


col1,col2,col3 = st.columns(3)


with col1:

    st.metric(
        "📄 Documents",
        "1" if st.session_state.text else "0"
    )


with col2:

    st.metric(
        "🤖 AI Status",
        "Online"
    )


with col3:

    st.metric(
        "💬 Questions",
        len(st.session_state.chat_history)
    )



st.divider()



# ---------------- UPLOAD ----------------


st.markdown("## 📄 Upload Medical PDF")


uploaded_file = st.file_uploader(
    "Upload patient report / medical document",
    type=["pdf"]
)



if uploaded_file:


    with st.spinner("📖 Processing medical document..."):


        text = read_pdf(uploaded_file)

        st.session_state.text = text

        st.session_state.vectorstore = create_vectorstore(text)



    st.success(
        "✅ Medical document processed successfully"
    )


    with st.expander("📃 Extracted Text"):

        st.text_area(
            "Content",
            text,
            height=300
        )



# ---------------- CHAT ----------------


if st.session_state.vectorstore:


    st.divider()


    st.markdown(
        "## 🤖 MediGuide AI Assistant"
    )


    question = st.chat_input(
        "Ask anything about this medical document..."
    )


    if question:


        with st.spinner("🧠 Analysing..."):


            answer = ask_ai(
                st.session_state.vectorstore,
                question
            )


        st.session_state.chat_history.append(
            {
                "question":question,
                "answer":answer
            }
        )



    # Display Chat

    for chat in st.session_state.chat_history:


        with st.chat_message("user"):

            st.write(
                chat["question"]
            )


        with st.chat_message("assistant"):

            st.write(
                chat["answer"]
            )



# ---------------- REPORT DOWNLOAD ----------------


if len(st.session_state.chat_history)>0:


    st.divider()


    st.markdown(
        "## 📋 Consultation Report"
    )


    report = f"""
MediGuide AI Consultation Report

Generated:
{datetime.now()}


--------------------------------

"""


    for i,item in enumerate(
        st.session_state.chat_history,
        start=1
    ):


        report += f"""

Question {i}:

{item['question']}


AI Response:

{item['answer']}


--------------------------------

"""



    st.download_button(

        label="📥 Download Consultation Report",

        data=report,

        file_name="MediGuide_AI_Report.txt",

        mime="text/plain"

    )



# ---------------- EMPTY STATE ----------------


if st.session_state.vectorstore is None:


    st.info(
        "👆 Upload a medical PDF to start chatting with MediGuide AI"
    )