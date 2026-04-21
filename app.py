import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline

def prediction_query():
    # Create input fields for user to enter features
    area_sqm = st.number_input("Area (in sqm)", min_value=0.0)
    bhk = st.number_input("BHK", min_value=0, step=1)
    bathroom = st.number_input("Bathroom", min_value=0, step=1)
    balcony = st.number_input("Balcony", min_value=0, step=1)
    addl_room = st.number_input("Additional Room", min_value=0, step=1)
    sector = st.number_input("Sector", min_value=0, step=1)
    landmark_count = st.number_input("Landmark Count", min_value=0, step=1)
    has_hospital_or_clinic = st.checkbox("Has Hospital or Clinic")
    has_police_stn = st.checkbox("Has Police Station")
    has_fire_stn = st.checkbox("Has Fire Station")
    has_mall = st.checkbox("Has Mall")
    has_market = st.checkbox("Has Market")
    has_park = st.checkbox("Has Park")
    has_bank_or_atm = st.checkbox("Has Bank or ATM")
    has_institute = st.checkbox("Has Institute")
    has_airport = st.checkbox("Has Airport")
    has_rly_stn = st.checkbox("Has Railway Station")
    has_metro_stn = st.checkbox("Has Metro Station")
    has_expy = st.checkbox("Has Expressway")
    has_petrol_pump = st.checkbox("Has Petrol Pump")
    has_hotel = st.checkbox("Has Hotel")
    has_temple_or_church = st.checkbox("Has Temple or Church")
    has_famous_chowk = st.checkbox("Has Famous Chowk")
    has_club = st.checkbox("Has Club")
    has_stadium = st.checkbox("Has Stadium")
    has_restro_cafe = st.checkbox("Has Restaurant or Cafe")
    area_type = st.selectbox("Area Type", ["Type 1", "Type 2", "Type 3"])
    floor_rise = st.selectbox("Floor Rise", ["Low", "Medium", "High"])
    age = st.selectbox("Age of Property", ["New", "Old"])
    society = st.text_input("Society Name")
    city = st.text_input("City Name")

    query_dict = {
        "area_sqm": area_sqm,
        "bhk": bhk,
        "bathroom": bathroom,
        "balcony": balcony,
        "addl_room": addl_room,
        "sector": sector,
        "landmark_count": landmark_count,
        "has_hospital_or_clinic": has_hospital_or_clinic,
        "has_police_stn": has_police_stn,
        "has_fire_stn": has_fire_stn,
        "has_mall": has_mall,
        "has_market": has_market,
        "has_park": has_park,
        "has_bank_or_atm": has_bank_or_atm,
        "has_institute": has_institute,
        "has_airport": has_airport,
        "has_rly_stn": has_rly_stn,
        "has_metro_stn": has_metro_stn,
        "has_expy": has_expy,
        "has_petrol_pump": has_petrol_pump,
        "has_hotel": has_hotel,
        "has_temple_or_church": has_temple_or_church,
        "has_famous_chowk": has_famous_chowk,
        "has_club": has_club,
        "has_stadium": has_stadium,
        "has_restro_cafe": has_restro_cafe,
        "area_type": area_type,
        "floor_rise": floor_rise,
        "age": age,
        "society": society,
        "city": city
    }
    return query_dict

def price_prediction():
    st.title('Gurgaon Real Estate Price Prediction')
    pred_query_dict = prediction_query()
    pred_query_df = pd.DataFrame([pred_query_dict])

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
    st.title('Gurgaon Real Estate Project')
    st.sidebar.title('Gurgaon Real Estate Project')
    option = st.sidebar.selectbox('Select One',['Price Prediction','Recommendation System','Analytics'])
    st.title('Gurgaon Real Estate Project')

    if option == 'Price Prediction':
        st.title('Gurgaon Real Estate Price Prediction')
        price_prediction()
    elif option == 'Recommendation System':
        st.title('Gurgaon Real Estate Recommendation System')
        recommendation_system()
    elif option == 'Analytics':
        st.title('Gurgaon Real Estate Analytics')
        overall_analysis()

















if __name__ == '__main__':
    main()









        data = CustomData(
            area_sqm = float(request.form.get('area_sqm')),
            bhk = int(request.form.get('bhk')),
            bathroom = int(request.form.get('bathroom')),
            balcony = int(request.form.get('balcony')),
            addl_room = int(request.form.get('addl_room')),
            sector = int(request.form.get('sector')),
            landmark_count = int(request.form.get('landmark_count')),
            has_hospital_or_clinic = bool(request.form.get('has_hospital_or_clinic')),
            has_police_stn = bool(request.form.get('has_police_stn')),
            has_fire_stn = bool(request.form.get('has_fire_stn')),
            has_mall = bool(request.form.get('has_mall')),
            has_market = bool(request.form.get('has_market')),
            has_park = bool(request.form.get('has_park')),
            has_bank_or_atm = bool(request.form.get('has_bank_or_atm')),
            has_institute = bool(request.form.get('has_institute')),
            has_airport = bool(request.form.get('has_airport')),
            has_rly_stn = bool(request.form.get('has_rly_stn')),
            has_metro_stn = bool(request.form.get('has_metro_stn')),
            has_expy = bool(request.form.get('has_expy')),
            has_petrol_pump = bool(request.form.get('has_petrol_pump')),
            has_hotel = bool(request.form.get('has_hotel')),
            has_temple_or_church = bool(request.form.get('has_temple_or_church')),
            has_famous_chowk = bool(request.form.get('has_famous_chowk')),
            has_club = bool(request.form.get('has_club')),
            has_stadium = bool(request.form.get('has_stadium')),
            has_restro_cafe = bool(request.form.get('has_restro_cafe')),
            area_type = request.form.get('area_type'),
            floor_rise = request.form.get('floor_rise'),
            age = request.form.get('age'),
            society = request.form.get('society'),
            city = request.form.get('city')
        )

        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template("home.html", results=results[0])