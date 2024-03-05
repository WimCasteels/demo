import streamlit as st
from streamlit_mic_recorder import speech_to_text
from openai import OpenAI
import os
#import sounddevice as sd 
import soundfile as sf

state=st.session_state
#st.session_state.openai_client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

#systeem prompt
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = "Beantwoord de vragen alsof je zelf een IT student bent aan de AP Hogeschool in Antwerpen. Begin het gesprek met jezelf voor te stellen als student."

st.title("IT@AP Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Ik ben een IT student aan de AP Hogeschool in Antwerpen. Hoe kan ik je helpen?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hoe kan ik je helpen?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #response = st.write_stream(response_generator())
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": st.session_state.system_prompt}] +
            [{"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
        #print(stream.choices[0].message.content)
    # TTS
        # speech = client.audio.speech.create(
        #     model="tts-1",
        #     voice="nova",
        #     input=response)
        # file_path = os.getcwd() +"\\soundfile.mp3"
        # speech.stream_to_file(file_path)
        # audio_data, sample_rate = sf.read(file_path)
        # sd.play(audio_data, sample_rate)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



# if text := speech_to_text(
#     language='nl',
#     start_prompt="Opname",
#     stop_prompt="Stop opname",
#     use_container_width=False,just_once=True,key='STT'):
#     with st.chat_message("user"):
#         st.markdown(text)
#     st.session_state.messages.append({"role": "user", "content": text})
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         #response = st.write_stream(response_generator())
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[{"role": "system", "content": st.session_state.system_prompt}] +
#             [{"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#         #print(stream.choices[0].message.content)
#     # TTS
#         speech = client.audio.speech.create(
#             model="tts-1",
#             voice="nova",
#             input=response)
#         file_path = os.getcwd() +"\\soundfile.mp3"
#         speech.stream_to_file(file_path)
#         audio_data, sample_rate = sf.read(file_path)
#         sd.play(audio_data, sample_rate)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})


