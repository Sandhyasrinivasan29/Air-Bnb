# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open("ICN.png")
st.set_page_config(page_title= "Airbnb Data Visualization | By Jafar Hussain",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Jafar Hussain*!
                                        Data has been gathered from mongodb atlas"""}
                  )