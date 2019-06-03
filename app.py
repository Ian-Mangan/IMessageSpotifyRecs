import spotipy
import spotipy.util as util
import sqlite3
from urllib.parse import urlparse

def authorize(username):
	scope2 = 'playlist-read-private'
	scope1 = 'playlist-modify-private'
	token = util.prompt_for_user_token(username,scope=scope1 + " " + scope2,client_id='get_your_own',client_secret='API_key',redirect_uri='https://github.com/Ian-Mangan')
	return token

def checkForPlaylist():
	playlists = sp.current_user_playlists()
	user = sp.current_user()
	for playlist in playlists["items"]:
		if playlist['owner']['id'] == username and playlist['name'] == "Recs from IMessage":
			return playlist['id']
		else:
			newplaylistneeded = True
	if(newplaylistneeded):
		sp.user_playlist_create(user['id'], "Recs from IMessage", public=False)
		playlists = sp.current_user_playlists()
		for playlist in playlists["items"]:
			if playlist['owner']['id'] == username and playlist['name'] == "Recs from IMessage":
				return playlist['id']


def parseIMessage(cursor):
	sql_attatchments = cursor.execute("Select * FROM 'message' JOIN 'handle' ON 'handle'.ROWID = 'message'.handle_id WHERE 'message'.text LIKE '%spotify%'").fetchall()
	uri_list = []
	for i in sql_attatchments:
		link = i[2]
		parsed = urlparse(link)
		if parsed.path[:7] == "/track/":
			uri_list.append(parsed.path[7:])
	return uri_list

if __name__ == "__main__":
	username = input("Input your username from https://www.spotify.com/us/account/overview/: ")
	conn = sqlite3.connect('/Users/ian/Library/Messages/chat.db')
	c = conn.cursor()
	token = authorize(username)
	sp = spotipy.Spotify(auth=token)
	playlist_id = checkForPlaylist()
	uri_list = parseIMessage(c)
	sp.user_playlist_add_tracks(username,playlist_id,uri_list)
