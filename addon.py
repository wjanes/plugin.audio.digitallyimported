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
        'house': {
        'Disco House': [f'http://prem2.di.fm/discohouse_hi?{apikey}', 'disco_house.jpg', addon.getLocalizedString(33100)],
        'Funky House': [f'http://prem2.di.fm/funkyhouse_hi?{apikey}', 'funky_house.jpg', addon.getLocalizedString(33101)],
        'Deep House': [f'http://prem2.di.fm/deephouse_hi?{apikey}', 'deep_house.jpg', addon.getLocalizedString(33102)],
        'House': [f'http://prem2.di.fm/house_hi?{apikey}', 'house.jpg', addon.getLocalizedString(33103)],
        'Deep Organic House': [f'http://prem2.di.fm/deeporganichouse_hi?{apikey}', 'deep_organic_house.jpg', addon.getLocalizedString(33104)],
        'Deep Progressive House': [f'http://prem2.di.fm/deepprogressivehouse_hi?{apikey}', 'deep_progressive_house.jpg', addon.getLocalizedString(33105)],
        'Vocal House': [f'http://prem2.di.fm/vocalhouse_hi?{apikey}', 'vocal_house.jpg', addon.getLocalizedString(33106)],
        'Slap House': [f'http://prem2.di.fm/slaphouse_hi?{apikey}', 'slap_house.jpg', addon.getLocalizedString(33107)],
        'Summer Chill House': [f'http://prem2.di.fm/summerchillhouse_hi?{apikey}', 'summer_chill_house.jpg', addon.getLocalizedString(33108)],
        'Soulful House': [f'http://prem2.di.fm/soulfulhouse_hi?{apikey}', 'soulful_house.jpg', addon.getLocalizedString(33109)],
        'Nu Disco': [f'http://prem2.di.fm/nudisco_hi?{apikey}', 'nu_disco.jpg', addon.getLocalizedString(33110)],
        'Tech House': [f'http://prem2.di.fm/techhouse_hi?{apikey}', 'tech_house.jpg', addon.getLocalizedString(33111)],
        'Elektro House': [f'http://prem2.di.fm/electrohouse_hi?{apikey}', 'electro_house.jpg', addon.getLocalizedString(33112)],
        'EDM Hits': [f'http://prem2.di.fm/edmhits_hi?{apikey}', 'edm_hits.jpg', addon.getLocalizedString(33113)],
        'Big Room House': [f'http://prem2.di.fm/bigroomhouse_hi?{apikey}', 'big_room_house.jpg', addon.getLocalizedString(33114)],
        'Bass & Jackin House': [f'http://prem2.di.fm/bassnjackinghouse_hi?{apikey}', 'bass_and_jacking_house.jpg', addon.getLocalizedString(33115)],
        'Bassline': [f'http://prem2.di.fm/baselinehouse_hi?{apikey}', 'bassline.jpg', addon.getLocalizedString(33116)],
        '00s Club Hits': [f'http://prem2.di.fm/00sclubhits_hi?{apikey}', '00s_club_hits.jpg', addon.getLocalizedString(33117)],
        'Jazz House': [f'http://prem2.di.fm/jazzhouse_hi?{apikey}', 'jazz_house.jpg', addon.getLocalizedString(33118)],
        'Old School House': [f'http://prem2.di.fm/oldschoolhouse_hi?{apikey}', 'oldschool_house.jpg', addon.getLocalizedString(33119)],
        'Electro Swing': [f'http://prem2.di.fm/electroswing_hi?{apikey}', 'electro_swing.jpg', addon.getLocalizedString(33120)],
        'Detroit House and Techno': [f'http://prem2.di.fm/detroithousentechno_hi?{apikey}', 'detroit_house_n_techno.jpg', addon.getLocalizedString(33121)],
        'Latin House': [f'http://prem2.di.fm/latinhouse_hi?{apikey}', 'latin_house.jpg', addon.getLocalizedString(33122)],
        'Tribal House': [f'http://prem2.di.fm/tribalhouse_hi?{apikey}', 'tribal_house.jpg', addon.getLocalizedString(33123)],
        'Progressive': [f'http://prem2.di.fm/progressive_hi?{apikey}', 'progressive.jpg', addon.getLocalizedString(33124)],
        'Iconic Radio': [f'http://prem2.di.fm/iconicradio_hi?{apikey}', 'iconic_radio.jpg', addon.getLocalizedString(33125)],
        'EDM Festival': [f'http://prem2.di.fm/edmfestival_hi?{apikey}', 'edm_festival.jpg', addon.getLocalizedString(33126)],
        'Melodic Progressive': [f'http://prem2.di.fm/melodicprogressive_hi?{apikey}', 'melodic_progressive.jpg', addon.getLocalizedString(33127)],
        'Elektro Pop': [f'http://prem2.di.fm/electropop_hi?{apikey}', 'electro_pop.jpg', addon.getLocalizedString(33128)],
        'Deep Nu Disco': [f'http://prem2.di.fm/deepnudisco_hi?{apikey}', 'deep_nu_disco.jpg', addon.getLocalizedString(33129)],
        'Deep Tech': [f'http://prem2.di.fm/deeptech_hi?{apikey}', 'deep_tech.jpg', addon.getLocalizedString(33130)],
        'Downtempo Lounge': [f'http://prem2.di.fm/downtemplounge_hi?{apikey}', 'downtempo_lounge.jpg', addon.getLocalizedString(33131)],
        'Chill & Tropical House': [f'http://prem2.di.fm/chillntropicalhouse_hi?{apikey}', 'chill_and_tropical_house.jpg', addon.getLocalizedString(33132)],
        'DJ Mixes': [f'http://prem2.di.fm/djmixes_hi?{apikey}', 'dj_mixes.jpg', addon.getLocalizedString(33133)]



    },
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
def create_listitem(title, url, icon, fanart, plot='', is_playable=True):
    liz = xbmcgui.ListItem(label=title, path=url)
    liz.setArt({'icon': icon, 'fanart': fanart, 'thumb': icon})
    liz.setInfo(type='music', infoLabels={'title': title, 'genre': plot})
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
    streams = STREAMS.get(genre, {}) # type: ignore
    xbmcplugin.setPluginCategory(_handle, 'DI.FM Streams')
    xbmcplugin.setContent(_handle, 'songs')
    for stream, data in streams.items():
        stream_url = data[0]
        stream_icon = get_image(data[1])
        stream_fanart = get_image(data[1])
        stream_title = stream or 'DI.FM Stream'
        stream_plot = data[2] if len(data) > 2 else ''
        liz = create_listitem(stream_title, stream_url, stream_icon, stream_fanart, plot=stream_plot)
        url = get_url({'action': 'play', 
                       'url': stream_url,
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
            play_stream._error_shown = True # type: ignore
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
