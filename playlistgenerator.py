import json
import spotipy
import webbrowser
import sys
import spotipy.util as util
import spotipy.oauth2 as oauth2
from json.decoder import JSONDecodeError
import collections
import queue
import random

#-------------------------- Get id for artist ----------------------------------------

def get_id_for_artist(artist_name):
    searchResults = spotify.search(artist_name, 1, 0, "artist")
    artist_id = searchResults['artists']['items'][0]['id']
    return artist_id

#-------------------------- Gets related artists for an artist ----------------------------------------

def get_related_artists(id, depth):
    child_artists = []
    child_artist_depth = depth + 1
    related_artists = spotify.artist_related_artists(id)
    random.shuffle(related_artists)
    for child_artist in related_artists['artists'][:3]: ## get related artists, shuffle and add 3
        artist_node = artist(child_artist['id'], child_artist['name'], child_artist_depth)
        child_artists.append(artist_node)
    return child_artists

#-------------------------- Depth First Search function to get artists ----------------------------------------

def get_artists_for_playlist(artist_id, artist_name, min_depth, max_depth):
    artist_node = artist(artist_id, artist_name, 0)
    frontier = queue.LifoQueue()
    explored = []
    artists = []
    related_artists = []
    artists.append(artist_node.id)
    frontier.put(artist_node)
    while (not frontier.empty()):
        artist_node = frontier.get()
        if (artist_node.depth < min_depth and artist_node.id in artists):
            artists.remove(artist_node.id)
        if (artist_node not in explored):
            if (artist_node.depth >= min_depth and artist_node.id not in artists):
                artists.append(artist_node.id)
            explored.append(artist_node.id)
        if (artist_node.depth != max_depth):
            related_artists = get_related_artists(artist_node.id, artist_node.depth)
            for related_artist in related_artists:
                if (related_artist.id not in explored):
                    frontier.put(related_artist)
    return artists


#-------------------------- main ----------------------------------------

client_id = "" ## insert your client_id
client_secret = "" ##insert your client_secret
redirect_uri = "" # insert your redirect uri

acc_name = input('Enter your Spotify account name: ')
playlist_name = input('Enter the name of the playlist you want to create: ')
artist_name = input('Enter the name of an artist: ')
print('Creating playlist', playlist_name,)

artist = collections.namedtuple('artist', 'id name depth') 
token = util.prompt_for_user_token(acc_name,"playlist-modify-public",client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)

if token:
    spotify = spotipy.Spotify(auth=token)
    spotify.trace = False
    print("Generating playlist...")
    tmp_artist_id = get_id_for_artist(artist_name)
    artists = get_artists_for_playlist(tmp_artist_id, artist_name, 2, 5) ## Depth First Seach to get related artists
    track_ids = []
    for artist in artists:
        results = spotify.artist_top_tracks(artist) ##ID
        random.shuffle(results)
        for track in results['tracks'][:3]: ## shuffle the artists top tracks and choose one
            tmp_track = "spotify:track:" + track['id']
            track_ids.append(tmp_track)
    random.shuffle(track_ids)
    playlists = spotify.user_playlist_create(acc_name, playlist_name) ## create the playlist
    webbrowser.open(playlists['external_urls']['spotify'])
    spotify.user_playlist_add_tracks(acc_name, playlists['id'], track_ids) ## add the tracks to playlist
    print("Success")
