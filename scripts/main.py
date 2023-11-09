# Utils
import yaml
from yaml.loader import SafeLoader
import sys
sys.path.append('../data/')
sys.path.append("../scripts/")
sys.path.append("../config/")
import os
from utils import load_audios, download_audio, move_audio
# Data
import pandas as pd
# Streamlit
import streamlit as st
import streamlit_authenticator as stauth



# Look for CSV file and load the dataset
def main():
    # Login
    try:
        with open('config/config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
           
    except:
        st.title("Error reading .yaml file")
    
   
    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')


    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main', key='unique_key')
        page = st.sidebar.selectbox("Select a page", ("Load Data",))

        
        # Pages
        if page == "Load Data":
            s3_name = "s3-drop-audio"
            
            audio_list  = load_audios()
            

            bring_audios(audio_list, s3_name)

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        

   

def bring_audios(audio_list, s3_name):
    
    st.title("Clasificación de Audios")
    download_path = 'files'
    # Seleccionar Audio
    selected_audio_id = st.selectbox("Selecciona un Audio:", audio_list)
    
    if selected_audio_id:
        st.title("Clasificar el Audio")
        audio_path = download_audio(s3_name, selected_audio_id, download_path)
        if audio_path:
            st.audio(audio_path) 
    # Seleccionar clasificación
    selected_option = st.selectbox("Selecciona una Clasificación:", ("Bebe Llorando", "Conversación", "Gato", "Perro", "Otro"), key=1)
    
    # Realizar una acción basada en la selección
    if selected_option:
        st.write(f"Has seleccionado la clasificación: {selected_option}")
    
    confirm_button = st.button("Confirmar Etiquetado", type='primary')

    if confirm_button:
        if selected_audio_id in audio_list:
            try:
                st.title("Audio Etiquetado")
                move_audio(selected_audio_id, s3_name, selected_option)
            except:
                st.title("Error Etiquetando el Audio")


if __name__ == "__main__":
    main()