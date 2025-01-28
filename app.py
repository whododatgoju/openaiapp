import streamlit as st
from openai import OpenAI
from langchain_community.llms import OpenAI as LangOpenAI

# Initialize OpenAI client
client = OpenAI()

# Set up tabs
tab1, tab2 = st.tabs(["💬 Chat", "🖼️ Vision"])

# Sidebar - OpenAI API Key Input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

with tab1:
    st.title("💬 AI Chat")
    
    def generate_response(input_text):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
            return
        
        llm = LangOpenAI(temperature=0.7, openai_api_key=openai_api_key)
        response = llm(input_text)
        st.info(response)

    with st.form('chat_form'):
        text = st.text_area('Enter your message:', 'What are the three key pieces of advice for learning how to code?')
        submitted = st.form_submit_button('Submit')

        if submitted:
            generate_response(text)

with tab2:
    st.title("🖼️ Vision AI")

    image_url = st.text_input("Enter an Image URL:", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg")

    if st.button("Analyze Image"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]}
                ],
                max_tokens=300,
            )

            if response and hasattr(response, "choices"):
                st.image(image_url, caption="Analyzed Image", use_column_width=True)
                st.success(response.choices[0].message.content)
            else:
                st.error("Failed to generate response. Please check your API key or image URL.")
