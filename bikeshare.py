import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington) and handle invalid inputs
    while True:
        city = input('Enter the city name:').lower()
        if city in ['chicago', 'new york city', 'washington']: break
        else:
            print('It\'s a not a valid city. Please enter Chicago, New York or Washington')

    # Get user input for month (all, january, february, ... , june) and handle invalid inputs
    while True:
        month= input('Enter month (if you want to select all months, please enter \"all\"):').lower()
        if month in ['all','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']: break
        else:
            print('It\'s a not a valid month. Please enter a valid month or all')

    # Get user input for day of week (all, monday, tuesday, ... sunday) and handle invalid inputs
    while True:
        day= input('Enter day of week (if you want to select all days, please enter \"all\"):').lower()
        if day.title() in ['All','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]: break
        else:
            print('It\'s a not a valid month. Please enter a valid month or all')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # calculate travek time to create a new column
    df['travel_time_minutes'] = (df['End Time']-df['Start Time'])/np.timedelta64(1,'m')


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate the most common month
    popular_month = df['month'].value_counts().idxmax()

    # Calculate the most common day of week
    popular_weekday = df['day_of_week'].value_counts().idxmax()

    # Calculate the most common start hour
    popular_hour = df['hour'].value_counts().idxmax()

    # Print the results
    print('\nMost Common Month: {}\n'.format(popular_month))
    print('\nMost Common Day of Week: {}\n'.format(popular_weekday))
    print('\nMost Common Hour: {}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()

    # Display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()

    # Display most frequent station (combination of start station and end station trip)
    popular_station = df['Start Station'].append(df['End Station']).value_counts().idxmax()

   # Print the results
    print('\nMost Popular Start Station: {}\n'.format(popular_start_station))
    print('\nMost Popular End Station: {}\n'.format(popular_end_station))
    print('\nMost Popular Station: {}\n'.format(popular_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time
    total_travel_time = df['travel_time_minutes'].sum()

    # calculate mean travel time
    mean_travel_time = df['travel_time_minutes'].mean()

    # Print the results
    print('\nTotal Travel Time: {}\n'.format(total_travel_time))
    print('\nMean Travel Time: {}\n'.format(mean_travel_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
    except:
        gender = 'Data not available for this city'

    # Display earliest, most recent, and most common year of birth
    try:
        earlies_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].value_counts().idxmax())
        
    except:
        earlies_birth_year, recent_birth_year, common_birth_year = 'Data not available for this city', 'Data not available for this city', 'Data not available for this city'
        
    # Print the results
    print('\nCounts of user types: \n{}\n'.format(user_types))
    print('\nCounts of gender: \n{}\n'.format(gender))
    print('\nEarliest year of birth: {}\n'.format(earlies_birth_year))
    print('\nMost recent year of birth: {}\n'.format(recent_birth_year))
    print('\nMost common year of birth: {}\n'.format(common_birth_year))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        x = 0
        y = 1
        raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        while True:                     
            if raw_data.lower()== 'yes':
                print(df.iloc[5*x:5*y])
                x+=1
                y+=1
                more_raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')
                if more_raw_data.lower() == 'yes' and raw_data.lower()== 'yes':
                    print(df.iloc[5*x:5*y])
                    x+=1
                    y+=1
                else: break
       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
