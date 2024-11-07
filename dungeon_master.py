import os
import openai
import numpy as np
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Dungeons and Dragons Dungeon Master Chatbot", layout="wide")

# Custom CSS to center the title and the API input
st.markdown("""
    <style>
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    .centered-title {
        font-size: 3rem;
        font-weight: bold;
        color: #333;
    }
    .api-input-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Check if OpenAI API key is in session state
if 'openai_api_key' not in st.session_state:
    st.markdown('<div class="api-input-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
        
        if openai_api_key:
            # Basic check: ensure it starts with "sk-" and has a reasonable length
            if openai_api_key.startswith("sk-") and len(openai_api_key) > 20:
                st.success("API key provided!")
                st.session_state.openai_api_key = openai_api_key
                openai.api_key = openai_api_key  # Set the OpenAI API key for the library
                st.rerun()  # Rerun the app to initialize the chatbot with the new key
            else:
                st.warning("Please enter a valid OpenAI API key.")
        else:
            st.info("Please enter your OpenAI API key to proceed.")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Initialize current scenario
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = None

    def create_campaign():
        """Generate a campaign setting using the chatbot."""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Dungeon Master AI for a Dungeons & Dragons campaign. "
                        "Your role is to create a rich fantasy world, introduce unique NPCs (non-player characters), "
                        "and craft plot points and quests. Keep descriptions brief and vivid, and ensure the campaign is engaging and immersive."
                    )
                }
            ]
        )
        response_content = response['choices'][0]['message']['content']
        st.session_state.current_scenario = response_content  # Store campaign description in session state
        
        return response_content

    # Function to set the initial scenario
    def set_scenario():
        """Set the initial scenario for the campaign."""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Dungeon Master AI for a Dungeons & Dragons campaign. "
                        "Your role is to create engaging scenarios that set the stage for the adventure. "
                        "Provide a vivid description of the setting, introduce key elements, and present hooks that draw players into the story."
                    )
                }
            ]
        )
        scenario_content = response['choices'][0]['message']['content']
        st.session_state.current_scenario = scenario_content
        return scenario_content

    # Function to handle user choices
    def handle_user_choice(user_choice):
        """Process user choice and generate a response from the chatbot."""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Dungeon Master AI for a Dungeons & Dragons campaign. "
                        "Your role is to respond to player actions and maintain the flow of the game. "
                        "Provide clear options and consequences for the player's actions."
                    )
                },
                {"role": "user", "content": user_choice}
            ]
        )
        response_content = response['choices'][0]['message']['content']
        return response_content

    # Streamlit UI
    st.title("Dungeons and Dragons Dungeon Master Chatbot")

    if st.button("Create Campaign"):
        campaign = create_campaign()
        st.write("### Campaign Created:")
        st.write(campaign)
        scenario = set_scenario()
        st.write("### Initial Scenario:")
        st.write(scenario)

    if st.session_state.current_scenario:
        st.write("### Current Scenario:")
        st.write(st.session_state.current_scenario)

        user_choice = st.text_input("What do you want to do? (e.g., explore the forest, talk to the stranger)")

        if st.button("Submit Choice"):
            response = handle_user_choice(user_choice)
            st.write("### Dungeon Master Response:")
            st.write(response)