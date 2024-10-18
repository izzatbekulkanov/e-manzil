import requests

from urllib.parse import quote  # quote funksiyasini import qilamiz

class oAuth2Client:
    def __init__(self, client_id, client_secret, redirect_uri, authorize_url, token_url, resource_owner_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.resource_owner_url = resource_owner_url

    def get_authorization_url(self, state=None):
        # redirect_uri ni percent-encoding usuli bilan kodlaymiz
        encoded_redirect_uri = quote(self.redirect_uri)
        url = f"{self.authorize_url}?client_id={self.client_id}&redirect_uri={encoded_redirect_uri}&response_type=code"
        if state:
            url += f"&state={state}"
        return url

    def get_access_token(self, auth_code):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post(self.token_url, data=payload)
        response.raise_for_status()  # Xatolarni tekshirish
        return response.json()

    def get_user_details(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.resource_owner_url, headers=headers)
        response.raise_for_status()  # Xatolarni tekshirish
        return response.json()
