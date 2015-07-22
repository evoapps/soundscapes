import subprocess
from math import ceil
from unipath import Path

from django.conf import settings

import pydub

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

        dbfs_of_peaks = [chunk.dBFS for chunk in moments]
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
