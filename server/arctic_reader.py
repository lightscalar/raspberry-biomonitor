from arctic import Arctic
from filters import *
import numpy as np


store = Arctic('localhost')
session_id = '59adaa8c378acdce232895ab'
lib = store.get_library(session_id)

# Get the time.
t = lib.read('00-t').data
t_sys = lib.read('00-t_sys').data
v = lib.read('00-v').data
vf = lib.read('00-v_filt').data

