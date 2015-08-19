import numpy as np
import pandas as pd
import subprocess
from unipath import Path

from django.conf import settings

class WaveformHandler(object):
    def __init__(self, src, reset = False, interval = 5, sampling_rate = 8000):
        self.mp3_src = src
        self.interval = 5
        self.sampling_rate = 8000

        mp3_name = Path(self.mp3_src).stem
        waveform_name = mp3_name + '.csv'
        self.waveform_dst = Path(settings.ANALYSES_DIR, waveform_name)

        if not self.waveform_dst.exists() or reset:
            self.analyze()

        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = pd.read_csv(self.waveform_dst, index_col = 0)
        return self._data

    @property
    def min(self):
        return self.data.y0.min()

    @property
    def max(self):
        return self.data.y1.max()

    @property
    def json(self):
        return self.data.to_json(orient = 'values')

    def analyze(self):
        data = np.frombuffer(
            subprocess.check_output([
                'ffmpeg',
                '-i', self.mp3_src,
                '-ac', '1',
                '-filter:a', 'aresample='+str(self.sampling_rate),
                '-map', '0:a',
                '-c:a', 'pcm_s16le',
                '-f', 'data', '-'
            ]),
            dtype = 'int16')

        num_samples = len(data)

        # size of window
        samples_in_interval = self.interval * self.sampling_rate
        num_intervals = num_samples / samples_in_interval

        # reshape the data so that each row is an interval
        num_samples_rounded = num_intervals * samples_in_interval
        chunks = np.reshape(data[:num_samples_rounded], (-1, samples_in_interval))
        del data

        # summarize the data
        low, high = np.percentile(chunks, [5, 95], axis = 1)
        waveform = pd.DataFrame({'y0': low,
                                 'y1': high})
        waveform.index *= self.interval
        waveform.index.name = 'time'
        waveform.to_csv(self.waveform_dst)

    def waveform_kwargs(self):
        return {
            'interval': self.interval,
            'values': self.json,
            'min': self.min,
            'max': self.max,
        }
