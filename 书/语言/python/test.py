'''
Description: 
Version: 2.0
Autor: dundun
'''

from collections import deque
from collections import defaultdict
from collections import namedtuple
from datetime import datetime
import numpy as np
import pandas as pd
import sys

ts = pd.Series(np.arange(4),
                index=pd.date_range('2025-1-1', periods=4, freq='M'))
print(ts)
print(ts.shift(2))
print(ts.shift(2, freq='ME'))


