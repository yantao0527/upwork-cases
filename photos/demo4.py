from io import BytesIO
import zipfile
from azure.storage.blob import BlobServiceClient
from flask import Flask, send_file

app = Flask(__name__)

# Azure Blob Storage connection string
connection_string = "<your-connection-string>"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Container and blob name for the zipped folder
container_name = "<your-container-name>"
zip_blob_name = "<your-zip-blob-name>"

@app.route("/download/<filename>")
def download_file(filename):
    # Download the zipped folder from Azure Blob Storage
    zip_blob_client = blob_service_client.get_blob_client(container_name=container_name, blob=zip_blob_name)
    zip_bytes = zip_blob_client.download_blob().content_as_bytes()

    # Extract the file from the zipped folder
    with BytesIO(zip_bytes) as zip_file:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            file_content = zip_ref.read(filename)

    # Return the file as an attachment
    return send_file(BytesIO(file_content), attachment_filename=filename, as_attachment=True)
