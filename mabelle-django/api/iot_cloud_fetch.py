import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration
from dotenv import load_dotenv
import requests
import asyncio
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
async def fetch_data(access_token):
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)

    thing_id = os.environ['THING_ID']
    api = iot.PropertiesV2Api(client)
    
    data = ""

    try:
        # Fetch the Thing asynchronously
        data = await asyncio.to_thread(api.properties_v2_list, thing_id)
    except iot.ApiException as e:
        print("Got an exception: {}".format(e))
        return None

    return data

def post_data(access_token, property_name, property_value):
    # Configure the Arduino IoT client
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)

    thing_id = os.environ['THING_ID']

    # Initialize the PropertiesV2Api
    api = iot.PropertiesV2Api(client)

    pid = property_name
    model_property = iot.ModelProperty() # ModelProperty | PropertyPayload describes a property of a thing. No field is mandatory

    print(model_property)

    try:
        # update properties_v2
        api_response = api.properties_v2_update(thing_id, pid, model_property)
        print(api_response)
    except ApiException as e:
        print("Exception when calling PropertiesV2Api->properties_v2_update: %s\n" % e)

# Code testing
if __name__ == '__main__':
    access_token = get_access_token()
    post_data(access_token, 'Seed', 10)
    # async def main():
    #     for i in range(1):  # Adjust for loop for as many readings as needed per method call
    #         data = await fetch_data(access_token)
    #         print(data)
    # asyncio.run(main())