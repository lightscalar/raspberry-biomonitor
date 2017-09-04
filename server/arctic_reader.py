from arctic import Arctic
from filters import *
import numpy as np


store = Arctic('localhost')
session_id = '59ac3967378acd7ec3236656'
lib = store.get_library(session_id)

# Get the time.
t = lib.read('00-bio_time').data
v = lib.read('00-values').data
vf = lib.read('00-filt_values').data
v_filt, _ = lowpass(t, v, freq_cutoff=10, filter_order=5)

