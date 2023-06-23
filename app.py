import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 Chat with your Data')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model

    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Zaid Ahmed](https://mzaidahmed.netlify.app)')

load_dotenv()

def main():
    st.header("Chat with your PDF 💬")
    
    #upload a PDF File
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    #st.write(pdf)
    if pdf is not None:
        pdf_reader=PdfReader(pdf)
        # st.write(pdf_reader)        
        text=""
        for page in pdf_reader.pages:
            
            text += page.extract_text()
        
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )    
        chunks=text_splitter.split_text(text=text)
        # st.write(chunks)        

        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)

        # Accept user questions/query
        query = st.text_input("Ask questions about your PDF file:")
        st.write(query)

        if query:
            docs = VectorStore.similarity_search(query=query, k=3)
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=query)
            st.write(response)


if __name__ == '__main__':
    main() 