import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
  
    try:
        #creating possible input items lists
        av_cities= ['chicago','new york','washington'] 
        av_filters=['both','month', 'day','not at all']
        days=['all', 'monday', 'tuesday', 'wednesday', 'thursday','friday', 'saturday', 'sunday']
        months=['all', 'january', 'february', 'march', 'april', 'may', 'june']
        #taking appropriate input from the user
        city = input('Would you like to see data for Chicago, New York, or Washington? \n')
        while city.lower() not in av_cities:
            city = input('please enter one of these cities {Chicago, New York, or Washington} \n')  
        filter_selected = input('Would you like to filter the data by month, day, both or not at all? \n')
        while filter_selected.lower() not in av_filters:               
            filter_selected = input('Would you like to filter the data by month, day, both or not at all? \n')            
        if filter_selected.lower() == 'both':
            month= input('which month? all, January, February, March, April, May, or June? \n')
            while month.lower() not in months:
                month= input('which month? all, January, February, March, April, May, or June? \n')
            day= input('which day? all, Monday, Tuesday, Wednesday, Thursday,Friday, Saturday, Sunday? \n')
            while day.lower() not in days:
                day= input('which day? all, Monday, Tuesday, Wednesday, Thursday,Friday, Saturday, Sunday? \n')
        elif filter_selected.lower() == 'month':  
            month= input('which month? all, January, February, March, April, May, or June? \n')
            while month.lower() not in months:
                month= input('which month? all, January, February, March, April, May, or June? \n')
            day = 'all'    
        elif filter_selected.lower() == 'day':  
            day= input('which day? all, Monday, Tuesday, Wednesday, Thursday,Friday, Saturday, Sunday? \n')
            while day.lower() not in days:
                day= input('which day? all, Monday, Tuesday, Wednesday, Thursday,Friday, Saturday, Sunday? \n')
            month='all'    
        elif filter_selected.lower() == 'not at all': 
            day = 'all'
            month = 'all'
    except:    
            print('incorrect input entered \n')

    return city.lower(), month.lower(), day.lower()


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
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #get month and day from date
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month 
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        #create new dataframe by selected month
        df = df[df['month'] == month]

    # filter by day 
    if day != 'all':
        #create the new dataframe by selected day
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #calculating most common  month
    mode_of_months=df['month'].mode()[0]
    #calculating most common  day
    mode_of_days=df['day_of_week'].mode()[0]
    #calculating most common  hour
    df['hours']=df['Start Time'].dt.hour
    mode_of_hours = df['hours'].mode()[0]
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('most common month is {} \nmost common day in week is {}'.format(mode_of_months,mode_of_days))
    print('most common hour in day is {} \n'.format(mode_of_hours))
 
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #calculating the most common start station,end station and trip
    mode_of_start = df['Start Station'].mode()[0]
    mode_of_end = df['End Station'].mode()[0]
    df['trip']= df['Start Station'] + df['End Station']
    mode_of_trips = df['trip'].mode()[0]  
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('most common start station is {} \nmost common end station is {} \nmost common trip is {} \n'.format(mode_of_start,mode_of_end,mode_of_trips))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    #calculating the total duration time and average duration time
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_duration = df['Trip Duration'].sum()
    average_duration = df['Trip Duration'].mean()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('total travel time is {} \naverage travel time is {} \n'.format(total_duration,average_duration))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_type_counts=df['User Type'].value_counts() #series of each type and its count
    print('Count of each user type: \n{}\n'.format(user_type_counts))
    
    if 'Gender'in df:
        #check if gender column exists in the selected dataset
        gender_count= df['Gender'].value_counts()  #series of each gender and its count
        df['Gender'] = df['Gender'].replace(np.nan,'not specified',inplace=True)
        print('Count of each gender: \n{}\n'.format(gender_count))
        
    #check if birth year columns exists in the selected dataset
    if 'Birth Year'in df:  #calculating the earliest, recent and most common birth year in NYC and Chicago
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        df['Birth Year'] = df['Birth Year'].replace(np.nan,common_year,inplace=True)
       
        print('earliest year is {} \nrecent year is {} \nmost common year is {} \n'.format(earliest_year,recent_year,common_year))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
        

def display_raw_data(df):
    """ this function displays five rows of the dataframe to the user according to his need
    input: takes a dataframe to display
    output: prints five rows of this dataframe
    """
    i = 0
    raw = input('Would you like to view five rows of data? Enter lower case yes or no.\n')
    pd.set_option('display.max_columns',200)

    while True:            
        if raw.lower() == 'no':
            break
        elif raw.lower() != 'yes':
            raw=input('please enter (yes) or (no) \n')
            if raw.lower()!='yes':
                continue
           
        print(df[i:i+5])
        raw = input('Would you like to view another five rows of data? Enter lower case yes or no.\n') 
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        #asking the user to restart or not
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while True:
            if restart.lower() != 'yes':
                if restart.lower()=='no':
                    break
                else: 
                    restart=input('please enter (yes) or (no) \n')
                    if restart.lower()!='yes':
                        continue
            else: 
                break
        
        if restart.lower()=='no':
                    break

if __name__ == "__main__":
	main()
