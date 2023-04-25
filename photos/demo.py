from azure.storage.blob import BlobServiceClient
from flask import Flask, request, send_file

app = Flask(__name__)

# Connect to Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string("your-connection-string")

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from the request
    file = request.files['file']

    # Create a BlobClient object for the file
    blob_client = blob_service_client.get_blob_client(container="your-container", blob=file.filename)

    # Upload the file to Azure Blob Storage
    blob_client.upload_blob(file)

    return "File uploaded successfully!"

@app.route('/download/<filename>')
def download_file(filename):
    # Create a BlobClient object for the file
    blob_client = blob_service_client.get_blob_client(container="your-container", blob=filename)

    # Download the file from Azure Blob Storage
    stream = blob_client.download_blob().content_as_bytes()

    # Return the file to the user
    return send_file(stream, attachment_filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
