import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime


def plot_price_evolution_by_origin_streamlit(df, title):

    st.title("Price Evolution by Origin")
    # Get all unique origin
    origins = df['origin'].unique()
    destinations = df['destination'].unique()

    # Use multiselect to allow the user to select multiple origins and destinations
    selected_origins = st.multiselect("Select Origins", origins, ["BCN", "MAD"])
    selected_destinations = st.selectbox("Select Destinations", destinations)


    # Filter the DataFrame to only include rows with the selected origins and destinations
    df_filtered = df[df['origin'].isin(selected_origins) & (df['destination'] == selected_destinations)]
    df_filtered['searchDay'] = df_filtered['searchDay'].dt.strftime('%d-%m-%Y')
    df_filtered_today = df[df['origin'].isin(selected_origins) & (df['destination'] == selected_destinations) & (df['searchDay'] == datetime.today().strftime("%d-%m-%Y"))]

    st.write("Today's price:")
    st.write(df_filtered_today)

    # Create an interactive line plot of the 'price' column against the 'searchDay' column
    fig = px.line(df_filtered, x='searchDay', y='price', color='origin', labels={'value': 'Price', 'variable': 'searchDay'}, title=title)
    st.plotly_chart(fig)


if __name__ == '__main__':
    flights = pd.read_csv('itineraries.csv')

    flights['date'] = pd.to_datetime(flights['date'], format="%d-%m-%Y")
    flights['searchDay'] = pd.to_datetime(flights['searchDay'], format="%d-%m-%Y")

    st.write("Price Evolution by Origin and Destination")
    plot_price_evolution_by_origin_streamlit(flights, 'Price Evolution go flight')
