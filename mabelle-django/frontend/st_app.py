import streamlit as st
import pandas as pd
import plost
from utils import *
from datetime import datetime
from django.templatetags.static import static

data = {
    'NPK': ['N', 'P', 'K'],
    'Reading': [1, 2, 3]
}
df = pd.DataFrame(data)

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Agriculture Dashboard')

st.sidebar.subheader('Planting Parameters')
seed_user_input = st.sidebar.number_input('Enter number of seeds', min_value=0)
distance_user_input = st.sidebar.number_input('Enter the distance:', min_value=0)
selected_date = st.sidebar.date_input("Select Date", datetime.now())
selected_time = st.sidebar.time_input("Select Time", datetime.now().time())
st.sidebar.write("Selected Date:", selected_date)
st.sidebar.write("Selected Time:", selected_time)

st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by LAU Students
---
''')


# Row A
st.markdown('### Metrics')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Temperature", "26 °C", "1.2 °C")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")


# Row B
seattle_weather = pd.read_csv('../static/data/seattle-weather.csv', parse_dates=['date'])

c1, c2, c3 = st.columns((6,1,3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color=time_hist_color,
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
with c3:
    st.markdown('### NPK chart')
    plost.donut_chart(
        data=df,
        theta='Reading',
        color='NPK',
        legend='hi', 
        use_container_width=True)

# Row C
st.markdown('### Temperature and Humidity')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)