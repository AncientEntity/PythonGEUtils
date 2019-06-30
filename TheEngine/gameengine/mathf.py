import time
import os
import random



def Clamp(value,minvalue,maxvalue):
    """
    Forces the given value to be within the minvalue and maxvalue.
    """
    if(value < minvalue):
        value = minvalue
        return value
    if(value > maxvalue):
        value = maxvalue
        return value
    return value
