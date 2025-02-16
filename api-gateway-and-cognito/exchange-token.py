import requests
import base64

# Define the necessary parameters
client_id = '10vkdof0fa8kg9ilmj9f011ru6'
client_secret = '1st7qnb3a0dem7le5sm0n828m0lv7h4c977aoek6m7usq894n3u4'
redirect_uri = 'https://kientrucsugiaiphap.com'
token_endpoint = 'https://ap-southeast-19vxnycvv4.auth.ap-southeast-1.amazoncognito.com/oauth2/token'
authorization_code = 'cb08f3e3-b883-42ba-8fb8-b06507849818'

# Encode the client ID and client secret
client_credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')

# Prepare the request headers and body
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {encoded_credentials}'
}

body = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri
}

# Make the POST request to the token endpoint
response = requests.post(token_endpoint, headers=headers, data=body)

# Check if the request was successful
if response.status_code == 200:
    tokens = response.json()
    id_token = tokens.get('id_token')
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    print('ID Token:', id_token)
    print('Access Token:', access_token)
    print('Refresh Token:', refresh_token)
else:
    print('Failed to exchange authorization code for tokens:', response.text)