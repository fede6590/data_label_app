import boto3
import pandas as pd
import os 
import datetime
import streamlit as st
try:
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('s3-drop-audio')
except:
    st.title("The token has expired")
    

def load_audios(s3_name = "s3-drop-audio"):
    audio_list = []
    
    for my_bucket_object in bucket.objects.all():
        key_parts = my_bucket_object.key.split('/')
        if len(key_parts) == 1 and my_bucket_object.key.endswith('.wav'):
            audio_list.append(my_bucket_object.key)
    
    return audio_list



def download_audio(bucket_name, object_key, local_file_path = "files"):
    
    audio_path = os.path.join(local_file_path, object_key)
    if not os.path.exists(audio_path):
        s3.Object(bucket_name, object_key).download_file(audio_path)
    else:
        pass
    return audio_path


def move_audio(file_key, bucket_name, directory):
    try:
        create_directory(bucket_name, directory)
        # Specify the source and destination paths
        source_key = file_key
        destination_key = f'{directory}/{file_key}'

        # Copy the object to the destination
        s3.Object(bucket_name, destination_key).copy_from(CopySource={'Bucket': bucket_name, 'Key': source_key})

        # Delete the original object (file)
        s3.Object(bucket_name, source_key).delete()

    except:
        print("Error creando el directorio dentro del S3")
    

def create_directory(bucket_name, directory):

    
    # Validate if the directory already exists
    objects = s3.Bucket(bucket_name).objects.filter(Prefix=directory)
    folder_exists = any(obj.key == directory for obj in objects)
    if folder_exists:
        print(f"Folder '{directory}' exists in S3 bucket '{bucket_name}'.")
    else:
        print(f"Folder '{directory}' does not exist in S3 bucket '{bucket_name}'.")
        # Create an S3 object to represent the folder (notice the trailing '/')
        folder = s3.Object(bucket_name, f"{directory}/")
        # Create the folder by putting an empty string as the object's content
        folder.put(Body='')
        print(f"Folder '{directory}' created in S3 bucket '{bucket_name}'.") 