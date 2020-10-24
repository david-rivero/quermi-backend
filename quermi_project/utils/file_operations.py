import json
import os
from io import BytesIO
from boxsdk import Client, JWTAuth

PRIVATE_KEY = os.getenv('BOX_PRIVATE_KEY') \
    .replace(':', ' ') \
    .replace('#', '=') \
    .encode().decode('unicode_escape')
CREDENTIALS_FILE_PATH = JWTAuth(
    client_id=os.getenv('BOX_CLIENT_ID'),
    client_secret=os.getenv('BOX_CLIENT_SECRET'),
    enterprise_id=os.getenv('BOX_ENTERPRISE_ID'),
    jwt_key_id=os.getenv('BOX_PUBLIC_KEY_ID'),
    rsa_private_key_data=PRIVATE_KEY,
    rsa_private_key_passphrase=os.getenv('BOX_PASSPHRASE')
)
MEDIA_FOLDER_NAME = 'quermi-media'
client = Client(CREDENTIALS_FILE_PATH)


def get_media_folder():
    """
        Auxiliar method, get media folder
    """
    root = client.root_folder()
    found_folder = False
    folder = None

    for subfolder in root.get_items():
        if subfolder.name == MEDIA_FOLDER_NAME:
            found_folder = True
            folder = subfolder
            break
    if not found_folder:
        folder = root.create_subfolder(MEDIA_FOLDER_NAME)
    return folder

def upload_file(binary_file, file_name, folder_name=''):
    """

    """
    media_folder = get_media_folder()
    current_folder = media_folder
    if folder_name:
        subfolder = media_folder.create_subfolder(folder_name)
        current_folder = subfolder
    result = current_folder.upload_stream(binary_file, file_name=file_name)

    # create_shared_link
    return result.get_shared_link_download_url() or ''

def remove_object(box_object):
    if box_object:
        box_object.delete()

def remove_file(filename, folder_name=MEDIA_FOLDER_NAME):
    """
        Remove file and folder related
    """
    media_folder = get_media_folder()
    current_folder = media_folder
    if folder_name is not MEDIA_FOLDER_NAME:
        current_folder = folder_name

    for item_file in current_folder.get_items():
        if item_file.name == filename:
            item_file.delete()
            break
    
    if current_folder is not MEDIA_FOLDER_NAME:
        current_folder.delete()

def find_object_from_media(query_name=''):
    query = client.search().query(query=query_name)
    for result in query:
        if result.name.find(query_name) is not -1:
            return result
