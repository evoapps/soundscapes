import json
import numpy as np
from PIL import Image

def serialize_color_scheme(color_scheme):
    rgb_scheme = []
    for i, (r,g,b) in enumerate(color_scheme):
        rgb_scheme.append("rgb({},{},{})".format(r,g,b))
    return json.dumps(rgb_scheme)

def extract_color_scheme(src, n = 5):
    img = Image.open(src).convert('RGB')
    color_scheme = palette(img)
    return color_scheme[:n]

def palette(img):
    """
    Return palette in descending order of frequency
    """
    arr = np.asarray(img)
    palette, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    return palette[order[::-1]]

def asvoid(arr):
    """View the array as dtype np.void (bytes)
    This collapses ND-arrays to 1D-arrays, so you can perform 1D operations on them.
    http://stackoverflow.com/a/16216866/190597 (Jaime)
    http://stackoverflow.com/a/16840350/190597 (Jaime)
    Warning:
    >>> asvoid([-0.]) == asvoid([0.])
    array([False], dtype=bool)
    """
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))