import matplotlib.pyplot as plt
import numpy as np
from constants import *
import streamlit as st
import pandas as pd

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