import os

import onedrivesdk


def authenticate_and_get_client():
    assert 'CLIENT_ID' in os.environ, 'CLIENT_ID is not set for this environment'
    assert 'CLIENT_SECRET' in os.environ, 'CLIENT_SECRET is not set for this environment'

    client_id=os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    redirect_uri = 'http://localhost:8080/'

    api_base_url='https://api.onedrive.com/v1.0/'
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readonly']

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider=http_provider,
        client_id=client_id,
        scopes=scopes)

    try:
        auth_provider.load_session()

        auth_provider.refresh_token()

        client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

    except:
        client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
        auth_url = client.auth_provider.get_auth_url(redirect_uri)
        # Ask for the code
        print('Paste this URL into your browser, approve the app\'s access.')
        print('Copy everything in the address bar after "code=", and paste it below.')
        print(auth_url)
        code = input('Paste code here: ')

        client.auth_provider.authenticate(code, redirect_uri, client_secret)

        auth_provider.save_session()

    return client