import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from constants import BLUE_COLOR, GREY_COLOR
from constants import DARK_GREEN, REG_GREEN, LIGHT_GREEN, BLUE_COLOR, GREY_COLOR, WATER_CONTAINER_VOLUME, MAX_FERTILIZER, LIGHT_GREY


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

    fig, ax = plt.subplots(figsize=(10, 1))

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


def start_action():
    st.session_state.start_clicked = True


# Main function to display the dashboard
def main():
    st.title('Dashboard For Monitoring The Agriculture Robot')
    
    st.caption('This dashboard displays the data collected by the NPK sensor, the humidity and Temperature sensor, and weather predictions and the needed amounts of fertilizer and water')

   
    
   

    
    if 'start_clicked' not in st.session_state:
        st.session_state.start_clicked = False
    # User input for integer value

    st.markdown(
        """
        <style>
        .st-emotion-cache-kskxxl {
            width: 80% !important;
            margin-bottom: 5%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    forecast_list = generate_prediction()
    forecast_list = calc_delta(forecast_list)
    col1, col2, col3 = st.columns(3)
    icon1 = "🌡"
    icon2 = "🌢"

   
    
    with col1:
        st.markdown(
        """
        <style>
        .st-emotion-cache-j5r0tf {
            border: 1px solid black !important;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin:-5px;
            padding-bottom: 20px;

        }
        </style>
        """,
        unsafe_allow_html=True
    )
        
      
        st.subheader(f"{icon1} Temperature Forecast ")
        
        columns = st.columns(5)  # Create 5 columns

        # Generate metrics in the columns
        for i, column in enumerate(columns, 0):
          with column:
            if i == 2:
                st.metric(label='Current', value=forecast_list[i]['temp'], delta=forecast_list[i]['delta_temp'])
               
            else:
             column.metric(label=forecast_list[i]['time'], value=forecast_list[i]['temp'], delta=forecast_list[i]['delta_temp'])
                
        st.write(' ')
       
        st.subheader(f"{icon2} Humidity Forecast ")
        hum_columns = st.columns(len(forecast_list))

        # Display humidity metrics
        for i, column in enumerate(hum_columns):
            with column:
                if i==2:
                    st.metric(label='Current', value=forecast_list[i]['hum'], delta=forecast_list[i]['delta_hum'])
                else:
                    column.metric(label=forecast_list[i]['time'], value=forecast_list[i]['hum'], delta=forecast_list[i]['delta_hum'])
        
        st.write(' ')
        st.write(' ')
        st.subheader('Rain Forcast')
        icon3 ="🌦"
        col21,col22 = st.columns(2)
        with col21:
            st.write("<h1 style='font-size:100px; margin-left:20%' '>🌦</h1>", unsafe_allow_html=True)
        with col22:
            st.write("<h1 style='font-size:30px;margin-left:-40%'> 20% Rain </h1>", unsafe_allow_html=True)
            st.write("<h1 style='font-size:15px; margin-left:-30%; margin-top:-10%'>3% (night)</h1>", unsafe_allow_html=True)

           
  

        

   

    with col2:
        st.write(' ')
        st.write(' ')
        
        seed_user_input = st.number_input('Enter number of seeds', min_value=0)
        distance_user_input = st.number_input('Enter the distance:', min_value=0)
        selected_date = st.date_input("Select Date", datetime.now())
        selected_time = st.time_input("Select Time", datetime.now().time())
        st.write("Selected Date:", selected_date)
        st.write("Selected Time:", selected_time)
        if st.button('Start'):
            start_action()

        positions = [1.5, 3, 7.2, 5, 11]
        if st.session_state.start_clicked:
            st.subheader('Distance Line with Marks')
            distance_line_fig = generate_distance_line(distance_user_input, seed_user_input, positions)
            st.pyplot(distance_line_fig)

        values_dict = {
            "water": 0.4,
            "fertilizer": 5
        }

        water_fertilizer_percent = get_water_fertilizer_percentages(values_dict)
        # st.progress(water_fertilizer_percent["water_used_percentage"])
        # st.progress(water_fertilizer_percent["fertilizer_used_percentage"])
        st.write(' ')
        max_val =5  # Sample water value
        fertilizer_value = 0.2  # Sample fertilizer value
        st.markdown('Fertilizer To be added')
        create_fertilizer_bar_graph(fertilizer_value,max_val)
        st.write(' ')
        st.markdown('Water to be added')
        create_Water_bar_graph(0.3,4)
    
    with col3: 
        st.write(' ')
        st.write(' ')
        with col3:
            # Bar graph for temperature and humidity
            st.subheader('Bar Graph for Temperature and Humidity Monitored Each Meter')
            temp_humidity__fig = generate_temphumidity_barchart()
            st.pyplot(temp_humidity__fig)

            # if st.session_state.start_clicked:
            st.subheader('Current NPK Values')
            fig = generate_npk_piechart()
            st.pyplot(fig)

    
    #st-emotion-cache-1v0mbdj e115fcil1
    st.markdown(
        """
        <style>
        .st-emotion-cache-1v0mbdj { 
            max-width: 100px; padding: 5% 5% 
            }
        </style>
        """,
        unsafe_allow_html=True
    )

        
     
# Example with an icon next to a subheader
       


    st.markdown(
        """
        <style>
        .block-container { max-width: 100%; padding: 5% 5% }
        </style>
        """,
        unsafe_allow_html=True
    )



if __name__ == '__main__':
    main()




