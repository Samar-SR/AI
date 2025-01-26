import streamlit as st
import requests



with st.sidebar:

    st.header("File and PDF upload Section")
    uploaded_file  = st.file_uploader("Upload file",
                     help="Drag and drop your file here. Note: The file size limit is 10MB.",
                     type = ['txt','pdf']
                     )

    if st.button("Upload"):
        if uploaded_file is not None:
            # Send the file to the FastAPI endpoint
            try:
                # Prepare the file data
                FASTAPI_URL = "http://127.0.0.1:8000/upload"

                #files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

                # Make a POST request to FastAPI
                response = requests.post(FASTAPI_URL, files=uploaded_file)

                if response.status_code == 200:
                    # Display success message from FastAPI
                    result = response.json()
                    st.success(result['message'])
                else:
                    # Display error message from FastAPI
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload a PDF file!")

    link = st.text_input("Enter Url")

    if st.button("Process"):
        if link.strip():  # Check if the user has entered a valid URL
            try:
                # Send the URL to the FastAPI endpoint
                FASTAPI_URL = "http://127.0.0.1:8000/urlupload"

                payload = {"link": link}
                response = requests.post(FASTAPI_URL, json=payload)
                if response.status_code == 200:
                    # Display success message from FastAPI
                    result = response.json()
                    st.success(result['message'])
                else:
                    # Display error message from FastAPI
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL!")



st.header("Self Rag Bot")
question = st.text_input("Enter your question")

if  st.button("Submit"):
    if question.strip():
        try:
            url = "http://127.0.0.1:8000/chat"  # Replace with your FastAPI endpoint
            payload = {"question": question}
            response = requests.post(url, json=payload)

            # Handle response
            if response.status_code == 200:
                result = response.json()
                st.success(f"Answer: {result.get('answer', 'No answer provided')}")
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question!")



