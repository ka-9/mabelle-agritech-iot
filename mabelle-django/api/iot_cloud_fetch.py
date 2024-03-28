import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration
from dotenv import load_dotenv
import requests
import os

load_dotenv()

# This method generates the access token so that we can interact with cloud (DO NOT TOUCH, thank you)
def get_access_token():
    # Define token endpoint and credentials
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    # Define token request parameters
    token_params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': "https://api2.arduino.cc/iot",
    }

    # Send token request
    try:
        response = requests.post(token_url, data=token_params)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.RequestException as e:
        print("Token request failed:", e)
        exit()

    # Check if request was successful
    if response.status_code == 200:
        # Extract token from response
        token_data = response.json()
        access_token = token_data.get('access_token')
        if access_token:
            print("Access token granted")
        else:
            print("Token request succeeded, but access token not found in response.")
    elif response.status_code == 401:
        print("Token request failed: Unauthorized. Please verify client credentials.")
    else:
        print("Token request failed with status code:", response.status_code)

    return access_token


# This method fetches data from the iot cloud using the generated access token
def fetch_data(access_token):

    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)

    thing_id = os.environ['THING_ID']
    api = iot.PropertiesV2Api(client)

    # Here is the code to fetch the Thing
    try:
        data = api.properties_v2_list(thing_id)
    except ApiException as e:
        print("Got an exception: {}".format(e))

    if data:
        for obj in data:
            value_updated_at = obj.value_updated_at
            last_value = obj.last_value
            name = obj.name
            print(f"Name: {name}, Last Value: {last_value}, Value Updated At: {value_updated_at}")


# Code testing
if __name__ == '__main__':
    access_token = get_access_token()
    for i in range(1): # Adjust for loop for as many readings as needed per method call!
        fetch_data(access_token)