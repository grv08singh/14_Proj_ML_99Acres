import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline

def prediction_query():
    # Create input fields for user to enter features
    st.subheader("Choose your preferences for the property:")
    all_sectors = [1, 2, 3, 4, 5, 7, 9, 10, 12, 14, 15, 21, 22, 23, 24, 28, 30
                   , 31, 33, 36, 37, 38, 39, 40, 41, 43, 45, 47, 48, 49, 50, 51
                   , 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65, 66, 67
                   , 68, 69, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 82, 83
                   , 84, 85, 86, 88, 89, 90, 91, 92, 93, 95, 99, 102, 103, 104
                   , 105, 106, 107, 108, 109, 110, 111, 112, 113]


    col1,col2,col3,col4 = st.columns(4)
    with col1:
        bhk = st.selectbox("Bedroom", options=list(range(1, 11)))
        sector = st.selectbox("Sector", options=all_sectors)
    with col2:
        floor_rise = st.selectbox("Floor Rise", ["Low", "Mid", "High"])
        age = st.selectbox("Property Age", ["New", "Mid-Aged", "Old", "Under Construction"])


    st.subheader("Nearby Landmarks:")
    col5,col6,col7,col8,col9 = st.columns(5)
    with col5:
        has_market = st.checkbox("Market")
        has_mall = st.checkbox("Mall")
        has_park = st.checkbox("Park")
        has_institute = st.checkbox("School or College")
    with col6:
        has_metro_stn = st.checkbox("Metro Station")
        has_airport = st.checkbox("Airport")
        has_bank_or_atm = st.checkbox("Bank or ATM")
        has_hospital_or_clinic = st.checkbox("Hospital")

    query_dict = {
        "bhk": bhk,
        "sector": sector,
        "floor_rise": floor_rise,
        "age": age,
        "has_hospital_or_clinic": has_hospital_or_clinic,
        "has_mall": has_mall,
        "has_market": has_market,
        "has_park": has_park,
        "has_bank_or_atm": has_bank_or_atm,
        "has_institute": has_institute,
        "has_airport": has_airport,
        "has_metro_stn": has_metro_stn
    }
    return query_dict

def price_prediction():
    st.header('Gurgaon Real Estate Price Prediction')
    pred_query_dict = prediction_query()
    pred_query_df = pd.DataFrame([pred_query_dict])

    if st.button("Predict Price"):
        pp=PredictPipeline()
        pred=pp.predict(pred_query_df)
        st.write(f"Predicted Price: INR {pred[0]} crore")

    st.write("Recommendations based on your input:")
    recommendation_system(pred_query_df)

def recommendation_system(pred_query_df):
    # Implement recommendation logic here
    pass

def overall_analysis():
    st.title('Gurgaon Real Estate Analytics')
    pass

def main():
    st.set_page_config(layout='wide',page_title='Real Estate Project',page_icon='🏠')
    st.title('Real Estate - Machine Learning Project')
    st.sidebar.title('Gurgaon City')
    option = st.sidebar.radio("Select One:", ['Price Prediction', 'Recommendation System', 'Analytics'])

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