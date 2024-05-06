import streamlit as st
import pandas as pd
import plost
from django.templatetags.static import static
from utils import *
import sqlite3

access_token = get_access_token()
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Flag to start the motors
motors_on = False

# Init DB Connection
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()


with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
with st.sidebar: 
    st.markdown('''
    ---
    # Mabelle™ 🌺  
    ---
    ''')    
    st.header('Agriculture Dashboard')
    with st.form("my_form"):
        st.subheader('Planting Parameters')
        seed_user_input = st.number_input('Enter number of seeds', min_value=0)
        distance_user_input = st.number_input('Enter the distance:', min_value=0)

        submitted = st.form_submit_button("Submit")
        if submitted:
            motors_on = True
            st.write("### Form submitted!")
            st.write("Seed input:", seed_user_input)
            st.write("Selected distance:", distance_user_input)

            # Send dashboard info to Arduino Cloud IOT
            ids = load_dashboard_ids()
            to_return = [motors_on, seed_user_input, distance_user_input]

            for i in range(len(ids)):
                post_data(access_token, ids[i], to_return[i])


    st.subheader('Heat map parameter')
    npk_color = st.selectbox('Select Data', ('Nitrogen', 'Phosphorus', 'Potassium')) 

    st.subheader('Line chart parameters')
    plot_data = st.multiselect('Select Data', ['Temperature', 'Humidity'], ['Temperature', 'Humidity'])
    plot_height = st.slider('Specify plot height', 200, 500, 350) 

# Execute SQL queries
c.execute('SELECT * FROM core_reading ORDER BY timestamp DESC LIMIT 1;')
db_data = c.fetchall()

c.execute('SELECT temperature, humidity FROM core_reading;')
t_h_data = c.fetchall()

c.execute('SELECT timestamp, nitrogen_level, phosphorus_level, potassium_level FROM core_reading;')
npk_data = c.fetchall()


# Row A
st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", f"{db_data[0][5]}°C", "1.2 °C")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", f"{db_data[0][6]}%", "4%")


# Row B
# seattle_weather = pd.read_csv('../static/data/seattle-weather.csv', parse_dates=['date'])

c1, c2, c3 = st.columns((6,1,3))
with c1:
    npk_df = pd.DataFrame(npk_data, columns=['timestamp', 'Nitrogen', 'Phosphorus', 'Potassium'], index=range(len(npk_data)))
    npk_df['Reading'] = npk_df.index
    st.markdown('### NPK Distribution')
    plost.time_hist(
        data=npk_df,
        date='timestamp',
        x_unit='week',
        y_unit='day',
        color={
            "field": npk_color,
            "type": "nominal",
            "scale": {"scheme": "greens"}
        },
        aggregate='median',
        legend=None,
        height=345,
        use_container_width=True
    )
with c3:
    data = {
        'NPK': ['N', 'P', 'K'],
        'Reading': [db_data[0][2], db_data[0][3], db_data[0][4]]
    }
    df = pd.DataFrame(data)
    st.markdown('### NPK Latest reading')
    plost.donut_chart(
        data=df,
        theta='Reading',
        color= {
            "field": "NPK",
            "type": "nominal",
            "scale": {"scheme": "greens"}
        },
        legend='hi, this is an easter egg', 
        use_container_width=True
    )

# Row C
st.markdown('### Temperature and Humidity')
t_h_df = pd.DataFrame(t_h_data, columns=['Temperature', 'Humidity'], index=range(len(t_h_data)))
t_h_df['Reading'] = t_h_df.index
color_cond = None if len(plot_data) == 0 else '#4D772E' if len(plot_data) != 2 else ['#A9A9A9', '#4D772E']
st.line_chart(t_h_df, x = 'Reading', y = plot_data, height = plot_height, color=color_cond)