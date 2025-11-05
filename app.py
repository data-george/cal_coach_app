import requests
import re
import base64
import os
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model, ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

### You will add code from Step 2 here

credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                   # api_key = "<YOUR_API_KEY>" # Normally you'd put an API key here, but we've got you covered here
                  )
client = APIClient(credentials)

model_id = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"
project_id = "skills-network"
params = TextChatParameters()

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params=params
)

### Step 3

def input_image_setup(uploaded_file):
    """
    Encodes the uploaded image file into a base64 string to be used with AI models.

    Parameters:
    - uploaded_file: File-like object uploaded via a file uploader (Streamlit or other frameworks)

    Returns:
    - encoded_image (str): Base64 encoded string of the image data
    """
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.read()

        # Encode the image to a base64 string
        encoded_image = base64.b64encode(bytes_data).decode("utf-8")

        return encoded_image
    else:
        raise FileNotFoundError("No file uploaded")

### Step 4

def format_response(response_text):
    """
    Formats the model response to display each item on a new line as a list.
    Converts numbered items into HTML `<ul>` and `<li>` format.
    Adds additional HTML elements for better presentation of headings and separate sections.
    """
    # Replace section headers that are bolded with '**' to HTML paragraph tags with bold text
    response_text = re.sub(r"\*\*(.*?)\*\*", r"<p><strong>\1</strong></p>", response_text)

    # Convert bullet points denoted by "*" to HTML list items
    response_text = re.sub(r"(?m)^\s*\*\s(.*)", r"<li>\1</li>", response_text)

    # Wrap list items within <ul> tags for proper HTML structure and indentation
    response_text = re.sub(r"(<li>.*?</li>)+", lambda match: f"<ul>{match.group(0)}</ul>", response_text, flags=re.DOTALL)

    # Ensure that all paragraphs have a line break after them for better separation
    response_text = re.sub(r"</p>(?=<p>)", r"</p><br>", response_text)

    # Ensure the disclaimer and other distinct paragraphs have proper line breaks
    response_text = re.sub(r"(\n|\\n)+", r"<br>", response_text)

    return response_text

### Step 5

@app.route('/generate', methods=['POST'])
def index():
    # This is where you'll add your main application logic later, after step 5
    #TODO

if __name__ == '__main__':
    app.run(debug=True)