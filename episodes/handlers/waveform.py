import numpy as np
import pandas as pd
import subprocess
from unipath import Path

from django.conf import settings

def get_waveform(src, interval = 5, reset = False):
    audio_name = Path(src).name
    waveform_name = audio_name + '.csv'
    waveform_dst = Path(settings.ANALYSES_DIR, waveform_name)

    if not waveform_dst.exists() or reset:
        sampling_rate = 8000
        data = np.frombuffer(
            subprocess.check_output([
                'ffmpeg',
                '-i', src,
                '-ac', '1',
                '-filter:a', 'aresample='+str(sampling_rate),
                '-map', '0:a',
                '-c:a', 'pcm_s16le',
                '-f', 'data', '-'
            ]),
            dtype = 'int16')

        num_samples = len(data)

        # size of window
        samples_in_interval = interval * sampling_rate
        num_intervals = num_samples / samples_in_interval

        # reshape the data so that each row is an interval
        num_samples_rounded = num_intervals * samples_in_interval
        chunks = np.reshape(data[:num_samples_rounded], (-1, samples_in_interval))
        del data

        # summarize the data
        low, high = np.percentile(chunks, [5, 95], axis = 1)
        waveform = pd.DataFrame({'y0': low,
                                 'y1': high})
        waveform.index *= interval
        waveform.index.name = 'time'
        waveform.to_csv(waveform_dst)

    waveform = pd.read_csv(waveform_dst, index_col = 0)
    return waveform.to_json(orient = 'values')
