# Spotify-playlist-generator
Simple Spotify playlist generator implemented in Python using Spotify's API and a custom depth first search algorithm. 
Enter an artist and it will generate a playlist based on related artists down the search tree.

## How to run script
To run the script you will have to have a Spotify account. 

Follow this guide to get a client id and client secret: https://developer.spotify.com/documentation/web-api/quick-start/

You will have to add a redirect url for your app under "edit settings" on the Dashboard page. 

When you are done with that, add the client id, client secret and redirect url to the script and you are good to go!
```python
client_id = "" ## insert your client_id
client_secret = "" ##insert your client_secret
redirect_uri = "" # insert your redirect uri
```
