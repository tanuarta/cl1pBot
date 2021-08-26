from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '1SvBMA88yCqetZbf6ICxyZ47HkBX5n919'

def upload(filename):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }

    print("Uploading File")

    media = MediaFileUpload(filename, mimetype='video/mp4')
    file = service.files().create(  body=file_metadata,
                                    media_body=media,
                                    fields='id'
                                ).execute()

    print("File upload successful")

    fileId = file.get('id')

    permission = {
            'type': 'anyone',
            'role': 'reader',
        }

    service.permissions().create(fileId=fileId, body=permission).execute()
    
    return fileId
    