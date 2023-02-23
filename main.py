import pandas as pd
from geopy import distance
import matplotlib.pyplot as plt
import folium

pd.set_option('display.width', 1080)  # Pandas adjustment to the width view in print command
pd.set_option('display.max_columns', 100)  # Pandas tweak to not hide columns in print command


# defines a function to calculate the distance between two geographic points
def calc_distance(geo):
    if pd.isnull(geo[['start_lat', 'start_lng', 'end_lat', 'end_lng']]).any():
        return float('nan')
    lat1, long1, lat2, long2 = geo[['start_lat', 'start_lng', 'end_lat', 'end_lng']]
    coords_1 = (lat1, long1)
    coords_2 = (lat2, long2)
    return distance.distance(coords_1, coords_2).km


# read the CSV files and set the variables
df_2022_02 = pd.read_csv("Data/tripdata_2022_02.csv")
df_2022_03 = pd.read_csv("Data/tripdata_2022_03.csv")
df_2022_04 = pd.read_csv("Data/tripdata_2022_04.csv")
df_2022_05 = pd.read_csv("Data/tripdata_2022_05.csv")
df_2022_06 = pd.read_csv("Data/tripdata_2022_06.csv")
df_2022_07 = pd.read_csv("Data/tripdata_2022_07.csv")
df_2022_08 = pd.read_csv("Data/tripdata_2022_08.csv")
df_2022_09 = pd.read_csv("Data/tripdata_2022_09.csv")
df_2022_10 = pd.read_csv("Data/tripdata_2022_10.csv")
df_2022_11 = pd.read_csv("Data/tripdata_2022_11.csv")
df_2022_12 = pd.read_csv("Data/tripdata_2022_12.csv")
df_2023_01 = pd.read_csv("Data/tripdata_2023_01.csv")

# display information from the DataFrames
print(df_2022_02.info())
print(df_2022_03.info())
print(df_2022_04.info())
print(df_2022_05.info())
print(df_2022_06.info())
print(df_2022_07.info())
print(df_2022_08.info())
print(df_2022_09.info())
print(df_2022_10.info())
print(df_2022_11.info())
print(df_2022_12.info())
print(df_2023_01.info())

# create a single DataFrame with all information grouped together
df_tripdata = pd.concat([df_2022_02, df_2022_03, df_2022_04, df_2022_05, df_2022_06, df_2022_07, df_2022_08, df_2022_09,
                         df_2022_10, df_2022_11, df_2022_12, df_2023_01], axis=0)
# displays information from the DataFrame df_tripdata
# print(df_tripdata.info())

# modifies string format to datetime in "started_at" and "ended_at" attributes
df_tripdata['started_at'] = pd.to_datetime(df_tripdata['started_at'], format='%Y-%m-%d %H:%M:%S')
df_tripdata['ended_at'] = pd.to_datetime(df_tripdata['ended_at'], format='%Y-%m-%d %H:%M:%S')
# print(df_tripdata.info())

# add a column for duration
df_tripdata['duration'] = df_tripdata['ended_at'] - df_tripdata['started_at']

# add a column for the day of the week
df_tripdata['day_of_week'] = df_tripdata['started_at'].dt.day_name()

# NOT USED DUE TO THE DELAY IN CALCULATION PROCESSING #
# adds a column with the calculation of the distance between the geographic coordinates of the collection and
# delivery points (was not used due to delay in calculation processing)
# df_tripdata['distance_km'] = df_tripdata.apply(calc_distance, axis=1)


# reorder the columns for better visualization of the data
df_tripdata = df_tripdata[['ride_id', 'rideable_type', 'member_casual', 'started_at', 'ended_at', 'duration',
                           'day_of_week', 'start_station_name', 'start_station_id', 'end_station_name',
                           'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng']]

# check for duplicate records
duplicates = df_tripdata['ride_id'].duplicated()
if duplicates.any():
    print('There are duplicate values in the ride_id column')
else:
    print('There are no duplicate values in the ride_id column')

# look for anomalies in the duration of the rides
print(df_tripdata['duration'].describe())

# count null values in the "duration" column
count_null_duration = df_tripdata['duration'].isnull().sum()
print("There are", count_null_duration, "null values in the duration column.")

# count negative or zero values in the "duration" column
count_neg_duration = (df_tripdata['duration'] <= pd.Timedelta(0)).sum()
print("There are", count_neg_duration, "negative or equal to zero in the duration column.")

# eliminate rows with negative or zero values in the "duration" column
df_tripdata = df_tripdata.loc[df_tripdata['duration'] > pd.Timedelta(0)]

# count values greater than or equal to 1 day in the "duration" column
count_duration_greater_than_1day = (df_tripdata['duration'] >= pd.Timedelta(days=1)).sum()
print("There are", count_duration_greater_than_1day, "values greater than or equal to 1 day in the duration column.")

# delete values greater than or equal to 1 day in the "duration" column
df_tripdata = df_tripdata.loc[df_tripdata['duration'] < pd.Timedelta(days=1)]
# print(df_tripdata['duration'].describe())

# count the null values in each column of the DataFrame
for attribute in df_tripdata:
    nulls = df_tripdata[attribute].isnull().sum()
    print(f"The column {attribute} has {nulls} null values.")

# Display DataFrame information
print(df_tripdata.info())
print(df_tripdata.head())


'''
##########
## PLOT ##
##########
'''

# Charts for analysis

''' Proportion of Users'''  # pie chart
# count values in each category of the 'member_casual' column
count_users = df_tripdata['member_casual'].value_counts()
# create the pie chart
colors = ['#4285F4', '#DB4437']
count_users.plot(kind='pie', autopct='%1.1f%%', colors=colors)
# set title and display chart
plt.title('Proportion of Users: "Member" and "Casual"', fontdict={'fontname': 'Roboto', 'fontsize': 18})
plt.axis('equal')
plt.axis('off')
plt.show()

'''Count of trips started per month'''  # line chart
# group by month and count occurrences for each user category
count_tsm = df_tripdata.groupby([df_tripdata['started_at'].dt.strftime('%Y-%m'), 'member_casual'])['ride_id'].count()
# create the line chart
colors = ['#DB4437', '#4285F4']
count_tsm.unstack().plot(kind='line', color=colors)
# configure axis title and labels
plt.title('Count of Trips Started per Month', fontdict={'fontname': 'Roboto', 'fontsize': 18})
plt.xlabel('Month')
plt.ylabel('Number of Trips')
plt.legend(title='User Type', loc='upper right')
plt.xticks(rotation=45)
plt.show()

'''Trip Count by Day of Week and Member Type'''  # stacked column chart
# converting column "day_of_week" to category type
df_tripdata['day_of_week'] = pd.Categorical(df_tripdata['day_of_week'], categories=['Monday', 'Tuesday', 'Wednesday',
                                                                                    'Thursday', 'Friday', 'Saturday',
                                                                                    'Sunday'], ordered=True)
# group data by 'day_of_week' and 'member_casual' and count occurrences
df_grouped = df_tripdata.groupby(['day_of_week', 'member_casual']).size().unstack()
# create the stacked column chart
colors = ['#DB4437', '#4285F4']
stacked = df_grouped.plot(kind='bar', stacked=True, color=colors)
# cConfigure axis title and labels
stacked.set_title('Trip Count by Day of Week and Member Type', fontdict={'fontname': 'Roboto', 'fontsize': 18})
stacked.set_xlabel('Day of the Week')
stacked.set_ylabel('Trip Count')
plt.legend(title='User Type', loc='upper left')
plt.xticks(rotation=45)
plt.show()

'''Mean Trip Duration by Month and User Type  # clustered bar chart'''
# calculates the average of trip times in minutes, separated by month, year and type of user
mean_tsm = df_tripdata.groupby([df_tripdata['started_at']
                               .dt.strftime('%Y-%m'), 'member_casual'])['duration'].mean().dt.total_seconds() / 60
# converts the timedelta type data to float so that it can be inserted into the chart
mean_tsm = mean_tsm.astype(float)
# creates the clustered bar chart
colors = ['#DB4437', '#4285F4']
mean_dur_user = mean_tsm.unstack().plot(kind='bar', rot=45, color=colors)
# defines the axis title and labels
mean_dur_user.set_xlabel('Month and Year')
mean_dur_user.set_ylabel('Mean Trip Duration (minutes)')
mean_dur_user.set_title('Mean Trip Duration by Month and User Type', fontdict={'fontname': 'Roboto', 'fontsize': 18})
plt.legend(title='User Type', loc='upper right')
plt.show()

# eliminate rows with null values in column 'member_casual'
df_clean_member_casual = df_tripdata.dropna(subset=['member_casual'])

'''Top Start Stations by Casual Users'''  # horizontal bar chart
# group by station and user type and count the number of occurrences
df_grouped_start_station = df_clean_member_casual.groupby(['start_station_name', 'member_casual']).size().unstack()
# select only the top 21 casual type counts
df_grouped_start_station = df_grouped_start_station.sort_values(by='casual', ascending=False).head(21)
df_grouped_start_station = df_grouped_start_station.sort_values(by='casual', ascending=True)
# create clustered bar chart
colors = ['#DB4437', '#4285F4']
df_grouped_start_station.plot(kind='barh', stacked=True, color=colors)
# configure the chart
plt.title('Top Casual Users Start Stations', fontdict={'fontname': 'Roboto', 'fontsize': 18})
plt.xlabel('Number of trips')
plt.ylabel('Start station name')
plt.legend(title='User Type', loc='lower right')
plt.show()

'''Top End Stations by Casual Users'''  # horizontal bar chart
# group by station and user type and count the number of occurrences
df_grouped_end_station = df_clean_member_casual.groupby(['end_station_name', 'member_casual']).size().unstack()
# select only the top 21 casual type counts
df_grouped_end_station = df_grouped_end_station.sort_values(by='casual', ascending=False).head(21)
df_grouped_end_station = df_grouped_end_station.sort_values(by='casual', ascending=True)
# create clustered bar chart
colors = ['#DB4437', '#4285F4']
df_grouped_end_station.plot(kind='barh', stacked=True, color=colors)
# configure the chart
plt.title('Top Casual Users End Stations', fontdict={'fontname': 'Roboto', 'fontsize': 18})
plt.xlabel('Number of trips')
plt.ylabel('End station name')
plt.legend(title='User Type', loc='lower right')
plt.show()

''' Top Stations DataFrame with Geolocation'''  # df_top_stations DataFrame
# sums the start and end values for the 21 stations most used by casual users
df_top_stations = df_grouped_start_station.head(21).add(df_grouped_end_station.head(21), fill_value=0, axis=0)
# ranks the stations with the highest number of casual users
df_top_stations = df_top_stations.sort_values('casual', ascending=False)
# adds the geolocation data for each station
df_top_stations = df_top_stations.reset_index()
df_top_stations.rename(columns={'index': 'start_station_name'}, inplace=True)
df_geo_info = df_tripdata[['start_station_name', 'start_lat', 'start_lng']]
df_top_stations = df_top_stations.merge(df_geo_info.groupby('start_station_name')
                                        .first(), on='start_station_name', how='left')
df_top_stations.rename(columns={'start_station_name': 'station_name', 'start_lat': 'lat', 'start_lng': 'lng'},
                       inplace=True)
print(df_top_stations)

'''Top Stations Interactive Map'''  # interactive map
# create an interactive map centered on Chicago
map_chicago = folium.Map(location=[41.9000, -87.6298], zoom_start=13)
# sets the scale factor and add circles for each station
scale_factor = 0.0005
for index, row in df_top_stations.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lng']], radius=row['member']*scale_factor, color='#4285F4',
                        fill=True, fill_color='#4285F4', popup=row['station_name']).add_to(map_chicago)
    folium.CircleMarker(location=[row['lat'], row['lng']], radius=row['casual']*scale_factor, color='#DB4437',
                        fill=True, fill_color='#DB4437', popup=row['station_name']).add_to(map_chicago)
# add title and legend to the map
title_html = '''
             <h3 align="center" style="font-size:20px"><b>Top Stations Rides</b></h3>
             '''
map_chicago.get_root().html.add_child(folium.Element(title_html))
legend_html = '''
                <div style="position: fixed; 
                            bottom: 50px; left: 50px; width: 150px; height: 90px; 
                            border:2px solid grey; z-index:9999; font-size:14px;
                            background-color:white;
                            ">
                            <p><b>    Users</b></p>
                            <p><span style='color:#4285F4;'>&#9679;</span>  Member</p>
                            <p><span style='color:#DB4437;'>&#9679;</span>  Casual</p>
                </div>
                '''
map_chicago.get_root().html.add_child(folium.Element(legend_html))
# adds markers with station names
for index, row in df_top_stations.iterrows():
    folium.Marker(location=[row['lat'], row['lng']], popup=row['station_name'],
                  tooltip=row['station_name']).add_to(map_chicago)
# adds controls layer
folium.LayerControl().add_to(map_chicago)
# saves the map in html format
map_chicago.save('Data/map_chicago.html')
