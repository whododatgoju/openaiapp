import streamlit as st
st.image("https://emarsys.com/app/uploads/2020/03/real-ai.jpg", caption="AI-Powered Streamlit App")
st.image("https://i.imgur.com/bQtWJUI.jpg", caption="AI-Powered Streamlit App")
import requests
import json
import base64
from langchain_community.llms import OpenAI
from openai import OpenAI as OpenAIClient

# Sidebar - OpenAI API Key Input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# Dropdown Menu for Navigation
selected_tab = st.selectbox(
    "Select a Feature:",
    [
        "💬 Chat", "🖼️ Vision", "🎨 Image Generation",
        "🔊 Audio Generation", "🎙 Speech to Text",
        "🛑 Moderation", "🧠 Reasoning", "🛠 Functions"
    ]
)

if selected_tab == "💬 Chat":
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

elif selected_tab == "🖼️ Vision":
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

elif selected_tab == "🎨 Image Generation":
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

elif selected_tab == "🛠 Functions":
    st.title("🛠 AI Functions (Tool Calling)")

    st.markdown("""
    ### How Function Calling Works
    OpenAI's GPT-4o model can **call functions** to retrieve real-world data.  
    This example fetches the **temperature in both Celsius and Fahrenheit** along with a **weather description** using a weather API.
    """)

    # Function to get weather data from Open-Meteo API
    def get_weather(latitude, longitude):
        try:
            response = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode&hourly=temperature_2m"
            )
            data = response.json()
            temp_c = data['current']['temperature_2m']
            temp_f = (temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
            weather_code = data['current']['weathercode']

            # Mapping weather codes to descriptions
            weather_descriptions = {
                0: "Clear sky ☀️",
                1: "Mainly clear 🌤",
                2: "Partly cloudy ⛅",
                3: "Overcast ☁️",
                45: "Fog 🌫",
                48: "Rime fog 🌫❄",
                51: "Light drizzle 🌦",
                53: "Moderate drizzle 🌦",
                55: "Heavy drizzle 🌧",
                61: "Light rain 🌦",
                63: "Moderate rain 🌧",
                65: "Heavy rain 🌧🌧",
                71: "Light snow 🌨",
                73: "Moderate snow 🌨🌨",
                75: "Heavy snow ❄️❄️❄️",
                95: "Thunderstorms ⛈",
                96: "Thunderstorms with light hail ⛈",
                99: "Thunderstorms with heavy hail 🌩",
            }

            weather_description = weather_descriptions.get(weather_code, "Unknown weather condition 🤷")
            return temp_c, temp_f, weather_description

        except Exception as e:
            return None, None, f"Error retrieving weather data: {str(e)}"

    # Expanded list of locations including Miami
    locations = {
        "Miami, USA": (25.7617, -80.1918),
        "New York, USA": (40.7128, -74.0060),
        "Los Angeles, USA": (34.0522, -118.2437),
        "Chicago, USA": (41.8781, -87.6298),
        "Houston, USA": (29.7604, -95.3698),
        "Toronto, Canada": (43.6532, -79.3832),
        "Vancouver, Canada": (49.2827, -123.1207),
        "Buenos Aires, Argentina": (-34.6037, -58.3816),
        "São Paulo, Brazil": (-23.5505, -46.6333),
        "Mexico City, Mexico": (19.4326, -99.1332),
        "Lima, Peru": (-12.0464, -77.0428),
        "Bogotá, Colombia": (4.7110, -74.0721),
        "Santiago, Chile": (-33.4489, -70.6693)
    }

    # User selection method (dropdown or manual entry)
    input_method = st.radio("Choose input method:", ["Select a City", "Enter Latitude/Longitude"])

    if input_method == "Select a City":
        location_name = st.selectbox("Select a location:", list(locations.keys()))
        latitude, longitude = locations[location_name]
    else:
        latitude = st.number_input("Enter Latitude:")
        longitude = st.number_input("Enter Longitude:")

    if st.button("Get Weather via Function Call"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            try:
                client = OpenAIClient(api_key=openai_api_key)
                temp_c, temp_f, weather_description = get_weather(latitude, longitude)

                if temp_c is not None:
                    st.success(f"✅ Weather Retrieved for {location_name if input_method == 'Select a City' else 'your custom location'}")
                    st.write(f"🌡 **Temperature:** {temp_c:.1f}°C / {temp_f:.1f}°F")
                    st.write(f"🌦 **Conditions:** {weather_description}")
                else:
                    st.error("⚠ Failed to retrieve weather data. Please try again.")

            except Exception as e:
                st.error(f"Error: {str(e)}")



elif selected_tab == "🧠 Reasoning":
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
