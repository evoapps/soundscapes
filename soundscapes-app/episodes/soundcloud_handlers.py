from dateutil import parser
import soundcloud
import yaml
from unipath import Path

from django.conf import settings

def connect_to_soundcloud():
    path_to_soundcloud_secrets = Path(settings.BASE_DIR,
                                      'soundscapes/secrets.yml')

    with open(path_to_soundcloud_secrets, 'rb') as creds_handle:
        creds = yaml.load(creds_handle)

    return soundcloud.Client(client_id = creds['client_id'])

def search_soundcloud_for(api_route, q = None):
    client = connect_to_soundcloud()
    found = None

    response = client.get(api_route, q = q)
    if hasattr(response, '__iter__'):
        found = _search_for_gimlet(response)

    return found or response

def _search_for_gimlet(matches):
    found = None
    for match in matches:
        gimlet_in_tag_list = hasattr(match, 'tag_list') and \
                             match.tag_list.find('gimlet') > 0
        gimlet_in_website = hasattr(match, 'website') and \
                            match.website.find('gimlet') > 0
        # add other match conditions here

        if gimlet_in_tag_list or gimlet_in_website:
            found = match
            break

    return found

def convert_to_pydatetime(soundcloud_datetime):
    return parser.parse(soundcloud_datetime)
