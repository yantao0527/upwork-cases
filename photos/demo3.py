import zipfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from flask import Flask, request, jsonify

app = Flask(__name__)

# define the connection string and container name
connection_string = "<your-connection-string>"
container_name = "<your-container-name>"

@app.route('/upload', methods=['POST'])
def upload_zip():
    # get the files from the request
    files = request.files.getlist("files")

    # create a zip file of the selected files
    with zipfile.ZipFile("myzipfile.zip", "w") as zip_file:
        for file in files:
            zip_file.write(file.filename)

    # upload the zip file to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client("myzipfile.zip")
    with open("myzipfile.zip", "rb") as data:
        blob_client.upload_blob(data)

    return jsonify({"message": "Upload successful!"})
