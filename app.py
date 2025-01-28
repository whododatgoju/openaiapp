import streamlit as st
from langchain_community.llms import OpenAI
from openai import OpenAI as OpenAIClient

# Set up tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🖼️ Vision", "🎨 Image Generation"])

# Sidebar - OpenAI API Key Input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

with tab1:
    st.title('🦜🔗 Quickstart App')

    def generate_response(input_text):
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
        st.info(llm(input_text))

    with st.form('my_form'):
        text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
        submitted = st.form_submit_button('Submit')

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            generate_response(text)

with tab2:
    st.title("🖼️ Vision AI")

    image_url = st.text_input("Enter an Image URL:", 
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg")

    if st.button("Analyze Image"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            try:
                client = OpenAIClient(api_key=openai_api_key)
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

            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab3:
    st.title("🎨 AI Image Generation")

    prompt = st.text_area("Enter a prompt for the image:", "a white siamese cat")
    size = st.selectbox("Select Image Size:", ["1024x1024", "512x512", "256x256"])
    
    if st.button("Generate Image"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            try:
                client = OpenAIClient(api_key=openai_api_key)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality="standard",
                    n=1,
                )

                if response and hasattr(response, "data"):
                    image_url = response.data[0].url
                    st.image(image_url, caption="Generated Image", use_column_width=True)
                    st.success("✅ Image generated successfully!")
                else:
                    st.error("⚠ Failed to generate image. Please try again.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
