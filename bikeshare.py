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
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Please enter a city to explore (Chicago, New York City, Washington): ")
        if city.lower() in ['chicago', 'new york city', 'washington']:
            print ("Thank you!\n")
            break
        else:
            print("\nSorry, your entry: \"{}\" is not a correct city choice. Please enter a displayed city.\n".format(city))

    while True:
        # get user input for month (all, january, february, ... , june)
        month = input("Please choose a month (All, January, February, ... , June): ")
        if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print ("Thank you!\n")
            break
        else:
            print("\nSorry, your entry: \"{}\" is not a correct month choice. Please enter \"All\" or a month in the displayed range.\n".format(month))

    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Please choose a day of the week to explore (All, Monday, Tuesday, ... Sunday): ")
        if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print ("Thank you!\n")
            break
        else:
            print("\nSorry, your entry: \"{}\" is not a correct day choice. Please enter \"All\" or a day of the week.\n".format(day))

    print('\nLoading data for your choices: city: {}, month: {}, day: {}!'.format(city, month, day))
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
    city = city.lower()
    month = month.lower()
    day = day.lower()

    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city])
    except OSError:
        print('cannot open: ', CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # find the most common hour (from 1 to 6)
    common_month = df['month'].mode()[0]

    # display the most common day of week
    # extract month from the Start Time column to create an month column
    df['week'] = df['Start Time'].dt.week
    # find the most common hour (from 1 to 26?)
    common_week = df['week'].mode()[0]


    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    common_hour = df['hour'].mode()[0]

    print('Most Common Month:', common_month)
    print('Most Common Week:', common_week)
    print('Most Common Start Hour:', common_hour)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

# Note: the following code for station stats was inspired from a discussion on our class forums and posted by Antonio F. and discussed with the mentors. I took notes and used the structures simliar to my above code (much of which was derived from the Project Practice examples).
    # display most commonly used start station
    common_start_station = df.mode()['Start Station'][0]
    print('The most commonly used start station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df.mode()['End Station'][0]
    print('The most commonly used end station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    most_requent_start_stop = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most commonly used station pair: ', most_requent_start_stop)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Total Travel Time:', total_travel_time)
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print("User Type Breakdown:")
    print(user_types)


    # Display counts of gender
    try:
        user_gender_count = df['Gender'].value_counts()
        print("\nUser Gender Breakdown:")
        print(user_gender_count)
    except:
        print("\nNo Gender data to share.")

    # Display earliest, most recent, and most common year of birth
    try:
        year_of_birth_min = df['Birth Year'].min()
        earliest_year_of_birth = int(year_of_birth_min)
        print("\nEarliest Year of Birth: ",earliest_year_of_birth)
        year_of_birth_max = df['Birth Year'].max()
        latest_year_of_birth = int(year_of_birth_max)
        print("Most Recent Year of Birth: ",latest_year_of_birth)
        year_of_birth_mode = df['Birth Year'].mode()
        most_common_year_of_birth = int(year_of_birth_mode)
        print("Most Common Year of Birth: ",most_common_year_of_birth)
    except:
        print("\nNo Birth Year data to share.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    while True:
        show_data = input('\nWould you like to see lines of raw data? Enter yes or no.\n')
        if show_data.lower() != 'yes':
            print ("Next you can resart to look at some more data!\n")
            break
        else:
            num_lines = input('\nHow many lines would you like? (enter a number): \n')
            print (df.iloc[0:int(num_lines)].to_json(orient='records', lines=True))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
