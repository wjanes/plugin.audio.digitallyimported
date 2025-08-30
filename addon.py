import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import sys
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import os

addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')
player = xbmc.Player()


def get_url(params):
    return '{0}?{1}'.format(_url, urlencode(params))


def get_image(image):
    return os.path.join(addonpath, 'resources', 'images', image)


def list_genres():
    genres = {
        'house': 'House',
        # Hier können weitere Genres ergänzt werden
    }
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Genres')
    for genre_id, genre_name in genres.items():
        url = get_url({'action': 'list_streams', 'genre': genre_id})
        liz = xbmcgui.ListItem(label=genre_name)
        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)

def list_streams(genre=None):
    all_streams = {
        'house': {
            'Disco House': ['http://prem2.di.fm/discohouse?' + xbmcaddon.Addon().getSetting("apikey"),
                            'disco_house.jpg', addon.getLocalizedString(33100)],
            'Funky House': ['http://prem2.di.fm/funkyhouse?' + xbmcaddon.Addon().getSetting("apikey"),
                            'funky_house.png', addon.getLocalizedString(33101)],
        },
        # Weitere Genres und Streams können hier ergänzt werden
    }
    streams = all_streams.get(genre, {})
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Streams')
    xbmcplugin.setContent(_handle, 'songs')
    for stream in streams:
        stream_url = streams[stream][0]
        stream_icon = get_image(streams[stream][1])
        stream_fanart = get_image(streams[stream][1])
        stream_title = stream or 'DI.FM Stream'
        stream_plot = streams[stream][2] if len(streams[stream]) > 2 else ''
        liz = xbmcgui.ListItem(label=stream_title, path=stream_url)
        liz.setArt({'icon': stream_icon, 'fanart': stream_fanart, 'thumb': stream_icon})
        liz.setInfo(type='music', infoLabels={'title': stream_title, 'plot': stream_plot, 'genre': genre or ''})
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('mimetype', 'audio/mpeg')
        url = get_url({'action': 'play', 'url': stream_url,
                       'icon': stream_icon,
                       'title': stream_title,
                       'fanart': stream_fanart})
        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=False)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_stream(path, icon, title, fanart):
    if player.isPlaying():
        xbmc.log('Stop player')
        player.stop()
    xbmc.log('Playing {}'.format(path))
    play_item = xbmcgui.ListItem(path=path)
    play_item.setInfo('music', {'title': title or 'DI.FM Stream'})
    play_item.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    play_item.setProperty('IsPlayable', 'true')
    play_item.setProperty('mimetype', 'audio/mpeg')
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(route):
    params = dict(parse_qsl(route))
    xbmc.log('Parameter list: {}'.format(params), xbmc.LOGDEBUG)
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
