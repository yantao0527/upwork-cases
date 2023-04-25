import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request

app = Flask(__name__)

# Azure Blob Storage configuration
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=<your-account-name>;AccountKey=<your-account-key>;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "<your-container-name>"
THUMBNAIL_FOLDER_NAME = "thumbnails"

def is_image(filename):
    if "images" in filename:
        for ext in [".png", "gif", "jpg"]:
            if ext in filename:
                return True
    return False

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file from the request
    for file in request.files.getlist("photos"):
        # Create a BlobServiceClient object to interact with the Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

        # Create a container if it doesn't exist
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        if not container_client.exists():
            container_client.create_container()

        # Upload the file to Azure Blob Storage with the original filename
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        blob_client.upload_blob(file.read(), overwrite=True)

        # Create a thumbnail if the uploaded file is an image
        if is_image(file.filename):
            from PIL import Image

            # Open the uploaded image with PIL
            img = Image.open(file.stream)

            # Create the thumbnail
            thumbnail_size = (100, 100)
            thumbnail = img.copy()
            thumbnail.thumbnail(thumbnail_size)

            # Generate a unique filename for the thumbnail
            thumbnail_filename = file.filename.replace("images", "thumbnails")

            # Upload the thumbnail to Azure Blob Storage with the original filename
            thumbnail_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=thumbnail_filename)
            with BytesIO() as output:
                thumbnail.save(output, format='JPEG')
                thumbnail_blob_client.upload_blob(output.getvalue(), overwrite=True)

    return 'File uploaded successfully!'

