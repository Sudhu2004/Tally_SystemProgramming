
import streamlit as st
import requests
import io

UPLOAD_URL = "http://127.0.0.1:5000/upload"

uploaded_filename = None
uploaded_file_content = None
UPLOAD_URL = "http://127.0.0.1:5000/upload"
DOWNLOAD_URL = "http://127.0.0.1:5000/download"
def upload_file(file):
    
    """Upload a file to the Flask server"""
    global uploaded_filename, uploaded_file_content
    files = {'file': file.getvalue()}
    response = requests.post(UPLOAD_URL, files=files)
    if response.status_code == 200:
        uploaded_filename = file.name  # Save the filename for later use
        uploaded_file_content = file.getvalue()  # Save the file content for download
        st.success("File uploaded successfully")
    else:
        st.error("Failed to upload file")


def download_file(filename):
    """Download a file from the Flask server"""
    try:
        response = requests.get(f"{DOWNLOAD_URL}/{filename}", stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            st.success("File downloaded successfully")
        else:
            st.error(f"Failed to download file: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
# Streamlit UI
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    upload_file(uploaded_file)

if uploaded_filename:
    st.text(f"Uploaded file: {uploaded_filename}")
    
    # Create a download button
    st.download_button(
        label="Download",
        data=uploaded_file_content,
        file_name=uploaded_filename,
        mime="application/pdf"
    )
