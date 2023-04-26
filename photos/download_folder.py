import os
import tempfile
import zipfile
from io import BytesIO
from datetime import datetime, timedelta
from flask import Flask, request, send_file
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

app = Flask(__name__)

# Azure Blob Storage connection string and container name
connection_string = "your_connection_string"
container_name = "your_container_name"
expiry_hours = 1  # Set the expiry time in hours

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def zip_exists(folder_name):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'{folder_name}.zip')
        blob_client.get_blob_properties()
        return True
    except Exception as e:
        return False

@app.route('/download-folder')
def download_folder():
    # Get the folder name from the request arguments
    folder_name = request.args.get('folder_name')

    if not zip_exists(folder_name):
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

        # Store zip file to ABS
        with open(temp_file.name, "rb") as data:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'{folder_name}.zip')
            blob_client.upload_blob(data)

        # Remove the temporary file
        os.remove(temp_file.name)

    # Get the account name and key from the connection string
    account_name = blob_service_client.account_name
    account_key = connection_string.split("AccountKey=")[1].split(";")[0]

    # Set the expiry time for the SAS token
    expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)

    # Generate the SAS token
    sas_token = generate_blob_sas(account_name,
                                account_key,
                                container_name,
                                f'{folder_name}.zip',
                                permission=BlobSasPermissions(read=True),
                                expiry=expiry_time)

    # Create the SAS URL
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{f'{folder_name}.zip'}?{sas_token}"

    # return sas url to the client
    return {sas_url: sas_url}
