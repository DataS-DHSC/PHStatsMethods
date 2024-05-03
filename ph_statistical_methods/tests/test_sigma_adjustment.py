# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:08:49 2024

@author: Jack.Burden_DHSC
"""
from utils_funnel import sigma_adjustment
import pytest


sigma_adjustment(0.975, 100000, 0.9, "low", 100)