# OneDrive utils

Basic utils using https://github.com/OneDrive/onedrive-sdk-python

OneDrive API documentation: https://dev.onedrive.com

## Auth

- Create an app in https://apps.dev.microsoft.com/
- Get **Client ID** and **Secret** from this app and set them as environment variables `CLIENT_ID` and `CLIENT_SECRET`
- Add URL for redirect `http://localhost:8080/`

### Virtualenv bin/postactivate sample
```
export CLIENT_ID=??????
export CLIENT_SECRET=??????
```

## Scripts

Eg. `python list.py "/Parent Folder/Subfolder"`

### dl.py <path>
- Download all folders, subfoldres and files for given path

### duplicates.py <path>
- Check duplicates for given path

### list.py <path> --depth=?
- List folders for given path

#### args
**--depth=?** *(default = 0)*
- ? can be number from 1 to N
- ? = 0 is indefinitely
