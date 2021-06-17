from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Gdrive:
    def __init__(self, id_path):
        self.id = id_path
        gauth = GoogleAuth()
        #criar arquivo mycreds.txt com o token obtido em: https://console.developers.google.com/

        gauth.LoadCredentialsFile('mycreds.txt')

        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        gauth.SaveCredentialsFile("mycreds.txt")

        self.drive = GoogleDrive(gauth)
        self.file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(self.id)}).GetList()

    def get_files(self):
        for file in self.file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            file.GetContentFile(file['title'])

    def download_files(self):
        for i, file in enumerate(sorted(self.file_list, key=lambda x: x['title']), start=1):
            print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(self.file_list)))
            file.GetContentFile(file['title'])

    def upload_files(self, files:list):
        upload_file_list = files
        for upload_file in upload_file_list:
            gfile = self.drive.CreateFile({'parents': [{'id': self.id}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload()  # Upload the file.