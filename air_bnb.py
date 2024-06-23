# Importing Libraries
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image

# Set the layout for the Streamlit app
st.set_page_config(layout="wide")

# Display an image (Airbnb logo)
st.image(r"C:/Users/sandh/OneDrive/Desktop/Airbnb_Logo_Bélo.svg.png", width=200)

# Display the main title
st.markdown("<h1 style='display: flex; align-items: center; font-size: 27px; margin: 0;'>AIR BNB DATA VISUALIZATION </h1>", unsafe_allow_html=True)

# Sidebar menu for navigation
with st.sidebar:
    selected = option_menu(
        "Menu", ["Home", "Overview", "Explore Data"], 
        icons=["house", "bar-chart-line", "graph-up-arrow", "exclamation-circle"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF4B4B"},
            "nav-link-selected": {"background-color": "#FF4B4B"}
        }
    )

# Load the data
df_all = pd.read_csv("Air_bnb.csv") 

if selected == "Home":
    col1,col2=st.columns(2)
    with col1:
        st.write("Welcome to the Airbnb Data Visualization App!")
        st.write("Use the sidebar to navigate through the different sections.") 
        st.header("About Airbnb")
        st.write("")
        st.write('''***Airbnb is an online marketplace that connects people who want to rent out
                their property with people who are looking for accommodations,
                typically for short stays. Airbnb offers hosts a relatively easy way to
                earn some income from their property.Guests often find that Airbnb rentals
                are cheaper and homier than hotels.***''')
        st.write("")
        st.write('''***Airbnb Inc (Airbnb) operates an online platform for hospitality services.
                    The company provides a mobile application (app) that enables users to list,
                    discover, and book unique accommodations across the world.
                    The app allows hosts to list their properties for lease,
                    and enables guests to rent or lease on a short-term basis,
                    which includes vacation rentals, apartment rentals, homestays, castles,
                    tree houses and hotel rooms. The company has presence in China, India, Japan,
                    Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy,
                    Norway, Portugal, Russia, Spain, Sweden, the UK, and others.
                    Airbnb is headquartered in San Francisco, California, the US.***''')

    with col2:
    
        st.image(r"C:/Users/sandh/OneDrive/Desktop/gif_1.gif")
        st.image(r"C:/Users/sandh/OneDrive\Desktop/gif 1.gif")
    
    

# OVERVIEW PAGE
if selected == "Overview":
    tab1, tab2 = st.tabs(["📝 DATAFRAME", "🚀 INSIGHTS"])
    
    # RAW DATA TAB
    with tab1:
        st.write(df_all)
    
    with tab2:
        # Slider for choosing price range
        price_range = st.sidebar.slider("Choose price", df_all["Price"].min(), df_all["Price"].max(), (df_all["Price"].min(), df_all["Price"].max()))

        country = st.sidebar.multiselect("Select Country", sorted(df_all.Country.unique()))
        property = st.sidebar.multiselect("Select Property Type", sorted(df_all.Property_type.unique()))
        room = st.sidebar.multiselect("Select Room Type", sorted(df_all.Room_type.unique()))

        # Filter the DataFrame based on selected country, property type, room type, and price range
        filtered_df = df_all[
            (df_all['Country'].isin(country)) &
            (df_all['Property_type'].isin(property)) &
            (df_all['Room_type'].isin(room)) &
            (df_all['Price'].between(price_range[0], price_range[1]))
        ]

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            # Query to group by 'Property_type', find the number of rows in each group, reset index name to 'Listings', and sort by 'Listings'
            query1 = filtered_df.groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False).head(10)
            fig1 = px.bar(query1,
                          title='Top 10 Property Types',
                          x='Listings',
                          y='Property_type',
                          orientation='h',
                          color='Property_type',
                          color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig1, use_container_width=True)
            
            # TOP 10 HOSTS BAR CHART
            df2 = filtered_df.groupby(["host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False).head(10)
            fig2 = px.bar(df2,
                          title='Top 10 Hosts with Highest number of Listings',
                          x='Listings',
                          y='host_name',
                          orientation='h',
                          color='host_name',
                          color_continuous_scale=px.colors.sequential.Agsunset)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df3 = filtered_df.groupby(["Room_type"]).size().reset_index(name="Room Counts")
            fig3 = px.pie(df3,
                          title='Total Listings in each Room_types',
                          names='Room_type',
                          values='Room Counts',
                          color_discrete_sequence=px.colors.sequential.Rainbow,
                          width=500)
            fig3.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig3, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            df4 = filtered_df.groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'Total_Listings'})
            fig4 = px.choropleth(df4,
                                 title='Total Listings in each Country',
                                 locations='Country',
                                 locationmode='country names',
                                 color='Total_Listings',
                                 color_continuous_scale=px.colors.sequential.Rainbow, width=600)
            st.plotly_chart(fig4, use_container_width=True)

# Additional functionality for other menu items can be added here


if selected == "Explore Data":
    st.write("Explore the data using various interactive tools and charts.")
    
    tab1, tab2, tab3 = st.tabs(["**PRICE ANALYSIS**", "**AVAILABILITY ANALYSIS**", "**LOCATION ANALYSIS**"])
    
    with tab1:
        col1, col2,col3 = st.columns(3)
        
        with col1:
            country = st.selectbox("**Select Country**", df_all["Country"].unique())
    
            room_type = st.radio("**Select Room Type**", df_all["Room_type"].unique())
        
        # Filter data based on selected country and room type
            df1_filtered = df_all[(df_all["Country"] == country) & (df_all["Room_type"] == room_type)].copy()
        
        # Group by property type and calculate sum of relevant columns
            df_grouped1 = df1_filtered.groupby("Property_type")[["Price", "Reviews_count", "Review_scores"]].sum().reset_index()
        
        # Create a bar chart
            fig_1 = px.bar(
                df_grouped1, 
                x="Property_type", 
                y="Price", 
                hover_data=["Reviews_count", "Review_scores"], 
                color_discrete_sequence=px.colors.sequential.haline_r,
                width=500, 
                height=500
            )
            
            st.plotly_chart(fig_1)
    
        with col3:
           
            property_type=st.selectbox("**select Property Type**", df1_filtered["Property_type"].unique())
            df2_filtered = df1_filtered[(df1_filtered["Property_type"] == property_type)]
            df_grouped2 = df2_filtered.groupby("host_response_time")[["Price", "Beds"]].sum().reset_index()

           
            
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            fig_2=px.pie( df_grouped2,
                         values="Price",
                         names="host_response_time",
                         hover_data=["Beds"],
                         color_discrete_sequence=px.colors.sequential.Pinkyl_r,
                         width=450, 
                         height=500)
            st.plotly_chart(fig_2)
            
        with col1:
            host_response=st.radio("Select Response Time",(df2_filtered["host_response_time"].unique()))
            df3_filtered=df2_filtered[(df2_filtered["host_response_time"]==host_response)]
            df_grouped3=df3_filtered.groupby("Bed_type")[["Price","Minimum_nights","Maximum_nights"]].sum().reset_index()
       
            fig_3=px.bar( df_grouped3,
                         x="Bed_type",
                         y=["Minimum_nights","Maximum_nights"],
                         hover_data=["Price"],
                         color_discrete_sequence=px.colors.sequential.Rainbow,
                         width=450, 
                         height=500,
                         barmode='group')
            st.plotly_chart(fig_3)

        with col3:
            bed_type = st.radio("**Select Bed Type**", df_grouped3["Bed_type"].unique())
            df4_filtered = df3_filtered[df3_filtered["Bed_type"] == bed_type]
            df_grouped4 = df4_filtered[["Name","Price", "Beds", "Bedrooms", "Accommodates"]].reset_index(drop=True)

            fig_4=px.bar( df_grouped4,
                         x="Name",
                         y=["Beds", "Bedrooms", "Accommodates"],
                         hover_data="Price",
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         width=450, 
                         height=500,
                         barmode='group')
            st.plotly_chart(fig_4)
        
        df_grouped5 = df4_filtered[["Name","Price", "Beds", "Bedrooms", "Accommodates","Amenities"]].reset_index(drop=True)
        df_grouped5



    with tab2:
        col1, col2,col3 = st.columns(3)
        
        with col1:
            country = st.selectbox("**Select country**", df_all["Country"].unique())
        with col2:
            property_type = st.selectbox("**Select Property Type**", df_all["Property_type"].unique())
        
        df_filtered_av1 = df_all[(df_all["Country"] == country) & (df_all["Property_type"] == property_type)].copy()
        col1,col2=st.columns(2)
        with col1:
            fig_av1=px.sunburst(df_filtered_av1,path=["Room_type","Bed_type","Is_location_exact"],values="Availability_30",width=500,height=500,color_discrete_sequence=px.colors.sequential.Hot_r)
            st.plotly_chart(fig_av1)

            fig_av2=px.sunburst(df_filtered_av1,path=["Room_type","Bed_type","Is_location_exact"],values="Availability_60",width=500,height=500,color_discrete_sequence=px.colors.sequential.Hot_r)
            st.plotly_chart(fig_av2)
        with col2:

            fig_av3=px.sunburst(df_filtered_av1,path=["Room_type","Bed_type","Is_location_exact"],values="Availability_90",width=500,height=500,color_discrete_sequence=px.colors.sequential.Hot_r)
            st.plotly_chart(fig_av3)
  
            fig_av4=px.sunburst(df_filtered_av1,path=["Room_type","Bed_type","Is_location_exact"],values="Availability_365",width=500,height=500,color_discrete_sequence=px.colors.sequential.Hot_r)
            st.plotly_chart(fig_av4)

        with col1:
            roomtype_a= st.selectbox("Select the Room Type_a", df_filtered_av1["Room_type"].unique())

            df_filtered_av2= df_filtered_av1[df_filtered_av1["Room_type"] == roomtype_a]

            df_bar_ava= pd.DataFrame(df_filtered_av2.groupby("host_response_time")[["Availability_30","Availability_60","Availability_90","Availability_365","Price"]].sum())
            df_bar_ava.reset_index(inplace= True)

            fig_df_bar_ava = px.bar(df_bar_ava, x='host_response_time', y=['Availability_30', 'Availability_60', 'Availability_90', "Availability_365"], 
            title='AVAILABILITY BASED ON HOST RESPONSE TIME',hover_data="Price",
            barmode='group',color_discrete_sequence=px.colors.sequential.Rainbow_r,width=1000)

            st.plotly_chart(fig_df_bar_ava)

    with tab3:
            map_fig = px.scatter_mapbox(df_all, lat='Longitude', lon='Latitude', color='Price', size='Accommodates',
                                color_continuous_scale="spectral", hover_name='Name',
                                hover_data=["Property_type","Room_type","Beds","Cancellation_policy","Reviews_count"],
                                range_color=(0, 49000), mapbox_style="open-street-map", zoom=1)
            map_fig.update_layout(width=1150, height=800, title='Geospatial Distribution of Listings')

            st.plotly_chart(map_fig)


