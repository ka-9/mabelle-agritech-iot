import streamlit as st
import pandas as pd
import plost
from django.templatetags.static import static
from utils import *

access_token = get_access_token()

data = {
    'NPK': ['N', 'P', 'K'],
    'Reading': [1, 2, 3]
}
df = pd.DataFrame(data)

# Flag to start the motors
motors_on = False

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    

with st.sidebar:
    with st.form("my_form"):
        st.header('Agriculture Dashboard')
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
    time_hist_color = st.selectbox('Color by', ('temp_min', 'temp_max')) 

    st.subheader('Line chart parameters')
    plot_data = st.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
    plot_height = st.slider('Specify plot height', 200, 500, 250) 

st.sidebar.markdown('''
---
Mabelle™ 🌺
---
''')


# Row A
st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", "26 °C", "1.2 °C")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")


# Row B
seattle_weather = pd.read_csv('../static/data/seattle-weather.csv', parse_dates=['date'])

c1, c2, c3 = st.columns((6,1,3))
with c1:
    st.markdown('### NPK Distribution')
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
    st.markdown('### NPK Latest reading')
    plost.donut_chart(
        data=df,
        theta='Reading',
        color='NPK',
        legend='hi', 
        use_container_width=True)

# Row C
st.markdown('### Temperature and Humidity')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)