import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import geopandas as gpd

def get_data_file_paths(data_file_registry_path = "./data_files.json"):
    with open(data_file_registry_path) as path_registry_file:
        file_info_json = json.load(path_registry_file)

    journeys_files = []
    journeys = file_info_json["journeys"]
    for file in journeys["file_names"]:
        journeys_files.append(journeys["directory_path"] + file)

    stations_file = file_info_json["stations"]["directory_path"] + file_info_json["stations"]["file_name"]

    return journeys_files, stations_file

def load_journeys_data(file_paths = ["./journeys.csv"]):
    journey_dataframes = []
    for file in file_paths:
        df = pd.read_csv(file, usecols=["Duration", "End Date", "EndStation Id", "Start Date", "StartStation Id"], parse_dates=["End Date", "Start Date"])
        journey_dataframes.append(df)

    journeys_output_df = pd.concat(journey_dataframes, ignore_index = True)

    return journeys_output_df

def load_stations_data(file_path = "./stations.csv"):
    stations_df = pd.read_csv(file_path, usecols=["id", "lat", "long", "installed", "locked", "removalDate", "temporary", "nbDocks"])

    return stations_df

def load_data():
    journeys_files, stations_file = get_data_file_paths()

    journeys_df = load_journeys_data(journeys_files)
    stations_df = load_stations_data(stations_file)

    return journeys_df, stations_df

def stations_preprocessing(stations_df):
    # drop stations that are:
    # - not installed ("installed" == False) OR
    # - locked ("locked" == True) OR
    # - temporary ("temporary" == True) OR
    # - were removed ("removalDate" is not NaN, i.e. contains a value)
    stations_df = stations_df.drop(stations_df[(stations_df["installed"] == False) | (stations_df["locked"] == True) | (stations_df["temporary"] == True) | (stations_df.isnull()["removalDate"] == False)].index)

    # drop the columns that are not needed anymore
    stations_df = stations_df.drop(["installed", "locked", "temporary", "removalDate"], axis = 1)

    # drop stations for which the capacity is 0 or negative
    # those are likely out of service or the data is incorrect
    stations_df = stations_df.drop(stations_df[stations_df["nbDocks"] <= 0].index)

    return stations_df

def journeys_preprocessing(journeys_df, stations_df):
    # get IDs of available stations
    station_IDs = list(stations_df["id"])

    # drop all those journeys that start OR end at an unavailable station
    # where an unavailable station is one that is not present in the stations_df
    journeys_df = journeys_df.drop(journeys_df[(~journeys_df["EndStation Id"].isin(station_IDs)) | (~journeys_df["StartStation Id"].isin(station_IDs))].index)

    # drop journeys with duration < 0; they are clearly invalid
    journeys_df = journeys_df.drop(journeys_df[journeys_df["Duration"] < 0].index)

    # drop entries where no actual journey took place, i.e. rows such that:
    # - start station == end station AND
    # - duration < 60 seconds
    journeys_df = journeys_df.drop(journeys_df[(journeys_df["EndStation Id"] == journeys_df["StartStation Id"]) & (journeys_df["Duration"] < 60)].index)

    return journeys_df

def drop_inactive_stations(journeys_df, stations_df):
    pickup_stations = journeys_df["StartStation Id"].unique()
    return_stations = journeys_df["EndStation Id"].unique()

    # drop stations with zero pickups AND zero returns; those are inactive stations
    stations_df = stations_df.drop(stations_df[(~stations_df["id"].isin(pickup_stations)) & (~stations_df["id"].isin(return_stations))].index)

    return stations_df

def perform_preprocessing(journeys_df, stations_df):
    stations_df = stations_preprocessing(stations_df)

    journeys_df = journeys_preprocessing(journeys_df, stations_df)

    # remove stations not included in any journeys, i.e. with zero pickups and zero returns
    stations_df = drop_inactive_stations(journeys_df, stations_df)

    return journeys_df, stations_df

# THE FUNCTION NEEDS REFACTORING/OPTIMISATION: CONVERSION TO INT TAKES INCREDIBLY LONG
def get_journey_durations_minutes(journeys_df):
    # get journey durations in the form of a pandas Series
    durations = journeys_df["Duration"]

    # convert to minutes
    durations = durations / 60

    # convert the values from double to int
    # very slow and memory hungry, needs optimisation
    durations = durations.apply(lambda x: int(x))

    return durations

def compute_journey_durations_distribution(durations):
    # compute the distribution of journey durations
    distribution = durations.value_counts()

    return distribution

# describe the journey durations pandas.Series in terms of mean, std deviation, etc.
def describe_durations(durations):
    return durations.describe().apply( lambda x: format(x, "f") )

# compute the percentage of journeys shorter than 60 minutes
def percentage_journeys_lt_hour(distribution):
    # count the number of journeys shorter than or equal to 60 minutes
    short_journeys = distribution[distribution.index <= 60].sum()

    # get total number of journeys
    total_journeys = distribution.sum()

    return short_journeys / total_journeys * 100

def compute_journeys_per_weekday(journeys_df):
    days = [0,1,2,3,4,5,6]

    journeys_per_weekday = []
    for day in days:
        day_df = journeys_df.loc[ journeys_df["Day of week"] == day ]
        hourly_distribution = day_df["Hour"].value_counts().reindex(list(range(0,24)),fill_value=0)
        journeys_per_weekday.append( list(hourly_distribution.values) )

    return journeys_per_weekday

def compute_activity_per_station(journeys_df, stations_df):
    station_IDs = stations_df["id"].values

    num_days = len(set(journeys_df["Start Date"].values).union(set(journeys_df["End Date"].values)))

    pickups = []
    returns = []
    total_activity = []
    total_net_flow = []
    avg_net_flow = []
    for id in station_IDs:
        station_pickups = len(journeys_df.loc[ journeys_df["StartStation Id"] == id ])
        pickups.append(station_pickups)

        station_returns = len(journeys_df.loc[ journeys_df["EndStation Id"] == id ])
        returns.append(station_returns)

        total_activity.append( station_pickups + station_returns )

        station_net_flow = station_returns - station_pickups
        total_net_flow.append( station_net_flow )
        avg_net_flow.append( station_net_flow / num_days )

    return pickups, returns, total_activity, total_net_flow, avg_net_flow


def plot_journeys_durations_distribution(distribution):
    X = distribution.index.to_list()
    Y = distribution.to_list()
    plt.bar(X,Y)
    plt.title("Distribution of journey durations")
    plt.xlabel("Duration of a journey in minutes")
    plt.ylabel("Number of journeys")
    plt.show()

# THIS IS HARD-CODED FOR NOW BASED ON VISUAL ANALYSIS OF THE PLOTS GENERATED BY plot_stations_pickups_returns()
# def remove_outliers(journeys_df, stations_df):
#     max_pickups = 50000
#     max_returns = 50000
#
#     # get number of pickups for each station
#     pickups = journeys_df["StartStation Id"].value_counts()
#     # filter the pickups
#     pickups = pickups[pickups <= max_pickups]
#
#     # drop the stations which have more pickups than max_pickups; the outliers
#     stations_df = stations_df.drop(stations_df[~stations_df["id"].isin(pickups.index)].index)
#     # remove the journeys that originate at those stations
#     journeys_df = journeys_df.drop(journeys_df[~journeys_df["StartStation Id"].isin(pickups.index)].index)
#
#     # get number of returns for each station
#     returns = journeys_df["EndStation Id"].value_counts()
#     # filter the returns
#     returns = returns[returns <= max_returns]
#
#     # drop the stations which have more returns than max_returns; the outliers
#     stations_df = stations_df.drop(stations_df[~stations_df["id"].isin(returns.index)].index)
#     # remove the journeys that terminate at those stations
#     journeys_df = journeys_df.drop(journeys_df[~journeys_df["EndStation Id"].isin(returns.index)].index)
#
#     return journeys_df, stations_df

def plot_stations_pickups_returns(journeys_df, stations_df):
    pickups = journeys_df["StartStation Id"].value_counts()
    pickups = pickups.reindex(stations_df["id"], fill_value=0)
    X = pickups.index.to_list()
    Y = pickups.to_list()
    plt.subplot(1,2,1)
    plt.plot(X, Y, "bo")
    plt.title("Total number of pickups in the measured timespan")
    plt.xlabel("Station ID")
    plt.ylabel("Number of pickups")

    returns = journeys_df["EndStation Id"].value_counts()
    returns = returns.reindex(stations_df["id"], fill_value=0)
    X = returns.index.to_list()
    Y = returns.to_list()
    plt.subplot(1,2,2)
    plt.plot(X, Y, "go")
    plt.title("Total number of returns in the measured timespan")
    plt.xlabel("Station ID")
    plt.ylabel("Number of returns")

    plt.show()

def plot_journeys_per_weekday(journeys_per_weekday):
    # Y = [ val for day in journeys_per_weekday for val in day ]
    # X = list( range(0, len(Y)) )
    #
    # plt.plot(X,Y, marker="o")
    #
    # plt.title("Journeys in the course of week")
    # plt.xlabel("Time of week")
    # plt.ylabel("Number of journeys")
    #
    # for i in range(0, len(X)-1, 48):
    #     plt.axvspan(i, i+24, facecolor='b', alpha=0.15, zorder=-100)
    #
    # plt.show()

    # ###########################################################################

    my_xticks1 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ,'Saturday' ,'Sunday']
    my_major_xticks = ['00' , '00','00','00','00','00' , '00' , '00']
    my_minor_xticks = [0 , 6 , 12 , 18 , 24 , 30 , 36 , 42 , 48 , 54 , 60 , 66 , 72 , 78 , 84 , 90 , 96 , 102 , 108 , 114 , 120 , 126 , 132 , 138 , 144 , 150 , 156 , 162 , 168]
    my_minor_label = ['06' , '12' , '18' , '06' , '12' , '18' , '06' , '12' , '18' ,'06' , '12' , '18', '06' , '12' , '18' , '06' , '12' , '18' , '06' , '12' , '18']

    fig, ax = plt.subplots()

    Y = [ val for day in journeys_per_weekday for val in day ]
    X = list( range(0, len(Y)) )

    # ax.plot(X,Y, marker="o")
    ax.plot(X,Y)

    plt.title("Journeys in the course of week")
    plt.xlabel("Time of week")
    plt.ylabel("Number of journeys")

    for i in range(24, len(X)-1, 48):
        plt.axvspan(i, i+24, facecolor='b', alpha=0.15, zorder=-100)

    plt.xlim(-1,168)
    plt.ylim(0, 90_000)

    #set the major xticks by its location and the location is presented by the length of the list
    # plt.xticks([0,23,47,71,95,119,143,167] , my_major_xticks)
    plt.xticks([0,24,48,72,96,120,144,168] , my_major_xticks)
    # both for x and y axis

    ax.tick_params('both', length=7, width=1, which='major')
    plt.grid(which="both")

    # control the minor locator and added a fixedlocator function to it
    ax.xaxis.set_minor_locator(FixedLocator(my_minor_xticks))
    # add the label to the minor locator
    ax.xaxis.set_minor_formatter(FixedFormatter(my_minor_label))

    num = 11
    for i, xpos in enumerate(ax.get_xticks()):
        if(i == 7):
            break;
        ax.text(num,450, my_xticks1[i],
                size = 10, ha = 'center')
        num = num + 24

    plt.show()

def plot_stations_map(stations_df, col):
    # map = gpd.read_file("./data_visualisation/shapefiles/v3/London_Borough_Excluding_MHW.shp")
    # map = map.to_crs(epsg=4326)
    #
    # s_gdf = gpd.GeoDataFrame(stations_df, geometry = gpd.points_from_xy(stations_df["long"], stations_df["lat"]))
    #
    # ax = map["geometry"].plot()
    #
    # s_gdf["geometry"].plot(ax=ax, color="green")

    map = gpd.read_file("./data_visualisation/shapefiles/v4/London_buildings.shp")
    map = map.to_crs(epsg=4326)

    s_gdf = gpd.GeoDataFrame(stations_df, geometry = gpd.points_from_xy(stations_df["long"], stations_df["lat"]))

    fig, ax = plt.subplots()

    map.plot(ax=ax, alpha=0.4)

    s_gdf.plot(column=col, ax=ax, cmap="Oranges", legend=True, legend_kwds={"shrink": 0.3})

    ax.set_facecolor("lightblue")
    ax.set_alpha(0.15)

    plt.show()

def plot_map(map, s_gdf, col, colourmap, title):
    fig, ax = plt.subplots()

    map.plot(ax=ax, alpha=0.6)

    s_gdf.plot(column=col, ax=ax, cmap=colourmap, legend=True, legend_kwds={"shrink": 0.3})

    ax.set_facecolor("lightblue")
    ax.set_alpha(0.3)

    plt.xlim(-0.2560, 0.0225)
    plt.ylim(51.4130, 51.5820)

    plt.title(title)
    plt.xlabel("longitude")
    plt.ylabel("latitude")

    plt.show()
