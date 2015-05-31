import yaml
import soundcloud
from unipath import Path

from django.conf import settings

def connect_to_soundcloud():
    path_to_soundcloud_secrets = Path(settings.BASE_DIR,
                                      'soundscapes/secrets.yml')

    with open(path_to_soundcloud_secrets, 'rb') as creds_handle:
        creds = yaml.load(creds_handle)

    return soundcloud.Client(client_id = creds['client_id'])
