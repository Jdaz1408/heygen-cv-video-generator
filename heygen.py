import streamlit as st
import requests
from openai import OpenAI
import datetime
import pdfplumber
import io
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="HeyGen Video Generator")

# Create tabs
tab1, tab2 = st.tabs(["Generate Video", "Check Status"])

with tab1:
    api_keygen = os.getenv("API_KEYGEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)

    if 'edited_script' not in st.session_state:
        st.session_state.edited_script = ""

    def extract_text_from_pdf(pdf_file):
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text() or ''
            return text
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return None

    def generate_script(cv_text, job_description, question, duration):
        prompt = f"""
You are a creative assistant. Generate a script for a video based on:

CV: {cv_text}

Job description: {job_description}

Specific question: {question if question else 'Why this person is the best for the role'}

The video should be approximately {duration} minutes long.
The script should follow a rhythmic pattern based on a sine or cosine wave, where the length of the sentences varies smoothly and naturally.
Each sentence should be separated by a line break, and the script should be clear, concise, and emotionally resonant.
Do not respond with anything other than the text, jumping between lines. Do not add image cues or anything else, only the text to be used as narration.
The total length of your response must match the specified time, with a margin of error of 10 seconds.
If the topic is in English, the script should be in English; if it is in Spanish, the script should be in Spanish.
Before providing a response, verify if what the user provides is in English, and write the script in English.
Also, keep in mind not to make it rhyme too much; it shouldnt sound like a song.
        
        """
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un asistente creativo que escribe guiones para videos."},
                    {"role": "user", "content": prompt},
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error generating script: {e}")
            return None

    def send_to_heygen(script, job_title):
        url = "https://api.heygen.com/v2/video/generate"
        headers = {
            "X-Api-Key": api_keygen,
            "Content-Type": "application/json",
        }
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "b228b0b0ea2c4e24bf441d36c1bcf13b",
                        "avatar_style": "normal",
                    },
                    "voice": {
                        "type": "text",
                        "input_text": script,
                        "voice_id": "c39e1977d89d448d98b43242e53e6e00",
                    },
                    "background": {
                        "type": "color",
                        "value": "#008000",
                    },
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720,
            },
        }
        try:
            st.write("Sending request to HeyGen...")
            
            response = requests.post(url, headers=headers, json=payload)
            st.write("Response code:", response.status_code)
            st.write("Complete response:", response.text)
            
            response.raise_for_status()
            response_data = response.json()
            
            video_id = response_data.get('data', {}).get('video_id')
            if video_id:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("video_ids.txt", "a") as f:
                    f.write(f"{timestamp} | {video_id} | {job_title}\n")
                return video_id
            else:
                st.error(f"Could not get Video ID from response. Response structure: {response_data}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"HTTP request error: {str(e)}")
            if hasattr(e.response, 'text'):
                st.error(f"Error details: {e.response.text}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None

    st.title("HeyGen Video Generator")

    # Input fields
    uploaded_file = st.file_uploader("Upload your CV (PDF)", type=['pdf'])
    job_description = st.text_area("Job Description", height=200)
    job_title = st.text_input("Job Title")  # Added job title field
    question = st.text_area("What should the video be about? ", 
                           placeholder="laeve blank for 'Why you are the best for the role'",
                           height=100)
    duration = st.number_input("Video duration (minutes):", min_value=1, max_value=10)

    if st.button("Generate Script"):
        if uploaded_file and job_description and duration:
            cv_text = extract_text_from_pdf(uploaded_file)
            if cv_text:
                script = generate_script(cv_text, job_description, question, duration)
                if script:
                    st.session_state.script = script
                    st.session_state.edited_script = script
                    st.write("Generated script:")
                    st.text_area("Edit script if needed:", value=script, key="edited_script")
        else:
            st.error("Please upload your CV and provide the job description.")

    if "script" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Regenerate Script"):
                if uploaded_file and job_description and duration:
                    cv_text = extract_text_from_pdf(uploaded_file)
                    if cv_text:
                        new_script = generate_script(cv_text, job_description, question, duration)
                        if new_script:
                            st.session_state.script = new_script
                            st.rerun()

        with col2:
            if st.button("Send to HeyGen"):
                if job_title:  # Verify job title is provided
                    script_final = st.session_state.edited_script
                    video_id = send_to_heygen(script_final, job_title)
                    if video_id:
                        st.success("Video sent successfully")
                        st.code(video_id, language="text")
                else:
                    st.error("Please provide a job title before sending to HeyGen")

with tab2:
    st.title("Check Video Status")
    
    video_id_check = st.text_input("Enter video ID to check:")
    if st.button("Check Status"):
        if video_id_check:
            url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id_check}"
            headers = {"X-Api-Key": api_keygen}
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                
                if response_data.get('code') == 100:  # Verificar si la respuesta es exitosa
                    data = response_data.get('data', {})
                    status = data.get('status')
                    video_url = data.get('video_url')
                    duration = data.get('duration')
                    gif_url = data.get('gif_url')
                    
                    # Mostrar información del video
                    st.write("---")
                    st.write(f"📊 Estado: **{status}**")
                    if duration:
                        st.write(f"⏱️ Duración: **{duration:.2f} segundos**")
                    
                    # Si el video está completado, mostrar opciones de visualización
                    if status == "completed":
                        st.success("¡Video completado!")
                        
                        # Mostrar el video
                        if video_url:
                            st.write("🎥 Video:")
                            st.video(video_url)
                            st.download_button(
                                "⬇️ Descargar video",
                                video_url,
                                file_name=f"video_{video_id_check}.mp4",
                                mime="video/mp4"
                            )
                        
                        # Mostrar el GIF preview
                        if gif_url:
                            st.write("🎞️ Preview GIF:")
                            st.image(gif_url)
                    elif status == "processing":
                        st.info("El video está siendo procesado...")
                    elif status == "failed":
                        st.error(f"Error en el procesamiento del video: {data.get('error')}")
                else:
                    st.error(f"Error en la respuesta: {response_data.get('message', 'Error desconocido')}")
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error al consultar el estado: {str(e)}")
                if hasattr(e, 'response') and hasattr(e.response, 'text'):
                    st.error(f"Detalles del error: {e.response.text}")