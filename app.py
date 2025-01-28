import streamlit as st
import requests
import json
import base64
from langchain_community.llms import OpenAI
from openai import OpenAI as OpenAIClient

# Set up tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💬 Chat", "🖼️ Vision", "🎨 Image Generation",
    "🔊 Audio Generation", "🎙 Speech to Text", "🛑 Moderation", "🧠 Reasoning", "🛠 Functions"
])

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

with tab8:
    st.title("🛠 AI Functions (Tool Calling)")

    st.markdown("""
    ### How Function Calling Works
    OpenAI's GPT-4o model can **call functions** to retrieve real-world data.  
    This example fetches the **temperature in both Celsius and Fahrenheit** using a weather API.
    """)

    def get_weather(latitude, longitude):
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m")
        data = response.json()
        temp_c = data['current']['temperature_2m']
        temp_f = (temp_c * 9/5) + 32
        return temp_c, temp_f

    locations = {
        "New York, USA": (40.7128, -74.0060),
        "Los Angeles, USA": (34.0522, -118.2437),
        "Toronto, Canada": (43.6532, -79.3832),
        "Buenos Aires, Argentina": (-34.6037, -58.3816),
        "São Paulo, Brazil": (-23.5505, -46.6333),
    }

    location_name = st.selectbox("Select a location:", list(locations.keys()) + ["Manual Input"])

    if location_name == "Manual Input":
        latitude = st.number_input("Enter Latitude:", value=48.8566)
        longitude = st.number_input("Enter Longitude:", value=2.3522)
    else:
        latitude, longitude = locations[location_name]

    if st.button("Get Weather via Function Call"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            try:
                client = OpenAIClient(api_key=openai_api_key)
                temp_c, temp_f = get_weather(latitude, longitude)
                st.success(f"✅ Weather Retrieved: {temp_c}°C / {temp_f}°F")

            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab7:
    st.title("🧠 AI Reasoning")

    st.markdown("""
    ### How Reasoning Works
    The **O1 model** introduces **reasoning tokens**.  
    These tokens allow the model to **"think"** before providing a final response.
    """)

    reasoning_prompt = st.text_area("Enter a problem to solve:",
        "Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.")

    if st.button("Generate Reasoned Response"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            try:
                client = OpenAIClient(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="o1",
                    messages=[{"role": "user", "content": reasoning_prompt}]
                )

                if response and hasattr(response, "choices"):
                    st.success("✅ Reasoning Completed!")
                    st.write(response.choices[0].message.content)
                else:
                    st.error("⚠ Failed to generate reasoning response. Please try again.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
