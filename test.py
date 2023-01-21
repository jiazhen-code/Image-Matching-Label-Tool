import cv2
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt

ls = os.listdir('has_saved')
ls = [s.replace('.txt', '').replace('-', ' ')+'\n' for s in ls]
with open('worklist_check.txt', 'w') as f:
    f.writelines(ls)
