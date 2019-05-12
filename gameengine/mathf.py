import time
import os
import random



def Clamp(value,minvalue,maxvalue):
    if(value < minvalue):
        value = minvalue
        return value
    if(value > maxvalue):
        value = maxvalue
        return value
    return value
