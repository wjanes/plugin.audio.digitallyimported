import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import sys
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import os


# === DI.FM Kodi Addon by Groovie ===
# Refactored: zentrale Datenhaltung, Hilfsfunktionen, Logging, bessere Wartbarkeit

addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')
apikey = addon.getSetting("apikey")
player = xbmc.Player()

# --- Genres und Streams zentral ---
GENRES = {
    'trance': "Trance",
    'house': 'House',
    'lounge': 'Lounge',
    'techno': 'Techno',
    'deep': 'Deep',
    'edm': 'EDM',
    'chillout': 'Chillout',
    'bass': 'Bass',
    'dance': 'Dance',
    'vocal': 'Vocal',
    'hard': 'Hard',
    'ambience': 'Ambience',
    'synth': 'Synth',
    'classic': 'Classic'
}

STREAMS = {
    'trance': {
        'Trance': [f'http://prem2.di.fm/trance_hi?{apikey}', 'trance.jpg', addon.getLocalizedString(33200)],
        'Epic Trance': [f'http://prem2.di.fm/epictrance_hi?{apikey}', 'epic_trance.jpg', addon.getLocalizedString(33201)],
        'Vocal Trance': [f'http://prem2.di.fm/vocaltrance_hi?{apikey}', 'vocal_trance.jpg', addon.getLocalizedString(33202)],
        'Deep Progressive Trance': [f'http://prem2.di.fm/deepprogressivetrance_hi?{apikey}', 'deep_progressive_trance.jpg', addon.getLocalizedString(33203)],
        'Classic Trance': [f'http://prem2.di.fm/classictrance_hi?{apikey}', 'classic_trance.jpg', addon.getLocalizedString(33204)],
        'Classic Vocal Trance': [f'http://prem2.di.fm/classicvocaltrance_hi?{apikey}', 'classic_vocal_trance.jpg', addon.getLocalizedString(33205)],
        'Melodic Progressive': [f'http://prem2.di.fm/melodicprogressive_hi?{apikey}', 'melodic_progressive.jpg', addon.getLocalizedString(33206)],
        'Goa-Psy Trance': [f'http://prem2.di.fm/goapsy_hi?{apikey}', 'goa_psy_trance.jpg', addon.getLocalizedString(33207)],
        'Progressive': [f'http://prem2.di.fm/progressive_hi?{apikey}', 'progressive.jpg', addon.getLocalizedString(33208)],
        'DJ Mixes': [f'http://prem2.di.fm/djmixes_hi?{apikey}', 'dj_mixes.jpg', addon.getLocalizedString(33209)],
        'Progressive Psy': [f'http://prem2.di.fm/progressivepsy_hi?{apikey}', 'progressive_psy.jpg', addon.getLocalizedString(33210)],
        'Dark Psytrance': [f'http://prem2.di.fm/darkpsytrance_hi?{apikey}', 'dark_psytrance.jpg', addon.getLocalizedString(33211)],
        'Hands Up': [f'http://prem2.di.fm/handsup_hi?{apikey}', 'hands_up.jpg', addon.getLocalizedString(33212)]

    },
    'house': {
        'Disco House': [f'http://prem2.di.fm/discohouse_hi?{apikey}', 'disco_house.jpg', addon.getLocalizedString(33100)],
        'Funky House': [f'http://prem2.di.fm/funkyhouse_hi?{apikey}', 'funky_house.jpg', addon.getLocalizedString(33101)],
        'Deep House': [f'http://prem2.di.fm/deephouse_hi?{apikey}', 'deep_house.jpg', addon.getLocalizedString(33102)],
    }
}

# Baut eine Plugin-URL mit den übergebenen Parametern
def get_url(params):
    return '{0}?{1}'.format(_url, urlencode(params))


# Gibt den Pfad zu einem Bild in resources/images zurück
def get_image(image):
    return os.path.join(addonpath, 'resources', 'images', image)

# Einheitliches Logging
def log(msg, level=xbmc.LOGDEBUG):
    xbmc.log(f'[DI.FM Addon] {msg}', level)

# Erstellt und konfiguriert ein Kodi ListItem für einen Stream oder Ordner
def create_listitem(title, url, icon, fanart, plot='', genre='', is_playable=True):
    liz = xbmcgui.ListItem(label=title, path=url)
    liz.setArt({'icon': icon, 'fanart': fanart, 'thumb': icon})
    liz.setInfo(type='music', infoLabels={'title': title, 'plot': plot, 'genre': genre})
    if is_playable:
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('mimetype', 'audio/mpeg')
    return liz


# Zeigt alle verfügbaren Genres als Unterordner im Kodi-Plugin an
def list_genres():
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Genres')
    for genre_id, genre_name in GENRES.items():
        url = get_url({'action': 'list_streams', 'genre': genre_id})
        liz = xbmcgui.ListItem(label=genre_name)
        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)

# Zeigt alle Streams eines Genres als abspielbare ListItems an
def list_streams(genre=None):
    streams = STREAMS.get(genre, {})
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Streams')
    xbmcplugin.setContent(_handle, 'songs')
    for stream, data in streams.items():
        stream_url = data[0]
        stream_icon = get_image(data[1])
        stream_fanart = get_image(data[1])
        stream_title = stream or 'DI.FM Stream'
        stream_plot = data[2] if len(data) > 2 else ''
        liz = create_listitem(stream_title, stream_url, stream_icon, stream_fanart, plot=stream_plot, genre=genre or '')
        url = get_url({'action': 'play', 'url': stream_url,
                       'icon': stream_icon,
                       'title': stream_title,
                       'fanart': stream_fanart})
        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=False)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

# Startet die Wiedergabe eines ausgewählten Streams
def play_stream(path, icon, title, fanart):
    if not apikey or apikey.strip() == '':
        if not hasattr(play_stream, '_error_shown'):
            xbmcgui.Dialog().notification('DI.FM', 'API Key erforderlich!', xbmcgui.NOTIFICATION_ERROR, 5000)
            log('Abspielen abgebrochen: Kein API Key', xbmc.LOGERROR)
            play_stream._error_shown = True
        return
    
    if player.isPlaying():
        log('Stop player')
        player.stop()
    log(f'Playing {path}')
    play_item = create_listitem(title or 'DI.FM Stream', path, icon, fanart)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


# Router-Funktion: Steuert die Navigation und Aktionen im Plugin anhand der URL-Parameter
def router(route):
    params = dict(parse_qsl(route))
    log('Parameter list: {}'.format(params))
    if params:
        if params['action'] == 'play':
            play_stream(params['url'], params['icon'], params['title'], params['fanart'])
        elif params['action'] == 'list_streams':
            list_streams(params.get('genre'))
    else:
        list_genres()

# Einstiegspunkt
_url = sys.argv[0]
_handle = int(sys.argv[1])

if __name__ == '__main__':
    try:
        router(sys.argv[2][1:])
    except IndexError:
        pass
