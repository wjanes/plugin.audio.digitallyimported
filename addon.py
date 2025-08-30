import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import sys
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import os


# === DI.FM Kodi Addon ===
# Refactored: zentrale Datenhaltung, Hilfsfunktionen, Logging, bessere Wartbarkeit

addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')
apikey = addon.getSetting("apikey")
player = xbmc.Player()

# --- Genres und Streams zentral ---
GENRES = {
    'house': 'House',
    # Weitere Genres hier ergänzen
}

STREAMS = {
    'house': {
        'Disco House': [f'http://prem2.di.fm/discohouse?{apikey}', 'disco_house.jpg', addon.getLocalizedString(33100)],
        'Funky House': [f'http://prem2.di.fm/funkyhouse?{apikey}', 'funky_house.png', addon.getLocalizedString(33101)],
    },
    # Weitere Genres und Streams hier ergänzen
}


def get_url(params):
    """
    Baut eine Plugin-URL mit den übergebenen Parametern
    """
    return '{0}?{1}'.format(_url, urlencode(params))


def get_image(image):
    """
    Gibt den Pfad zu einem Bild in resources/images zurück
    """
    return os.path.join(addonpath, 'resources', 'images', image)

def log(msg, level=xbmc.LOGDEBUG):
    """
    Einheitliches Logging
    """
    xbmc.log(f'[DI.FM Addon] {msg}', level)

def create_listitem(title, url, icon, fanart, plot='', genre='', is_playable=True):
    """
    Erstellt und konfiguriert ein Kodi ListItem für einen Stream oder Ordner
    """
    liz = xbmcgui.ListItem(label=title, path=url)
    liz.setArt({'icon': icon, 'fanart': fanart, 'thumb': icon})
    liz.setInfo(type='music', infoLabels={'title': title, 'plot': plot, 'genre': genre})
    if is_playable:
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('mimetype', 'audio/mpeg')
    return liz


def list_genres():
    """
    Zeigt alle verfügbaren Genres als Unterordner im Kodi-Plugin an
    """
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Genres')
    for genre_id, genre_name in GENRES.items():
        url = get_url({'action': 'list_streams', 'genre': genre_id})
        liz = xbmcgui.ListItem(label=genre_name)
        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)

def list_streams(genre=None):
    """
    Zeigt alle Streams eines Genres als abspielbare ListItems an
    """
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


def play_stream(path, icon, title, fanart):
    """
    Startet die Wiedergabe eines ausgewählten Streams
    """
    if player.isPlaying():
        log('Stop player')
        player.stop()
    log(f'Playing {path}')
    play_item = create_listitem(title or 'DI.FM Stream', path, icon, fanart)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(route):
    """
    Router-Funktion: Steuert die Navigation und Aktionen im Plugin anhand der URL-Parameter
    """
    params = dict(parse_qsl(route))
    log('Parameter list: {}'.format(params))
    if params:
        if params['action'] == 'play':
            play_stream(params['url'], params['icon'], params['title'], params['fanart'])
        elif params['action'] == 'list_streams':
            list_streams(params.get('genre'))
    else:
        list_genres()


_url = sys.argv[0]
_handle = int(sys.argv[1])

if __name__ == '__main__':
    try:
        router(sys.argv[2][1:])
    except IndexError:
        pass
