import streamlit as st 
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory

# Set Up the Google Gemini Chat Model
google_api_key = 'AIzaSyBUoUSPd2RxP27oRjfgLDMdmsX26giZXU8'
GeminiChat = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=google_api_key)

# create prompt 
initial_prompt = """
You are Q&A chatbot make conversations in different fileds.
When get question from user make your response concise and oraginzed.
If you don't know question answer say i don't know.
"""
# Streamlit UI
st.title('Conversation Q&A Chatbot')

# Button to clear all messages
if st.button('Clear Messages'):
    # Clear session state for messages and history
    st.session_state.messages = []
    # Rerun the app to refresh the state
    st.experimental_rerun()  

# Initialize session state for messages and history
if 'messages' not in st.session_state:
    st.session_state.messages = [] 


# Display previous messages from the session state
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Input from user
prompt = st.chat_input('Ask your question')

if prompt:
    # Display user message in chat message container
    with st.chat_message('user'):
        st.write(prompt)
    
    # Add user message to session history and update messages
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Generate response from model 
    response_chunks = GeminiChat.stream(
        [msg['content']  for msg in st.session_state.messages]
        )
    
    # Collect response content for appending to history
    response_content = []
    
    # Display assistant's response in real-time
    with st.chat_message('assistant'):
        for chunk in response_chunks:
            st.write(chunk.content, end='', flush=True)  
            response_content.append(chunk.content)

    # Combine all response chunks
    complete_response = ' '.join(response_content)
    #  Add assistant message to history and session state
    st.session_state.messages.append({'role': 'assistant', 'content': complete_response})

    