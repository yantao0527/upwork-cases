import os
import tempfile
import zipfile
from io import BytesIO
from flask import Flask, request, send_file
from azure.storage.blob import BlobServiceClient, BlobClient

app = Flask(__name__)

# Azure Blob Storage connection string and container name
connection_string = "your_connection_string"
container_name = "your_container_name"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

@app.route('/download-folder')
def download_folder():
    # Get the folder name from the request arguments
    folder_name = request.args.get('folder_name')
    
    # Create a temporary file to store the zip file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    # Create the zip file and add all files in the folder to it
    with zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED) as zip:
        for blob in blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=folder_name):
            blob_client = blob_service_client.get_blob_client(container_name, blob.name)
            blob_data = blob_client.download_blob().readall()
            file_name = os.path.basename(blob.name)
            zip.writestr(file_name, blob_data)
    
    # Close the temporary file
    temp_file.close()
    
    # Send the zip file to the client
    return send_file(temp_file.name, as_attachment=True, attachment_filename=f'{folder_name}.zip')
