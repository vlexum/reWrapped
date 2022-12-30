import pandas as pd
import plotnine as p9

# what year do we want to look at
wrapped_year = "2022"

# list of json file names 
# must request song data from spotify - take about ~ 1 month to receive
filenames = ["endsong_0.json",
              "endsong_1.json",
              "endsong_2.json",
              "endsong_3.json",
              "endsong_4.json",
              "endsong_5.json",
              "endsong_6.json"]

# dicts for artist data
artist_num_played = {}
artist_ms_played = {}

# dicts for song data
song_num_played = {}
song_ms_played = {}

# look through all the data files
for filename in filenames:
    # convert file to dataframe
    listening_data = pd.read_json(filename)

    # loop through all song streams for that file
    for stream_index in listening_data.index:
        # get year from timestamp
        # starts with year so we can grab the first 4 chars
        streamed_year = listening_data["ts"][stream_index][:4]
        
        # check the steaming year 
        if (streamed_year == wrapped_year):
            # get artist
            artist = listening_data["master_metadata_album_artist_name"][stream_index]

            # get song
            song = listening_data["master_metadata_track_name"][stream_index]

            # keep track of how many times an artist/song was streamed 
            artist_num_played[artist] = artist_num_played.get(artist, 0) + 1
            song_num_played[song] = song_num_played.get(song, 0) + 1

            # how many ms of an artist/song was played
            artist_ms_played[artist] = artist_ms_played.get(artist, 0) + listening_data["ms_played"][stream_index]
            song_ms_played[song] = song_ms_played.get(song, 0) + listening_data["ms_played"][stream_index]

# Sort in descending order
num_artist_sorted = dict(sorted(artist_num_played.items(), key=lambda x:x[1], reverse=True))
ms_artist_sorted = dict(sorted(artist_ms_played.items(), key=lambda x:x[1], reverse=True))
num_song_sorted = dict(sorted(song_num_played.items(), key=lambda x:x[1], reverse=True))
ms_song_sorted = dict(sorted(song_ms_played.items(), key=lambda x:x[1], reverse=True))

# convert back to dataframe 
ms_artist_df = pd.DataFrame.from_dict(ms_artist_sorted, orient='index', columns=["Milliseconds Played in 2022 of Artist"])
num_artist_df = pd.DataFrame.from_dict(num_artist_sorted, orient='index', columns=["Number of Times Artist Streamed in 2022"])
ms_song_df = pd.DataFrame.from_dict(ms_song_sorted, orient='index', columns=["Milliseconds Played in 2022 of Song"])
num_song_df = pd.DataFrame.from_dict(num_song_sorted, orient='index', columns=["Number of Times Song Streamed in 2022"])

# html pages for easier data viewing
ms_artist_df.to_html("msArtistPlayed.html")
num_artist_df.to_html("numArtistPlayed.html")
ms_song_df.to_html("msSongPlayed.html")
num_song_df.to_html("numSongPlayed.html")
