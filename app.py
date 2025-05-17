import streamlit as st
import ollama

st.set_page_config(page_title="ChatBot", page_icon="🤖", layout="centered")
st.title("🤖 AI ChatBot")

st.subheader("Hello Buddy!")
st.divider()
st.subheader("What can I assist you with today?")
st.divider()

st.info("You can switch between Light and Dark mode from Streamlit settings (⚙️ in the top-right corner).")

# Maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# Display Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

    # Show feedback options only for assistant messages
    if msg["role"] == "assistant":
        feedback_key = f"feedback_{i}"
        comment_key = f"comment_{i}"

        if feedback_key not in st.session_state.feedback:
            st.session_state.feedback[feedback_key] = {"rating": None, "comment": ""}

        # Feedback selection
        feedback = st.radio(
            "Was this response helpful?", 
            ["👍 Yes", "👎 No", "Skip"], 
            index=2 if st.session_state.feedback[feedback_key]["rating"] is None else 
                   ["👍 Yes", "👎 No", "Skip"].index(st.session_state.feedback[feedback_key]["rating"]),
            key=feedback_key
        )

        # Feedback comment
        comment = st.text_area(
            "Any suggestions?", 
            value=st.session_state.feedback[feedback_key]["comment"], 
            key=comment_key
        )

        # Store feedback in session state
        if st.button(f"Submit Feedback {i}"):
            st.session_state.feedback[feedback_key] = {"rating": feedback, "comment": comment}
            st.success("Thank you for your feedback!")

query = st.chat_input("Enter your question")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ollama.generate(model='llama3.2:1B', prompt=query)
                assistant_response = response.get('response', "I'm sorry, I couldn't process that.")
            except Exception as e:
                assistant_response = f"Error: {str(e)}"

        st.write(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.feedback = {}
    st.experimental_rerun()
