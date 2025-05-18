from azure.storage.blob import BlobServiceClient, BlobBlock, ContentSettings, PublicAccess
import os
import uuid
import logging
import time
from azure.core.exceptions import ServiceRequestError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Azure config
STORAGE_ACCOUNT_NAME = ""
STORAGE_ACCOUNT_KEY = ""
CONTAINER_NAME = ""
LOCAL_VIDEO_FILE = "./nancy_ai_video.mp4"

# Upload settings
CHUNK_SIZE = 512 * 1024  # 512 KB chunks for better reliability
UPLOAD_TIMEOUT = 900     # Timeout per operation in seconds
MAX_RETRIES = 5          # Retry count for each chunk
RETRY_DELAY = 3          # Delay between retries in seconds

# Set up blob client
connect_str = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Ensure container exists
try:
    logger.info(f"Checking if container '{CONTAINER_NAME}' exists...")
    container_client.create_container()
    logger.info(f"Container '{CONTAINER_NAME}' created.")
except Exception:
    logger.info(f"Container '{CONTAINER_NAME}' already exists.")

# Make container public
logger.info("Setting container access to public...")
container_client.set_container_access_policy(signed_identifiers={}, public_access=PublicAccess.Container)

# Prepare for block upload
blob_name = os.path.basename(LOCAL_VIDEO_FILE)
blob_client = container_client.get_blob_client(blob_name)
file_size = os.path.getsize(LOCAL_VIDEO_FILE)
logger.info(f"Uploading '{LOCAL_VIDEO_FILE}' ({file_size / (1024 * 1024):.2f} MB) in chunks...")

block_list = []
uploaded = 0
block_num = 0

with open(LOCAL_VIDEO_FILE, "rb") as file:
    while True:
        chunk = file.read(CHUNK_SIZE)
        if not chunk:
            break
        block_id = str(uuid.uuid4())

        # Retry logic
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                blob_client.stage_block(
                    block_id=block_id,
                    data=chunk,
                    timeout=UPLOAD_TIMEOUT
                )
                block_list.append(BlobBlock(block_id=block_id))
                uploaded += len(chunk)
                progress = (uploaded / file_size) * 100
                logger.info(f"Uploaded chunk {block_num + 1}, Progress: {progress:.2f}%")
                break
            except ServiceRequestError as e:
                logger.warning(f"Attempt {attempt} failed for chunk {block_num + 1}: {e}")
                if attempt == MAX_RETRIES:
                    logger.error("Upload failed: Max retries reached.")
                    raise
                time.sleep(RETRY_DELAY)

        block_num += 1

# Commit all uploaded blocks
blob_client.commit_block_list(block_list, content_settings=ContentSettings(content_type='video/mp4'), timeout=UPLOAD_TIMEOUT)
logger.info("✅ Upload completed successfully.")

# Public URL
blob_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
print(f"✅ Uploaded '{LOCAL_VIDEO_FILE}' successfully.")
print(f"🌐 Public URL: {blob_url}")
