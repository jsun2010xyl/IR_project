import requests

def getTrackName(tid):
    response = requests.get('https://api.musixmatch.com/ws/1.1/track.get?track_id=' +
                            str(tid), params={'apikey': '4bc22c0c5eba9feffab3727257a61677'})
    if response.json()['message']['header']['status_code'] == 200:
        return response.json()['message']['body']['track']['track_name']
    return '!Not Found'

def getLyrics(tid):
    response = requests.get('https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id=' +
                            str(tid), params={'apikey': '4bc22c0c5eba9feffab3727257a61677'})
    if response.json()['message']['header']['status_code'] == 200:
        return response.json()['message']['body']['lyrics']['lyrics_body']
    return '!Not Found'
