import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import sys
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import os

addon = xbmcaddon.Addon()
apikey = addon.getSettingString("apikey")
addonpath = addon.getAddonInfo('path')
player = xbmc.Player()

streams = dict(
    {'Disco House': ['http://prem2.di.fm/discohouse?' + apikey, 'disco_house.jpg',addon.getLocalizedString(33100)],
     'Funky House': ['http://prem2.di.fm/funkyhouse?' + apikey, 'funky_house.png',addon.getLocalizedString(33101)]})

def get_url(params):
    return '{0}?{1}'.format(_url, urlencode(params))


def get_image(image):
    return os.path.join(addonpath, 'resources', 'images', image)


def list_streams():
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Streams')
    xbmcplugin.setContent(_handle, 'songs')

    for stream in streams:
        liz = xbmcgui.ListItem(label=stream)
        liz.setPath(streams[stream][0])
        liz.setArt({'icon': get_image(streams[stream][1]),
                    'fanart': get_image(streams[stream][1])})
        liz.setInfo(type='video', infoLabels={'plot': streams[stream][2]})

        liz.setProperty('IsPlayable', 'true')
        url = get_url({'action': 'play', 'url': streams[stream][0],
                       'icon': get_image(streams[stream][1]),
                       'title': 'DI.FM Stream'.format(stream),
                       'fanart': get_image(streams[stream][1])})

        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=False)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_stream(path, icon, title, fanart):
    if player.isPlaying():
        xbmc.log('Stop player')
        player.stop()
    xbmc.log('Playing {}'.format(path))
    play_item = xbmcgui.ListItem(path=path)
    play_item.setInfo('music', {'title': title})
    play_item.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(route):
    params = dict(parse_qsl(route))
    xbmc.log('Parameter list: {}'.format(params), xbmc.LOGDEBUG)
    if params:
        if params['action'] == 'play':
            play_stream(params['url'], params['icon'], params['title'], params['fanart'])
    else:
        list_streams()


_url = sys.argv[0]
_handle = int(sys.argv[1])

if __name__ == '__main__':
    try:
        router(sys.argv[2][1:])
    except IndexError:
        pass
