import os
import tempfile
import zipfile
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

app = Flask(__name__)

load_dotenv()
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING') # retrieve the connection string from the environment variable
container_name = os.getenv('AZURE_CONTAINER_NAME') # container name in which images will be store in the storage account
request_extensions = os.getenv('REQUESTED_EXTENSIONS').split(" ") # Let the zip file include only files of certain extensions
public_access = False
expiry_hours = 1  # Set the expiry time in hours

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def zip_exists(zip_blob_name):
    print(f"zip_exists zip_blob_name: [{zip_blob_name}]")
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=zip_blob_name)
        res = blob_client.exists()
        print("zip_exists result", res)
        return res
    except Exception as e:
        return False

def match_extension(file_name):
    base_name = os.path.basename(file_name)
    base_name = base_name.lower()
    for ext in request_extensions:
        if base_name.endswith(ext):
            return True
    return False

@app.route('/download-folder')
def download_folder():
    # Get the folder name from the request arguments
    folder_name = request.args.get('folder_name')
    zip_blob_name = f'{folder_name}.zip'
    folder_name = folder_name + "/"

    if not zip_exists(zip_blob_name):
        # Create a temporary file to store the zip file
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        # Create the zip file and add all files in the folder to it
        with zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED) as zip:
            for blob in blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=folder_name):
                if not match_extension(blob.name):
                    continue
                blob_client = blob_service_client.get_blob_client(container_name, blob.name)
                blob_data = blob_client.download_blob().readall()
                file_name = blob.name.replace(folder_name, "")
                print(f'file [{file_name}] add to [{zip_blob_name}]')
                zip.writestr(file_name, blob_data)

        # Close the temporary file
        temp_file.close()
        # print(temp_file.name)

        # Store zip file to ABS
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=zip_blob_name)
        with open(temp_file.name, "rb") as data:
            blob_client.upload_blob(data)

        # Remove the temporary file
        os.remove(temp_file.name)
        print("store zip file " + zip_blob_name)

    if public_access:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=zip_blob_name)
        return jsonify({"url": blob_client.url})
    else:
        # Get the account name and key from the connection string
        account_name = blob_service_client.account_name
        account_key = connection_string.split("AccountKey=")[1].split(";")[0]

        # Set the expiry time for the SAS token
        expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)

        # Generate the SAS token
        sas_token = generate_blob_sas(account_name=account_name,
                                    account_key=account_key,
                                    container_name=container_name,
                                    blob_name=zip_blob_name,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=expiry_time)

        # Create the SAS URL
        sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{zip_blob_name}?{sas_token}"
        #print(sas_url)

        # return sas url to the client
        return jsonify({"url": sas_url})

if __name__ == '__main__':
    # The port number is  not important for GUnicorn, 
    # let's keep 5002 so we can work outside docker easily
    app.run(host= '127.0.0.1', port='2200', debug=True)
