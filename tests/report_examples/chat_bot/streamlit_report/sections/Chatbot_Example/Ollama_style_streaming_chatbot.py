import json
import time

import requests
import streamlit as st

st.markdown(
    (
        "<h3 style='text-align: center; "
        "color: #023558;'>Ollama-style streaming chatbot</h3>"
    ),
    unsafe_allow_html=True,
)


st.markdown(
    ("<h4 style='text-align: center; " "color: #2b8cbe;'>ChatBot Component</h4>"),
    unsafe_allow_html=True,
)


# Init session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Function to send prompt to Ollama API
def generate_query(messages):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": "llama3.2", "messages": messages, "stream": True},
    )
    response.raise_for_status()
    return response


# Parse streaming response from Ollama
def parse_api_response(response):
    try:
        output = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(f"API error: {body['error']}")
            if body.get("done", False):
                return {"role": "assistant", "content": output}
            output += body.get("message", {}).get("content", "")
    except Exception as e:
        return {
            "role": "assistant",
            "content": f"Error while processing API response: {str(e)}",
        }


# Simulated typing effect for responses
def response_generator(msg_content):
    for word in msg_content.split():
        yield word + " "
        time.sleep(0.1)
    yield "\n"


# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, dict):
            st.markdown(content.get("text", ""), unsafe_allow_html=True)
            if "links" in content:
                st.markdown("**Sources:**")
                for link in content["links"]:
                    st.markdown(f"- [{link}]({link})")
            if "subgraph_pyvis" in content:
                st.components.v1.html(content["subgraph_pyvis"], height=600)
        else:
            st.write(content)


# Capture and append new user prompt
if prompt := st.chat_input("Enter your prompt here:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Retrieve question and generate answer
    combined = "\n".join(
        msg["content"] for msg in st.session_state.messages if msg["role"] == "user"
    )
    messages = [{"role": "user", "content": combined}]
    with st.spinner("Generating answer..."):
        response = generate_query(messages)
        parsed_response = parse_api_response(response)

    # Add the assistant's response to the session state and display it
    st.session_state.messages.append(parsed_response)
    with st.chat_message("assistant"):
        st.write_stream(response_generator(parsed_response["content"]))
