import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from src.pipeline.predict_pipeline import PredictPipeline
from src.pipeline.recommend_pipeline import RecommendationPipeline



def get_user_data():
    df = pd.read_csv("artifacts/data.csv")
    # Create input fields for user to enter features
    st.subheader("Choose Your Preference:")

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
        st.subheader("")
        
        # Show similar properties
        recommendation_system(user_query_df)

def recommendation_system(user_query_df):
    st.subheader("Recommendations based on your search:")
    rp = RecommendationPipeline()
    cos_similar, knn_similar = rp.get_similar_records(user_query_df, n_recommendations=3)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Cosine Similar Properties:")
        st.subheader("")
        for i, row in cos_similar.iterrows():
            st.markdown(f"**{row['society']}**")
            st.markdown(f"{row['bedroom']} BHK having {row['area_sqm']} sq.m area in")
            st.markdown(f"{row['sector']}, Gurgaon")
            st.subheader("")
    with col2:
        st.subheader("KNN Similar Properties:")
        st.subheader("")
        for i, row in knn_similar.iterrows():
            st.markdown(f"**{row['society']}**")
            st.markdown(f"{row['bedroom']} BHK having {row['area_sqm']} sq.m area in")
            st.markdown(f"{row['sector']}, Gurgaon")
            st.subheader("")


def data_analysis():
    st.header('Gurgaon Real Estate Analytics')
    df = pd.read_csv("artifacts/data.csv")
    df = df[df['bedroom'] <= 7] # Filter out properties with more than 7 bedrooms for better visualization
    st.subheader("Sample of the Dataset:")
    st.dataframe(df.sample(5, random_state=42), hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Price vs Area")
        fig = px.scatter(df, x='area_sqm', y='price_cr', color='bedroom',
                         hover_data=['society', 'sector'], 
                         color_continuous_scale=px.colors.sequential.Magenta, 
                         range_color=[1, 7])
        st.plotly_chart(fig)
        st.markdown("- Price generally increases with area, but there are some outliers. 6BHK properties seem to have a wide price range.")

        df_bedroom_count = df['bedroom'].value_counts().reset_index().sort_values(by='bedroom')
        st.subheader("Proportion of Bedrooms")
        fig = px.pie(df_bedroom_count, names='bedroom', values='count',
                     category_orders={'bedroom': [7,6,5,4,3,2,1]},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(rotation=90, direction='clockwise')
        st.plotly_chart(fig)
        st.markdown("- Most properties in Gurgaon are 3BHK followed by 2BHK and 4BHK.")

        st.subheader("5 Most Expensive Societies & Average Price")
        df_top_societies = df.groupby('society')['price_cr'].mean().sort_values(ascending=True).tail(5).reset_index()
        fig = px.bar(df_top_societies, x='price_cr', y='society', color_discrete_sequence=px.colors.qualitative.Pastel1)
        st.plotly_chart(fig)
        st.markdown("- The most expensive societies in Gurgaon have an average price above INR 10 crore.")

        st.subheader("Number of properties with different nearby landmarks")
        nearby_landmarks = ['has_market', 'has_mall', 'has_park', 'has_institute', 'has_metro_stn', 'has_airport', 'has_bank_or_atm', 'has_hospital_or_clinic']
        df_landmark_count = df[nearby_landmarks].sum().reset_index().rename(columns={'index': 'landmark', 0: 'count'}).sort_values(by='count', ascending=False)
        df_landmark_count['landmark'] = df_landmark_count['landmark'].str.replace('has_', '').str.replace('_', ' ')
        fig = px.funnel(df_landmark_count, x='count', y='landmark', 
                        color_discrete_sequence=px.colors.qualitative.Pastel2,
                        labels={'count': 'Number of Properties', 'landmark': 'Nearby Landmarks'})
        st.plotly_chart(fig)
        st.markdown("- Maximum number of properties in Gurgaon are near a hospital or clinic, followed by an Institute and airport.")
        
        df_sector_count = df['sector'].value_counts().reset_index().sort_values(by='count', ascending=False).head(5)
        st.subheader("Top 5 Sectors with maximum number of properties")
        fig = px.bar(df_sector_count, x='sector', y='count', 
                     color_discrete_sequence=px.colors.qualitative.Pastel, 
                     labels={'count': 'Number of Properties', 'sector': 'Sectors'})
        st.plotly_chart(fig)
        a = str(df_sector_count.iloc[0]['sector']).replace("sector ", "").strip()
        b = str(df_sector_count.iloc[1]['sector']).replace("sector ", "").strip()
        c = str(df_sector_count.iloc[2]['sector']).replace("sector ", "").strip()
        d = str(df_sector_count.iloc[3]['sector']).replace("sector ", "").strip()
        e = str(df_sector_count.iloc[4]['sector']).replace("sector ", "").strip()
        st.markdown(f"- Sectors {a}, {b}, {c}, {d} and {e} have the maximum number of properties in Gurgaon.")

        st.subheader("Log Price vs No. of Bedrooms")
        fig = px.box(df, x='bedroom', y='price_cr', log_y=True, color_discrete_sequence=px.colors.qualitative.Pastel2)
        st.plotly_chart(fig)
        st.markdown("- 6BHK seem cheaper than 5BHK on average.")

        st.subheader("Distribution of Price")
        fig, ax = plt.subplots()
        sns.histplot(df['price_cr'], bins=150, kde=True, ax=ax)
        st.pyplot(fig)
        st.markdown("- Maximum number of properties are priced between INR 1 crore and INR 3 crore.")

        st.subheader("Proportion of Floor Rise")
        df_floor_rise_count = df['floor_rise'].value_counts().reset_index()
        fig = px.pie(df_floor_rise_count, values='count', names='floor_rise', hole=0.6, 
                     color_discrete_sequence=px.colors.qualitative.Pastel1,
                     labels={'low': 'low rise', 'mid': 'mid rise', 'high': 'high rise'})
        fig.update_traces(rotation=90, direction='counterclockwise')
        st.plotly_chart(fig)
        st.markdown(f"- Approximately 50% of the flats in Gurgaon are in high rise buildings.")

        st.subheader("Treemap of Average Price by Sector and Society")
        fig = px.treemap(df, path=['sector', 'society'], values='price_cr', 
                         color_continuous_scale=px.colors.sequential.Plasma,
                         height=900, width=600)
        st.plotly_chart(fig)
        st.markdown("- The treemap shows the distribution of property prices across different sectors and societies in Gurgaon. Larger rectangles represent higher average prices, while smaller rectangles indicate lower average prices. This visualization helps identify which sectors and societies have more expensive properties.")














def main():
    st.set_page_config(layout='wide',page_title='Real Estate Project',page_icon='🏠')
    st.title('Real Estate - Machine Learning Project')
    st.sidebar.title('Gurgaon City')
    option = st.sidebar.pills("Select One:", ['Property Price Prediction', 'Gurgaon Property Analytics'])

    if option == 'Property Price Prediction':
        price_prediction()
    elif option == 'Gurgaon Property Analytics':
        data_analysis()





if __name__ == '__main__':
    main()