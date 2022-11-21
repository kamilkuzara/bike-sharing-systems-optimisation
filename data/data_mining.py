import pandas as pd
import json

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
        df = pd.read_csv(file, usecols=["Duration", "End Date", "EndStation Id", "Start Date", "StartStation Id"])
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

def perform_preprocessing(journeys_df, stations_df):
    stations_df = stations_preprocessing(stations_df)

    journeys_df = journeys_preprocessing(journeys_df, stations_df)

    return journeys_df, stations_df