from azure.storage.blob import BlobServiceClient
from flask import Flask, request

app = Flask(__name__)

# Define your Azure Blob Storage credentials
account_name = 'your_account_name'
account_key = 'your_account_key'
container_name = 'your_container_name'

# Create BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net")

@app.route('/upload', methods=['POST'])
def upload_files():
    # Get files from the request
    files = request.files.getlist('file')

    # Create container if not exists
    container_client = blob_service_client.get_container_client(container_name)
    container_client.create_container()

    # Upload each file to Azure Blob Storage
    for file in files:
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file.read())

    return 'Files uploaded successfully!'

@app.route('/download', methods=['GET'])
def download_files():
    # Get the name of the file to download from the request
    file_name = request.args.get('file_name')

    # Get the blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    # Download the file
    file_content = blob_client.download_blob().content_as_text()

    return file_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
