import eyed3
from unipath import Path

from django.conf import settings

def get_mp3_meta_data(episode_media_url, meta_data_key):
    path_to_episode = _resolve_media_url(episode_media_url)
    episode_audio = eyed3.load(path_to_episode)
    return getattr(episode_audio.tag, meta_data_key)

def _resolve_media_url(url):
    relative = Path(url).split_root()[1]
    return Path(settings.MEDIA_ROOT.parent, relative)
