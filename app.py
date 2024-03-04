import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.sidebar.header('Date and Time Range Filter')
start_date = st.sidebar.date_input('Start date', day_df['dteday'].min())
end_date = st.sidebar.date_input('End date', day_df['dteday'].max())

start_hour, end_hour = st.sidebar.select_slider(
    'Select hour range',
    options=list(range(24)),
    value=(0, 23)
)

filtered_day_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & (day_df['dteday'] <= pd.Timestamp(end_date))]
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & 
                           (hour_df['dteday'] <= pd.Timestamp(end_date)) &
                           (hour_df['hr'] >= start_hour) & 
                           (hour_df['hr'] <= end_hour)]

def plot_hourly_rentals(hour_df):
    hourly_rentals = hour_df.groupby(['workingday', 'hr'])['cnt'].mean().unstack(0)
    hourly_rentals.plot(kind='bar', figsize=(14, 8))
    plt.title('Weekday vs Weekend Average Bike Rental')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Number of Rentals')
    plt.legend(['Weekend', 'Weekday'], title='Day')
    st.pyplot(plt)

def plot_monthly_rentals(day_df):
    monthly_rentals = day_df.groupby(['yr', 'mnth'])['cnt'].mean().unstack(0)
    monthly_rentals.plot(kind='bar', figsize=(14, 8))
    plt.title('Average Bike Rental on Two Different Years')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Rentals')
    plt.xticks(ticks=range(0, 12), labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], rotation=45)
    plt.legend(['Year 0', 'Year 1'], title='Year')
    st.pyplot(plt)

def plot_user_type_rentals(day_df):
    user_type_rentals = day_df.groupby('mnth').agg({'casual': 'mean', 'registered': 'mean'})
    user_type_rentals.plot(kind='bar', figsize=(14, 8))
    plt.title('Casual vs Registered Average Bike Rental')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Rentals')
    plt.xticks(ticks=range(0, 12), labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], rotation=45)
    plt.legend(['Casual', 'Registered'], title='Type')
    st.pyplot(plt)

def main():
    st.title('Bike Rental Analysis Dashboard')

    st.header('Hourly Bike Rental Analysis')
    plot_hourly_rentals(filtered_hour_df)

    st.header('Monthly Bike Rental Analysis')
    plot_monthly_rentals(filtered_day_df)

    st.header('User Type Bike Rental Analysis')
    plot_user_type_rentals(filtered_day_df)

if __name__ == '__main__':
    main()

