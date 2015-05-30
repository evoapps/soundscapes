import eyed3
from unipath import Path

from django.conf import settings

def get_meta_data(url_to_episode):
    episode_location = _resolve_url(url_to_episode)
    mp3_meta_data = _strip_meta_data(episode_location)
    return mp3_meta_data

def _resolve_url(url):
    relative = Path(url).split_root()[1]
    absolute = Path(settings.MEDIA_ROOT.parent, relative)
    return absolute

def _strip_meta_data(file_loc):
    meta = {}
    audiofile = eyed3.load(file_loc)
    meta['show'] = audiofile.tag.artist
    meta['number'] = audiofile.tag.track_num[0]
    meta['name'] = audiofile.tag.title
    return meta
