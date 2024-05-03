import matplotlib.pyplot as plt
import numpy as np
from frontend.constants import *
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def create_fertilizer_bar_graph(fertilizer_value,max_fertilizer_value):
    fig, ax = plt.subplots(figsize=(20, 1))  # Adjust figsize as needed

    # Create bars for water and fertilizer
    ax.barh(y=0, width=max_fertilizer_value, color=LIGHT_GREEN, height=0.2, edgecolor='none')
    ax.barh(y=0, width=fertilizer_value, color=DARK_GREEN, height=0.2, edgecolor='none')

    # Hide axes
    ax.axis('off')
  
    # Show the plot
    st.pyplot(fig)

def create_Water_bar_graph(Water_value,max_water_value):
    fig, ax = plt.subplots(figsize=(20, 1))  # Adjust figsize as needed

    # Create bars for water and fertilizer
    ax.barh(y=0, width=max_water_value, color=LIGHT_GREY, height=0.2, edgecolor='none')
    ax.barh(y=0, width=Water_value, color=GREY_COLOR, height=0.2, edgecolor='none')

    # Hide axes
    ax.axis('off')
  
    # Show the plot
    st.pyplot(fig)


def generate_prediction():
    forecast_list = [
        {
            'time': '13:00 PM',
            'temp': 70,
            'hum':50
        },
        {
            'time': '14:00 PM',
            'temp': 72,
            'hum':56
        },
        {
            'time': '15:00 PM',
            'temp': 68,
            'hum':90
        },
        {
            'time': '16:00 PM',
            'temp': 80,
            'hum':70
        },
        {
            'time':' 17:00 PM',
            'temp': 75,
            'hum':20
        },
    ]

    return forecast_list

def calc_delta(forecast_list):
    for i in range(len(forecast_list) - 1):
        delta_temp = forecast_list[i + 1]['temp'] - forecast_list[i]['temp']
        delta_hum = forecast_list[i + 1]['hum'] - forecast_list[i]['hum']
        forecast_list[i + 1]['delta_temp'] = delta_temp
        forecast_list[i + 1]['delta_hum'] = delta_hum

    forecast_list[0]['delta_temp'] = 0
    forecast_list[0]['delta_hum'] = 0

    return forecast_list

    

def generate_distance_line(distance, nb_of_seeds, positions):
    fig, ax = plt.subplots(figsize=(8, 1))  # Specify a smaller figure size
    ax.plot([0, distance], [0, 0], color='black', linewidth=2)  # Draw the main line

    for pos in positions:
        if pos > distance:
            st.write(f"Mark at position {pos} cannot be drawn because it is outside the designated distance")
        else:
            ax.scatter(pos, 0, color="red", marker='o', zorder=5)  # Plot circles at positions
            ax.text(pos, -0.1, str(pos), ha='center', fontsize=8)  # Label the marks with position

    ax.set_xlim(0, distance)  # Set x-axis limits
    ax.axis('off')  # Turn off axis
    if len(positions) == nb_of_seeds:
        st.write("All the seeds have been planted")
    return fig


def generate_npk_piechart():
    data = {
        'N': 10,
        'P': 30,
        'K': 60
    }
    labels = data.keys()
    sizes = data.values()
    colors = [LIGHT_GREEN, REG_GREEN, DARK_GREEN]

    fig, ax = plt.subplots(figsize=(8,8))

    # Create the pie chart with white circle in the center
    pie_wedge_collection = ax.pie(sizes, labels=labels, startangle=90, colors=colors)[0]
    for pie_wedge in pie_wedge_collection:
        pie_wedge.set_edgecolor('white')  # Set edge color to white

    # Draw a white circle at the center
    centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white', linewidth=1.25)
    ax.add_artist(centre_circle)

    # Create legend manually
    legend_labels = [f'{label} ({size}%)' for label, size in zip(labels, sizes)]
    ax.legend(pie_wedge_collection, legend_labels, loc='center', fontsize='medium')

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig

def get_water_fertilizer_percentages(values_dict):
    water_percentage_used = int((values_dict["water"] / WATER_CONTAINER_VOLUME) * 100)
    fertilizer_percentage_used = int((values_dict["water"] / WATER_CONTAINER_VOLUME) * 100)

    percentage_dict = {
        "water_used_percentage": water_percentage_used,
        "fertilizer_used_percentage": fertilizer_percentage_used
    }
    return percentage_dict


def generate_temphumidity_barchart():
    temp_humidity_data = {
        'Meter': ['1', '2', '3', '4', '5'],
        'Temperature': np.random.uniform(15, 30, 5),
        'Humidity': np.random.uniform(30, 70, 5)
    }
    temp_humidity_df = pd.DataFrame(temp_humidity_data)

    fig, ax = plt.subplots()

    # Define the width of each bar
    bar_width = 0.25

    # Define the position of the bars for humidity and temperature
    index = np.arange(len(temp_humidity_df))

    # Plot temperature bars
    ax.bar(index - bar_width / 2, temp_humidity_df['Temperature'], bar_width, color=LIGHT_GREEN)
    ax.set_ylabel('Temperature (C)', color=DARK_GREEN)

    # Plot humidity bars
    ax2 = ax.twinx()
    ax2.bar(index + bar_width / 2, temp_humidity_df['Humidity'], bar_width, color=LIGHT_GREY)
    ax2.set_ylabel('Humidity (g/m^3)', color=GREY_COLOR)
    # Set labels and title
    ax.set_xlabel('Distance (m)')

    ax.set_title('Temperature and Humidity')
    ax.set_xticks(index)
    ax.set_xticklabels(temp_humidity_df['Meter'])

    return fig

def classify_nitrogen(nitrogen_value):
   
    if nitrogen_value >= 0 and nitrogen_value <= 20:
        return 0
   
    elif nitrogen_value > 20 and nitrogen_value <= 40:
        return 1
   
    elif nitrogen_value > 40 and nitrogen_value <= 60:
        return 2
   
    elif nitrogen_value > 60 and nitrogen_value <= 80:
        return 3
   
    elif nitrogen_value >80 and nitrogen_value <= 100:
        return 4
   
    elif nitrogen_value > 100 and nitrogen_value <= 120:
        return 5
    
    elif nitrogen_value > 120 and nitrogen_value <= 140:
        return 6
    
    elif nitrogen_value > 140 and nitrogen_value <= 160:
        return 7
   
    elif nitrogen_value > 160 and nitrogen_value <= 180:
        return 8
   
    elif nitrogen_value > 180 and nitrogen_value <= 200:
        return 9
    
    elif nitrogen_value > 200 and nitrogen_value <= 210:
        return 10
    elif nitrogen_value > 210 and nitrogen_value <= 220:
        return 11
    elif nitrogen_value > 220 and nitrogen_value <= 230:
        return 12
    elif nitrogen_value > 230 and nitrogen_value <= 240:
        return 13
    else:
        return 14
    
def classify_phosphorus(phosphorus_value):
    #very low = 0
    if phosphorus_value >= 0 and phosphorus_value <= 5:
        return 0
     # low = 1
    elif phosphorus_value > 5 and phosphorus_value <= 10:
        return 1
    #moderately low = 2
    elif phosphorus_value > 10 and phosphorus_value <= 15:
        return 2
    #slightly low = 3
    elif phosphorus_value > 15 and phosphorus_value <= 20:
        return 3
    #optimal = 4
    elif phosphorus_value > 25 and phosphorus_value <= 30:
        return 4
    #slightly high = 5
    elif phosphorus_value > 35 and phosphorus_value <= 40:
        return 5
    #moderately high =6
    elif phosphorus_value > 40 and phosphorus_value <= 60:
        return 6
    # high =7 
    elif phosphorus_value > 60 and phosphorus_value <= 80:
        return 7
    #very high = 8
    elif phosphorus_value > 80 and phosphorus_value <= 100:
        return 8
    #extremely high = 9
    elif phosphorus_value > 100 and phosphorus_value <= 120:
        return 9
    #toxic high = 10
    elif phosphorus_value > 120 and phosphorus_value <= 140:
        return 10
    elif phosphorus_value > 140 and phosphorus_value <= 160:
        return 11
    elif phosphorus_value > 160 and phosphorus_value <= 180:
        return 12
    elif phosphorus_value > 180 and phosphorus_value <= 200:
        return 13
    else:
        return 14
    
def classify_potassium(potassium_value):
   
    if potassium_value >= 0 and potassium_value <= 8:
        return 0
   
    elif potassium_value > 8 and potassium_value <= 16:
        return 1
   
    elif potassium_value > 16 and potassium_value <= 24:
        return 2
   
    elif potassium_value > 24 and potassium_value <= 32:
        return 3
   
    elif potassium_value >32 and potassium_value <= 40:
        return 4
   
    elif potassium_value > 48 and potassium_value <= 56:
        return 5
    
    elif potassium_value > 56 and potassium_value <= 64:
        return 6
    
    elif potassium_value > 64 and potassium_value <= 72:
        return 7
   
    elif potassium_value > 72 and potassium_value <=80 :
        return 8
   
    elif potassium_value > 80 and potassium_value <= 88:
        return 9
    
    elif potassium_value > 88 and potassium_value <= 96:
        return 10
    elif potassium_value > 96 and potassium_value <= 140:
        return 11
    elif potassium_value > 140 and potassium_value <= 190:
        return 12
    elif potassium_value > 190 and potassium_value <= 255:
        return 13
    else:
        return 14
    
def classify_temperature(temp_value):
    #very low = 0
    if temp_value >= 0 and temp_value <= 10:
        return 0
     # low = 1
    elif temp_value > 10 and temp_value <= 20:
        return 1
    #moderately low = 2
    elif temp_value > 20 and temp_value <=30:
        return 2
    #slightly low = 3
    elif temp_value >30 and temp_value <= 40:
        return 3
    #optimal = 4
    elif temp_value > 40 and temp_value <= 50:
        return 4
    #slightly high = 5
    elif temp_value > 50 and temp_value <= 60:
        return 5
    #moderately high =6
    else:
        return 6
    
def classify_humidity(hum_val):
    #very low = 0
    if hum_val >= 0 and hum_val <= 20:
        return 0
     # low = 1
    elif hum_val > 20 and hum_val <= 40:
        return 1
    #moderately low = 2
    elif hum_val > 40 and hum_val <=60:
        return 2
    #slightly low = 3
    elif hum_val >60 and hum_val <= 80:
        return 3
    #optimal = 4
    elif hum_val > 80 and hum_val <= 80:
        return 4
    #slightly high = 5
    elif hum_val > 80 and hum_val <= 100:
        return 5
    #moderately high =6
    else:
        return 6
    
def estimate_rain_intensity(temperature, humidity):
    # Define temperature and humidity thresholds
    temp_threshold = 30 
    humidity_threshold = 40

    # If both temperature and humidity exceed their respective thresholds, assume higher probability of rain
    if temperature < temp_threshold and humidity > humidity_threshold:
        #"Very low"
        return 0
    elif temperature < temp_threshold and humidity <= humidity_threshold:
        #"low"
        return 1
    elif temperature >= temp_threshold and humidity > humidity_threshold:
        #"Medium"
        return 2
    elif temperature >= temp_threshold and humidity <= humidity_threshold:
        #"high"
        return 3
    else:
        #very high
        return 4

def load_npkw_ids():

    # Define the environment variable names and their corresponding IDs
    env_variable_ids = {
        "NEEDED_NITROGEN_ID": None,
        "NEEDED_PHOSPHORUS_ID": None,
        "NEEDED_POTASSIUM_ID": None,
        "NEEDED_WATER_ID": None,
    }

    # Iterate over the environment variable names and get their values
    for env_variable, id_name in env_variable_ids.items():
        if env_variable in os.environ:
            env_variable_ids[env_variable] = os.environ[env_variable]

    # Extract the IDs from the dictionary and put them into an array
    ids = list(env_variable_ids.values())
    return ids
