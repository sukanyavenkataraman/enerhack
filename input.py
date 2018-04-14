'''
Read input
'''

import glob

class Input(object):
    def __init__(self, foldername):
        self.images = []

        normal_exp = glob.glob(foldername, '*_NE.*')

        for files in normal_exp:
            self.images.append(cv2.imread(img))