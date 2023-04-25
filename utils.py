from datetime import datetime as dt
from config import *
import math
import re
from shapes import ellipse

def timer(t, label):
    duration = dt.now() - t
    duration = duration.total_seconds()
    print("{} took {}".format(label, duration))
    return 






