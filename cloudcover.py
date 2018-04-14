'''
given a set of images, segment them, get the movement of objects, calculate cloud cover
using dense optical flow
'''
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import glob

import cv2
import numpy as np

class CloudCover(object):
    def __init__(self, imgs, time):

        self.imgs = []
        for img in imgs:
            self.imgs.append(cv2.imread(img))

        self.num = len(imgs)
        self.time = time

    def segmentImgs(self):

        segmentedImg = self.imgs[0:100]
        print (len(segmentedImg))
        for img in segmentedImg:
            print ('Segmenting img...')
            grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            # sure background area
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg, sure_fg)

            # Marker labelling
            ret, markers = cv2.connectedComponents(sure_fg)
            # Add one to all labels so that sure background is not 0, but 1
            markers = markers + 1
            # Now, mark the region of unknown with zero
            markers[unknown == 255] = 0

            markers = cv2.watershed(img, markers)
            img[markers == -1] = [255, 0, 0]

        cv2.imwrite('segment.png', segmentedImg[0])
        return segmentedImg

    def opticalFlow(self, imgs):

        prev = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
        flow = np.zeros_like(imgs[0], dtype=np.float32)
        flow[...,1] = 255

        flow_img = None
        for i in xrange(1, len(imgs)):
            curr = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2GRAY)
            #curr = imgs[i]

            print (curr.shape)
            flow_current = cv2.calcOpticalFlowFarneback(prev,curr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow_current[..., 0], flow_current[..., 1])

            print (flow_current.shape, mag.shape, ang.shape)
            flow[..., 0] = ang * 180 / np.pi / 2
            flow[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
            bgr = cv2.cvtColor(flow, cv2.COLOR_HSV2BGR)
            #cv2.imshow('frame2', bgr)
            #cv2.waitKey()
            prev = curr

            if i == len(imgs) -1:
                cv2.imwrite('opticalfb.png', curr)
                cv2.imwrite('opticalhsv.png', bgr)
                flow_img = bgr

        print (flow)
        cv2.destroyAllWindows()
        return flow_img

    def opticalFlowSparse(self, imgs):
        # params for ShiTomasi corner detection
        feature_params = dict(maxCorners=100,
                              qualityLevel=0.3,
                              minDistance=7,
                              blockSize=7)

        # Parameters for lucas kanade optical flow
        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # Create some random colors
        color = np.random.randint(0, 255, (100, 3))

        # Take first frame and find corners in it
        prev = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(prev, mask=None, **feature_params)
        # Create a mask image for drawing purposes
        mask = np.zeros_like(imgs[0])
        for i in xrange(1, len(imgs)):
            curr = imgs[i]
            frame_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
            # calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(prev, frame_gray, p0, None, **lk_params)
            # Select good points
            good_new = p1[st == 1]
            good_old = p0[st == 1]
            # draw the tracks
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
                frame = cv2.circle(curr, (a, b), 5, color[i].tolist(), -1)
            img = cv2.add(frame, mask)
            #cv2.imshow('frame', img)
            #k = cv2.waitKey(30) & 0xff
            #if k == 27:
            #    break

            # Now update the previous frame and previous points
            prev = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

        cv2.imshow('frame', frame)
        cv2.imwrite('frame.png', frame)
        cv2.waitKey(100)
        cv2.destroyAllWindows()

    def cloudCover(self):

        print ('Segmenting Images...')
        segmented_imgs = self.segmentImgs(input)
        print ('Calculating optical flow...')
        opflow_imgs = self.opticalFlow(segmented_imgs)
        print ('Calculating cloud cover...')
        cloud_cover, time = self.cloudCover(opflow_imgs)

        return cloud_cover, time

def main():
    foldername = '/Users/sukanya/Downloads/20180408/'
    input = glob.glob(foldername+'*_NE.*')

    cc = CloudCover(input, 10)
    seg = cc.segmentImgs()
    cc.opticalFlowSparse(seg)

if __name__ == "__main__":
    main()
