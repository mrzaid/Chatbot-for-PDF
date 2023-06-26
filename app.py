import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.redis import Redis
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

load_dotenv()
with st.sidebar:
    st.title('🤗💬 Chat with your Data')
    st.markdown('''
                ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
                ''')

def main():
    st.header("Chat with your own PDF")
    pdf = st.file_uploader("Upload your pdf", type="pdf")
    
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        texts = []
        for page in pdf_reader.pages:
            chunks = page.extract_text()
            texts.append(chunks)
            st.write(texts)
        
        embeddings = OpenAIEmbeddings()
        VectorStore = Redis.from_texts(texts, embeddings, redis_url="redis://localhost:6379")
        query = st.text_input("Ask questions related to your PDF")

        if query:
            results = VectorStore.similarity_search(query=query, k=3)
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            response = chain.run(input_documents=results, question=query)
            st.write(response) 

if __name__ == '__main__':
    main()
