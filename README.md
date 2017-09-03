# OneDrive utils

Basic utils using https://github.com/OneDrive/onedrive-sdk-python

OneDrive API documentation: https://dev.onedrive.com

## Auth

- Create an app in https://apps.dev.microsoft.com/
- Get Client ID and Secret from this app
- Add URL for redirect `http://localhost:8080/`

## Scripts

Eg. `python list.py "/Parent Folder/Subfolder"`

### dl.py <path>
- Download all folders, subfoldres and files for given path

### duplicates.py <path>
- Check duplicates for given path

### list.py <path>
- List folders for given path
