from unipath import Path

# RSS handling
import feedparser
import json
import requests

# mp3 handling
import numpy as np
import pydub
from scipy import weave
import scipy.io.wavfile

import pandas as pd

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

def get_audio_duration(mp3_file):
    audio_segment = pydub.AudioSegment.from_mp3(mp3_file)
    return audio_segment.duration_seconds

def get_audio_features(mp3_file):
    analyses_dir = Path(settings.ANALYSES_DIR)
    if not analyses_dir.exists():
        analyses_dir.mkdir()

    expected_file = Path(mp3_file.name).stem + '.csv'
    expected_loc = Path(analyses_dir, expected_file)

    if not expected_loc.exists():
        audio_segment = pydub.AudioSegment.from_mp3(mp3_file)

        # step 1: convert mp3 to wav
        temp_wav = Path(analyses_dir, Path(mp3_file.name).stem + '.wav')
        wav_segment = audio_segment.export(temp_wav, format = 'wav')

        rate, data = scipy.io.wavfile.read(wav_segment)
        ys = np.asarray(data[:,1], dtype = float)
        nsamples = len(ys)
        total_file_time = nsamples / rate

        ts, dt = np.linspace(0, total_file_time, nsamples, retstep = True)

        delta_sample = 5.0
        delta_window = delta_sample * 2
        index_width = (int)(delta_window / dt)

        nn = len(ys)
        samples = np.arange(0, nn, (int) (delta_sample / dt))
        nsamples_mva = len(samples)

        mva = np.zeros(nsamples_mva)
        mva_ts = np.zeros(nsamples_mva)

        y_squared = (ys**2)

        weave.inline(weave_code, ['y_squared', 'nn', 'mva', 'index_width', 'samples', 'nsamples_mva', 'mva_ts', 'ts'])

        frame = pd.DataFrame({'t': mva_ts, 'y': mva})
        frame.to_csv(expected_loc)

    frame = pd.read_csv(expected_loc)
    return frame.t.values, frame.y.values
