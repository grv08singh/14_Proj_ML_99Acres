import streamlit as st
import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import PredictPipeline
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def get_user_data():
    df = pd.read_csv("artifacts/data.csv")
    # Create input fields for user to enter features
    st.subheader("Property Preference:")

    col1,col2,col3 = st.columns(3)
    with col1:
        #Input 1: bedroom
        bedroom = st.selectbox("Bedroom", options=list(range(1, 7)))
        #Input 2: sector
        sector = st.selectbox("Sector", options=df[df['bedroom']==bedroom]['sector'].unique())
        #Input 3: area_sqm
        min_area = df[(df['bedroom']==bedroom) & (df['sector']==sector)]['area_sqm'].min()
        max_area = df[(df['bedroom']==bedroom) & (df['sector']==sector)]['area_sqm'].max()
        area_sqm = st.number_input(f"Area in sq.m.  [between {min_area} and {max_area}])", min_value=min_area, max_value=max_area, value=(min_area+max_area)/2)
        #Input 4: society
        society = st.selectbox("Society", options=df[(df['bedroom']==bedroom) & (df['sector']==sector)]['society'].unique())
        #Input 5: floor rise
        floor_rise = st.pills("Floor Rise", df[df['society']==society]['floor_rise'].unique())
        #Input 6: age of the property
        age = st.pills("Property Age", df[df['society']==society]['age'].unique())


        st.subheader("Nearby Landmarks:")
        col5,col6 = st.columns(2)
        with col5:
            has_market = int(st.checkbox("Market"))
            has_mall = int(st.checkbox("Mall"))
            has_park = int(st.checkbox("Park"))
            has_institute = int(st.checkbox("School or College"))
        with col6:
            has_metro_stn = int(st.checkbox("Metro Station"))
            has_airport = int(st.checkbox("Airport"))
            has_bank_or_atm = int(st.checkbox("Bank or ATM"))
            has_hospital_or_clinic = int(st.checkbox("Hospital"))

    query_dict = {
        "bedroom": bedroom,
        "sector": sector,
        "area_sqm": area_sqm,
        "society": society,
        "floor_rise": floor_rise,
        "age": age,
        "has_market": has_market,
        "has_mall": has_mall,
        "has_park": has_park,
        "has_institute": has_institute,
        "has_metro_stn": has_metro_stn,
        "has_airport": has_airport,
        "has_bank_or_atm": has_bank_or_atm,
        "has_hospital_or_clinic": has_hospital_or_clinic,
        #Feature values not set from the front end.
        "bathroom": bedroom,
        "balcony": df[(df['society']==society) & (df['bedroom']==bedroom)]['balcony'].mode()[0],
        "addl_room": df[(df['society']==society) & (df['bedroom']==bedroom)]['addl_room'].mode()[0],
        "landmark_count": int(df[(df['society']==society)]['landmark_count'].median()),
        "has_police_stn": 0,
        "has_fire_stn": 0,
        "has_rly_stn": 0,
        "has_expy": 0,
        "has_petrol_pump": 0,
        "has_hotel": 0,
        "has_temple_or_church": 0,
        "has_famous_chowk": 0,
        "has_club": 0,
        "has_stadium": 0,
        "has_restro_cafe": 0,
        "area_type": df[(df['society']==society) & (df['bedroom']==bedroom)]['area_type'].mode()[0],
        "city": 'gurgaon'
    }
    return query_dict

def price_prediction():
    st.header('Gurgaon Real Estate Price Prediction')
    user_query_dict = get_user_data()
    user_query_df = pd.DataFrame([user_query_dict])

    if st.button("Predict Price"):
        pp=PredictPipeline()
        price_lower, price_upper = pp.predict(user_query_df)
        st.subheader(f"Predicted Price:  INR {round(float(price_lower), 2)} - {round(float(price_upper), 2)} crore")
        
        # Show similar properties
        recommend_more(user_query_df)

def recommend_more(user_query_df):
    
    st.subheader("Similar Properties:")
    for i, idx in enumerate(indices[0]):
        prop = df.iloc[idx]
        st.write(f"**{i+1}. {prop['society']}** - {prop['sector']}")
        st.write(f"   {int(prop['bedroom'])} BHK, {prop['area_sqm']:.0f} sqm, ₹{prop['price_cr']:.2f} Cr")
        st.write("")






def overall_analysis():
    st.title('Gurgaon Real Estate Analytics')
    pass

def main():
    st.set_page_config(layout='wide',page_title='Real Estate Project',page_icon='🏠')
    st.title('Real Estate - Machine Learning Project')
    st.sidebar.title('Gurgaon City')
    option = st.sidebar.segmented_control("Select One:", ['Price Prediction', 'Recommendation System', 'Analytics'])

    if option == 'Price Prediction':
        price_prediction()
    elif option == 'Recommendation System':
        st.title('Gurgaon Real Estate Recommendation System')
        recommendation_system()
    elif option == 'Analytics':
        st.title('Gurgaon Real Estate Analytics')
        overall_analysis()





if __name__ == '__main__':
    main()