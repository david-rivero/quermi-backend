import os
from io import BytesIO
from boxsdk import Client, JWTAuth, OAuth2


CREDENTIALS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'credentials_box_config.json'
)
MEDIA_FOLDER_NAME = 'quermi-media'

config = JWTAuth.from_settings_file(CREDENTIALS_FILE_PATH)
client = Client(config)


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
