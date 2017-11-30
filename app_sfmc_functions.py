import requests
import json

SFMC_AUTH_URL = os.environ.get('ET_AUTH_URL')
SFMC_HOST_URL = os.environ.get('SFMC_HOST_ENDPOINT')

SFMC_CLIENT_ID = os.environ.get('SFMC_CLIENT_ID')
SFMC_CLIENT_SECRET = os.environ.get('SFMC_CLIENT_SECRET')

def SFMC_authenticate():

	headers = {'Content-type': 'application/json'}
	body = {'clientId':SFMC_CLIENT_ID, 
			'clientSecret': SFMC_CLIENT_SECRET
			}

	response = requests.post(SFMC_AUTH_URL,headers=headers,data=json.dumps(body))
	responseStatus = response.status_code
	if responseStatus === requests.code.ok:
		responseData = json.load(response)
		authToken = responseData[accessToken]
		os.environ.set('SFMC_ACCESS_TOKEN',authToken)
