import os,sys,json,spotipy,webbrowser
import spotipy.util as util
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import datetime
import statistics
from json.decoder import JSONDecodeError


# SPOTIPY_CLIENT_ID = '72bfe33eb8b9438d8019faaf22c01357'
# SPOTIPY_CLIENT_SECRET = '516b5e1fd4b548d69e908ea1e16269dc' 
# SPOTIPY_REDIRECT_URI = 'http://google.com/'

# ye to userid dera hy 
username = sys.argv[1]
#userID = xopcuaslx0pf7gwqrrewm9v81?si=8blLRe_NTJGT4jIKjGRbzg
scope = "user-read-private user-library-read user-read-recently-played"



#userid or scope mila kr. token mangalo shabash  
try:
    token = util.prompt_for_user_token(username,scope)
except(AttributeError,JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username,scope)


spotifyObject = spotipy.Spotify(auth=token)


date_format = "%Y-%m-%dT%H:%M:%SZ"
saved_counts = 0
played_counts = 0
genres_played = []
genres_saved = []
chart_genres = []


# saved tracks dekhlo jani
for item in spotifyObject.current_user_saved_tracks()['items']:
    track = item['track']
    date = datetime.datetime.strptime(item['added_at'], date_format)
    
    trackid = item['track']['id']
    popularity = item['track']['popularity']
    
    for artist in item['track']['artists']:
        artist_name = artist['name']
        genres = spotifyObject.artist(artist['id'])['genres']
        genres_saved = genres_saved + genres
        if date.year == datetime.datetime.now().year:
            chart_genres = chart_genres + genres
        # print(track['name'] + ' - ' + artist['name']+' - '+date)

    for feature in spotifyObject.audio_features(trackid):
        audio_features={
        'Dancability':feature['danceability'],
        'Energy':feature['energy'],
        'Instrumentalness':feature['instrumentalness'],
        'Liveness':feature['liveness'],
        'Acousticness':feature['acousticness']
        }    
    saved_counts += 1




#played tracks dekhlo jani
for item in spotifyObject.current_user_recently_played()['items']:
    trackid = item['track']['id']
    track_name = item['track']['name']

    for artist in item['track']['artists']:
        # artist_name = artist['name']
        genres_played = genres_played + spotifyObject.artist(artist['id'])['genres']

    for feature in spotifyObject.audio_features(trackid):
        audio_features={
        'Dancability':feature['danceability'],
        'Energy':feature['energy'],
        'Instrumentalness':feature['instrumentalness'],
        'Liveness':feature['liveness'],
        'Acousticness':feature['acousticness']
        }  
    played_counts += 1




# charts dekhlo jani


# indicator 1
my_dict = {i:chart_genres.count(i) for i in chart_genres}
pyplot.pie([float(v) for v in my_dict.values()], labels=[k for k in my_dict],autopct=None)
pyplot.savefig('new.png')


# indicator 2



danceability = []
energy = []
instrumentalness = []
liveness = []
acousticness = []

for item in spotifyObject.current_user_recently_played(limit=24)['items']:
    trackid = item['track']['id']

    for feature in spotifyObject.audio_features(trackid):
        danceability.append(feature['danceability'])
        energy.append(feature['energy'])
        instrumentalness.append(feature['instrumentalness'])
        liveness.append(feature['liveness'])
        acousticness.append(feature['acousticness'])
        
df = pd.DataFrame(
    {
        'Danceability':danceability,
        'Energy':energy,
        'Instrumentalness':instrumentalness,
        'Liveness':liveness,
        'Acousticness':acousticness
    }
)

totals = [i+j+k+l+m for i,j,k,l,m in zip(df['Danceability'], df['Energy'], df['Instrumentalness'],df['Liveness'],df['Acousticness'])]

danceability = [i / j * 100 for i,j in zip(df['Danceability'][0:20], totals)]
energy = [i / j * 100 for i,j in zip(df['Energy'][0:20], totals)]
instrumentalness = [i / j * 100 for i,j in zip(df['Instrumentalness'][0:20], totals)]
liveness = [i / j * 100 for i,j in zip(df['Liveness'][0:20], totals)]
acousticness = [i / j * 100 for i,j in zip(df['Acousticness'][0:20], totals)]

barWidth = 0.8
r = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] 
labels = [x for x in range(1,21)]
pyplot.bar(r, danceability, color='#f9bc86', edgecolor='white', width=barWidth)
pyplot.bar(r, energy, bottom=danceability, color='red', edgecolor='white', width=barWidth)
pyplot.bar(r, instrumentalness, bottom=[i+j for i,j in zip(danceability,energy)], color='#a3acff', edgecolor='white', width=barWidth)
pyplot.bar(r, liveness, bottom=[i+j+k for i,j,k in zip(danceability,energy,instrumentalness)], color='blue', edgecolor='white', width=barWidth)
pyplot.bar(r, acousticness, bottom=[i+j+k+l for i,j,k,l in zip(danceability,energy,instrumentalness,liveness)], color='green', edgecolor='white', width=barWidth)

pyplot.xticks(r,labels)
pyplot.xlabel("previous 20 trackes listned to")
pyplot.savefig('new2.png')






#indicator 3

danceability = []
energy = []
instrumentalness = []
liveness = []
acousticness = []
count=0

for item in spotifyObject.current_user_saved_tracks()['items']:
    trackid = item['track']['id']
    date = datetime.datetime.strptime(item['added_at'], date_format)
    last26weeks = datetime.datetime.now() - datetime.timedelta(days=182)
    if date > last26weeks:        
        for feature in spotifyObject.audio_features(trackid):
            danceability.append(feature['danceability'])
            energy.append(feature['energy'])
            instrumentalness.append(feature['instrumentalness'])
            liveness.append(feature['liveness'])
            acousticness.append(feature['acousticness'])
        count+=1
    

            
df = pd.DataFrame(
    {
        'Danceability':danceability,
        'Energy':energy,
        'Instrumentalness':instrumentalness,
        'Liveness':liveness,
        'Acousticness':acousticness
    }
)

totals = [i+j+k+l+m for i,j,k,l,m in zip(df['Danceability'], df['Energy'], df['Instrumentalness'],df['Liveness'],df['Acousticness'])]

danceability = [i / j * 100 for i,j in zip(df['Danceability'], totals)]
energy = [i / j * 100 for i,j in zip(df['Energy'], totals)]
instrumentalness = [i / j * 100 for i,j in zip(df['Instrumentalness'], totals)]
liveness = [i / j * 100 for i,j in zip(df['Liveness'], totals)]
acousticness = [i / j * 100 for i,j in zip(df['Acousticness'], totals)]



datenow = datetime.datetime.now()
weeks = datenow
mean_dict = {}
median_dict = {}
last26weeks = datenow - datetime.timedelta(weeks=26) 


for week in range(26):
    danceabilityMeans = []
    energyMeans = []
    instrumentalnessMeans = []
    livenessMeans = []
    acousticnessMeans = []
    for item in spotifyObject.current_user_saved_tracks()['items']:
        trackid = item['track']['id']
        date = datetime.datetime.strptime(item['added_at'], date_format)

        if date > weeks - datetime.timedelta(weeks=week) and date < weeks:

            for feature in spotifyObject.audio_features(trackid):
                danceabilityMeans.append(feature['danceability'])
                energyMeans.append(feature['energy'])
                instrumentalnessMeans.append(feature['instrumentalness'])
                livenessMeans.append(feature['liveness'])
                acousticnessMeans.append(feature['acousticness'])

    if danceabilityMeans:    
        mean_dict.update({"Week "+str(week)+" Means":{
            'Danceability':statistics.mean(danceabilityMeans),
            'Energy':statistics.mean(energyMeans),
            'Instrumentalness':statistics.mean(instrumentalnessMeans),
            'Liveness':statistics.mean(livenessMeans),
            'Acousticness':statistics.mean(acousticnessMeans)
        }})
        median_dict.update({"Week "+str(week)+" Medians":{
            'Danceability':statistics.median(danceabilityMeans),
            'Energy':statistics.median(energyMeans),
            'Instrumentalness':statistics.median(instrumentalnessMeans),
            'Liveness':statistics.median(livenessMeans),
            'Acousticness':statistics.median(acousticnessMeans)
        }})
    weeks = weeks - datetime.timedelta(weeks=week)
    


allmeans = [x for x in mean_dict['Week 1 Means'].values()]
allmedians = [x for x in median_dict['Week 1 Medians'].values()]

# will visualize it later




#indicator 4

graph_dict={}


for week in range(52):
    popularity = 0
    for item in spotifyObject.current_user_saved_tracks(limit=50)['items']:
        date = datetime.datetime.strptime(item['added_at'], date_format)
        if date > weeks - datetime.timedelta(weeks=week) and date < weeks:
            popularity += item['track']['popularity']

    graph_dict.update({week:popularity})
    weeks = weeks - datetime.timedelta(weeks=week)      
            

x,y = [x for x in graph_dict.keys()] , [y for y in graph_dict.values()]

pyplot.plot(x, y)
pyplot.savefig('new4.png')

