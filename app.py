import validators
import streamlit as st
import logging
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader, TextLoader
from youtube_video_with_subtitle import get_transcript  # Custom function to get transcript from YouTube
import os
from youtube_video_without_subtitles import query

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Streamlit UI Config
st.set_page_config(page_title="LangChain Content Summarizer", page_icon="📝")
st.title("Universal Content Summarizer")
st.subheader('Summarize Content from a YouTube URL, Website URL, or Uploaded File')

# Sidebar for API Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key (Optional)", value="", type="password")
    if not groq_api_key:
        groq_api_key = "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"  # Replace with a secure default if needed

# Input fields
content_url = st.text_input("Enter YouTube or Website URL")
uploaded_file = st.file_uploader("Or Upload a Video/Audio File", type=["mp4", "avi", "mov", "mp3", "wav"])

# Initialize Language Model with API Key
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

# Define Prompt Template
prompt_template = """
Provide a summary of the following content in 300 words:
Instructions:
1. Include the category and purpose of the content.
2. Summarize main points and highlight key discussions.
3. Conclude with any notable actions or insights.

Content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Summarization Process
if st.button("Summarize Content"):
    if not groq_api_key or (not content_url.strip() and uploaded_file is None):
        st.error("Please provide a URL or upload a file to proceed.")
        logger.warning("Missing input data: Either API key, URL, or uploaded file not provided.")
    elif content_url and not validators.url(content_url):
        st.error("Please enter a valid URL.")
        logger.error("Invalid URL provided.")
    else:
        try:
            with st.spinner("Processing..."):
                # Handling YouTube URLs
                if content_url and ("youtube.com" in content_url or "youtu.be" in content_url):
                    transcript = get_transcript(content_url)
                    with open('transcript.txt', 'w') as f:
                        f.write(transcript)
                    loader = TextLoader('transcript.txt')
                    logger.info("Transcript extracted for YouTube URL.")

                elif uploaded_file is not None:
                    os.makedirs("uploaded_files", exist_ok=True)
                    
                    # Remove spaces from the file name
                    sanitized_filename = uploaded_file.name.replace(" ", "_")
                    temp_file_path = os.path.join("uploaded_files", sanitized_filename)
                    
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    logger.info(f"Uploaded file saved at {temp_file_path}")
                    
                    # Perform transcription with Whisper model
                    transcription_result = query(temp_file_path)
                    
                    transcript = transcription_result.get('text', 'No transcription available')
                   
                    
                    with open('transcript.txt', 'w') as f:
                        f.write(transcript)
                    
                    loader = TextLoader('transcript.txt')
                    logger.info("Audio/Video file transcribed successfully.")
                    
                    # Delete the uploaded file after processing
                    os.remove(temp_file_path)
                    logger.info(f"Uploaded file {temp_file_path} deleted after processing.")
                    

                # Handling Other URLs
                else:
                    loader = UnstructuredURLLoader(
                    urls=[content_url],
                    ssl_verify=True,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                    logger.info("Loading content from non-YouTube URL.")

                # Load and summarize content
                docs = loader.load()
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)
                
                st.success(output_summary)
                
                st.download_button(
                            label="Download Result",
                            data=output_summary,  
                            mime="text/plain"
                        )
                logger.info("Content summarized successfully.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            logger.exception("Error during content summarization.")
