from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# Replace these values with your own
connection_string = "your_connection_string"
container_name = "your_container_name"
blob_name = "your_blob_name"
expiry_hours = 1  # Set the expiry time in hours

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the account name and key from the connection string
account_name = blob_service_client.account_name
account_key = connection_string.split("AccountKey=")[1].split(";")[0]

# Set the expiry time for the SAS token
expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)

# Generate the SAS token
sas_token = generate_blob_sas(account_name,
                               account_key,
                               container_name,
                               blob_name,
                               permission=BlobSasPermissions(read=True),
                               expiry=expiry_time)

# Create the SAS URL
sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

print("SAS URL:", sas_url)
