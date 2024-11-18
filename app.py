import streamlit as st
import google.generativeai as genai

genai.configure(api_key = "AIzaSyB4tK6azgrb_-VQSgsNT2BW29ABjwaxJII")

llm = genai.GenerativeModel("models/gemini-1.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []


def format_history_for_model(history):
    
    """ formatted history entries to match the model's expected structure"""
    
    formatted_history = []



    for entry in history:

        formatted_history.append({

            "role" : entry["role"],

            "parts" : [{"text" : entry["context"]}]

        })

    return formatted_history



def get_response(message):

    formatted_history = format_history_for_model(st.session_state.history)
    
    chatbot = llm.start_chat(history=formatted_history)
    
    response = chatbot.send_message(message)
    
    st.session_state.history.append({"role" : "user", "context" : message})
    
    st.session_state.history.append({"role" : "model", "context" : response.text})
    
    return response.text




st.title("Welcome to the CHATBOT 629")

st.chat_message("ai").write("Hi there, I am a helpful AI assistant. How can I help you today..?")




# print our previous chat
for entry in st.session_state.history:
    if entry["role"] == "user":
        st.chat_message("human").write(entry["content"])
    else:
        st.chat_message("ai").write(entry["content"])



human_prompt = st.chat_input("Say Something...")



if human_prompt:
    st.chat_message("human").write(human_prompt)
    response = get_response(human_prompt)
    st.chat_message("ai").write(response)