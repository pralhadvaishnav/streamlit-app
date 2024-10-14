import openai
import streamlit as st

# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'


# Define a function to call OpenAI API
def generate_response(prompt, history):
    """
    Generate response using OpenAI's GPT model.

    Args:
        prompt (str): The user input to pass to the model.
        history (list): A list that maintains the conversation history.

    Returns:
        str: The AI-generated response.
    """
    # Concatenate the conversation history and the new prompt
    conversation_history = "\n".join(history)
    conversation_history += f"\nUser: {prompt}\nAI:"

    try:
        # Call OpenAI API for the completion
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the latest GPT model
            prompt=conversation_history,
            max_tokens=150,  # Limit the response size
            temperature=0.9,  # Controls creativity of responses
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\nUser", "\nAI"]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


# Streamlit App
def main():
    """
    The main function that runs the Streamlit app.
    It manages the user interface and conversation logic.
    """
    st.title("Chatbot with Short-Term Memory")
    st.write("This is a simple chatbot app with short-term memory, powered by OpenAI's GPT.")

    # Initialize session state variables
    if 'history' not in st.session_state:
        st.session_state['history'] = []  # Conversation history
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ''  # User input

    # Display conversation history
    for i, line in enumerate(st.session_state['history']):
        if i % 2 == 0:  # User input
            st.write(f"User: {line}")
        else:  # AI response
            st.write(f"AI: {line}")

    # User input
    user_input = st.text_input("You: ", key="user_input")

    if user_input:
        # Update conversation history
        st.session_state['history'].append(user_input)

        # Get response from GPT model
        ai_response = generate_response(user_input, st.session_state['history'])

        # Append AI response to history
        st.session_state['history'].append(ai_response)

        # Clear the input field
        st.session_state['user_input'] = ''


if __name__ == "__main__":
    main()
