import streamlit as st
import requests
import json
from langchain_community.llms import OpenAI
from openai import OpenAI as OpenAIClient

# Set up tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💬 Chat", "🖼️ Vision", "🎨 Image Generation", 
    "🔊 Audio Generation", "🎙 Speech to Text", "🛑 Moderation", "🧠 Reasoning", "🛠 Functions"
])

# Sidebar - OpenAI API Key Input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

with tab8:
    st.title("🛠 AI Functions (Tool Calling)")

    st.markdown("""
    ### How Function Calling Works
    OpenAI's GPT-4o model can **call functions** to retrieve real-world data.  
    In this example, the model uses the **get_weather** function to fetch the temperature of a location.
    """)

    # Function to get weather data from an external API
    def get_weather(latitude, longitude):
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        data = response.json()
        return data['current']['temperature_2m']

    # User input for location
    latitude = st.number_input("Enter Latitude:", value=48.8566)  # Default: Paris
    longitude = st.number_input("Enter Longitude:", value=2.3522)  # Default: Paris

    if st.button("Get Weather via Function Call"):
        if not openai_api_key.startswith('sk-'):
            st.warning("⚠ Please enter a valid OpenAI API key!", icon="⚠")
        else:
            try:
                client = OpenAIClient(api_key=openai_api_key)

                # Define the function for GPT-4o
                tools = [{
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get current temperature for provided coordinates in Celsius.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "latitude": {"type": "number"},
                                "longitude": {"type": "number"}
                            },
                            "required": ["latitude", "longitude"],
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }]

                # User query
                messages = [{"role": "user", "content": f"What's the weather like at {latitude}, {longitude} today?"}]

                # Call GPT-4o with function calling
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    tools=tools,
                )

                # Get and display the response
                temperature = get_weather(latitude, longitude)
                st.success(f"✅ Weather Retrieved: {temperature}°C")

            except Exception as e:
                st.error(f"Error: {str(e)}")
