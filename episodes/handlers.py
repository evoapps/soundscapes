from unipath import Path
import subprocess

# RSS handling
import feedparser
import json
import requests

# mp3 handling
# import numpy as np
import pydub
from math import ceil
# from scipy import weave
# import scipy.io.wavfile
#
# import pandas as pd

from django.conf import settings
from django.core.files import File

weave_code = r"""
int i, j, ct, jmin, jmax, ii;
double sum=0;
for(ii = 0; ii < nsamples_mva; ++ii){
sum = 0;
ct = 0;
i = samples[ii];
jmin = i - index_width;
jmax = i + index_width;

if(i - index_width < 0)
jmin = 0;

if(i + index_width > nn)
jmax = nn;

for(j = jmin; j < jmax; ++j){
sum += y_squared[j];
ct++;
}
mva[ii] = sum / ct;
mva_ts[ii] = ts[i];
}
"""

def fetch_rss_entries(rss_url, n = None):
    """ Retrieve entries from an RSS feed

    n: the number of recent episodes to return

    Defaults to returning the full feed.
    """
    feed = feedparser.parse(rss_url)
    entries = feed['entries']
    n = n or len(entries)
    return entries[0:n]

def dump_rss_entry(rss_entry):
    # hack! "json.dumps(rss_entry)" chokes on time object
    modified_rss_entry = rss_entry.copy()
    modified_rss_entry['published_parsed'] = \
        str(modified_rss_entry['published_parsed'])
    return json.dumps(modified_rss_entry)

def download_episode(downloadable_url):
    """ A URL from the media_content['url'] of an RSS entry.

    This function does not rename the file. It only downloads the file
    if the expected name is not present in the DOWNLOADS_DIR directory.

    Returns a django.core.files.File object that can be fed to a FileField.
    """
    download_dir = Path(settings.DOWNLOADS_DIR)
    if not download_dir.exists():
        download_dir.mkdir()

    name_in_url = Path(downloadable_url).name
    expected_loc = Path(download_dir, name_in_url)

    # only download if necessary
    if not expected_loc.exists():
        response = requests.get(downloadable_url, stream = True)
        with open(expected_loc, 'wb') as expected_loc_handle:
            for chunk in response.iter_content(chunk_size = 1024):
                expected_loc_handle.write(chunk)

    return File(open(expected_loc, 'rb'))

def get_audio_duration(mp3_name):
    downloaded_mp3 = Path(settings.DOWNLOADS_DIR, mp3_name)

    json_data = subprocess.check_output(
        ['avprobe', '-show_format', '-of', 'json', downloaded_mp3]
    )
    duration = float(json.loads(json_data)['format']['duration'])
    return duration

def get_audio_features(mp3_name, interval_size = 5000.0):
    analyses_dir = Path(settings.ANALYSES_DIR)
    if not analyses_dir.exists():
        analyses_dir.mkdir()

    converted_wav = _convert_mp3_to_wav(mp3_name)
    chunks_of_wav = _break_wav_into_chunks(converted_wav)

    values = list()
    for chunk in chunks_of_wav:
        segment = pydub.AudioSegment.from_file(chunk, format = 'wav')
        moments = pydub.utils.make_chunks(segment, interval_size)
        del segment

        dbfs_of_peaks = [chunk.max_dBFS for chunk in moments]
        del moments

        values.extend([max(0, loudness + 120) for loudness in dbfs_of_peaks])

    times = [i * (interval_size / 1000.0) for i in range(len(values))]
    return zip(times, values)

def _convert_mp3_to_wav(mp3_name):
    stem = Path(mp3_name).stem

    downloaded_mp3 = Path(settings.DOWNLOADS_DIR, stem + '.mp3')
    converted_wav = Path(settings.ANALYSES_DIR, stem + '.wav')

    subprocess.check_output(['avconv', '-i', downloaded_mp3, converted_wav])
    return converted_wav

def _break_wav_into_chunks(full_length_wav, chunk_size = 600.0):
    stem = Path(full_length_wav).stem

    recreate_mp3_name = Path(full_length_wav).stem + '.mp3'
    duration = get_audio_duration(recreate_mp3_name)
    num_chunks = int(ceil(duration/chunk_size))
    start_times = [i * chunk_size for i in range(num_chunks)]
    chunk_names = ['{stem}-{i}-of-{total}.wav'.format(stem = stem, i = i, total = num_chunks - 1)
                   for i in range(num_chunks)]
    chunk_paths = [Path(settings.ANALYSES_DIR, name) for name in chunk_names]

    formatted_chunk_time = _format_time_for_avconv(chunk_size)

    for start, out_path in zip(start_times, chunk_paths):
        formatted_start_time = _format_time_for_avconv(start)
        subprocess.check_output(['avconv', '-i', full_length_wav, '-ss', formatted_start_time, '-t', formatted_chunk_time, out_path])

    return chunk_paths

def _format_time_for_avconv(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%d:%02d:%02d' % (hours, minutes, seconds)
