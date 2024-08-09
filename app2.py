import os
import gridfs

from pymongo import MongoClient

URL = "mongodb+srv://sudhrshan18:NaZFjUKdKlr2JrZF@cluster0.ma0bt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"



def mongo_conn():
    """create a connection"""
    try:
        conn = MongoClient(URL, port=27017)
        print("Mongodb Connected", conn)
        return conn.Ytube
    except Exception as err:
        print(f"Error in mongodb connection: {err}")


def upload_file(file_loc, file_name, fs):
    """upload file to mongodb"""
    with open(file_loc, 'rb') as file_data:
        data = file_data.read()

    # put file into mongodb
    fs.put(data, filename=file_name)
    print("Upload Complete")


def download_file(download_loc, db, fs, file_name):
    """download file from mongodb"""
    data = db.youtube.files.find_one({"filename": file_name})

    fs_id = data['_id']
    out_data = fs.get(fs_id).read()

    with open(download_loc, 'wb') as output:
        output.write(out_data)

    print("Download Completed!")

import streamlit as st

if __name__ == '__main__':
    # Streamlit file uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Define the destination path to save the uploaded file
        file_name = uploaded_file.name
        file_loc = os.path.join(os.getcwd(), file_name)
        down_loc = os.path.join(os.getcwd(), file_name)
        save_path = os.path.join(os.getcwd(), uploaded_file.name)
        
        # Save the uploaded file to the destination path
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.write(f"File saved at: {save_path}")

    db = mongo_conn()
    fs = gridfs.GridFS(db, collection="youtube")

    # upload file
    upload_file(file_loc=file_loc, file_name=file_name, fs=fs)
    # download file
    download_file(down_loc, db, fs, file_name)