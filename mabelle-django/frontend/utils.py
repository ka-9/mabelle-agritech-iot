import os
from dotenv import load_dotenv
import requests
import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration
from fpdf import FPDF

load_dotenv()

def load_dashboard_ids():

    # Define the environment variable names and their corresponding IDs
    env_variable_ids = {
        "FLAG_ID": None,
        "SEEDS_ID": None,
        "DISTANCE_ID": None,
    }

    # Iterate over the environment variable names and get their values
    for env_variable, id_name in env_variable_ids.items():
        if env_variable in os.environ:
            env_variable_ids[env_variable] = os.environ[env_variable]

    # Extract the IDs from the dictionary and put them into an array
    ids = list(env_variable_ids.values())
    return ids

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

def post_data(access_token, property_id, property_value):
    # Configure the Arduino IoT client
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)

    thing_id = os.environ['THING_ID']

    properties_api = iot.PropertiesV2Api(client)

    try:
        properties_api.properties_v2_publish(thing_id, property_id, {"value" : property_value})
        print(f"Published {property_value} to {property_id}")
    except iot.ApiException as e:
        print("Got an exception: {}".format(e))
        return None
    
# Function to create a PDF from the DataFrame
def create_pdf(df, filename):
    pdf = FPDF(orientation='L')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    pdf.add_page()
    pdf.set_font("Arial", size=8)

    # Add table headers
    pdf.cell(0, 10, 'core_readings Table Data', ln=True, align='C')
    pdf.ln(10)
    col_width = pdf.w / (len(df.columns) + 1)
    row_height = 10

    for column in df.columns:
        pdf.cell(col_width, row_height, column, border=1, align='C')
    pdf.ln(row_height)

    # Add data rows
    for index, row in df.iterrows():
        for col in row:
            pdf.cell(col_width, row_height, str(col), border=1, align='C')
        pdf.ln(row_height)

    pdf.output(filename)