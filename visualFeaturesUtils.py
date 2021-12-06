import cv2
import math
from collections import namedtuple
import numpy as np

ColorMoments = namedtuple('ColorMoments', ['mean', 'stdDeviation', 'skewness'])
def getEntropy(histogram, totalPixels):
    entropy = 0
    for pixels in histogram:
        if pixels != 0:
            proportion = float(pixels / totalPixels)
            entropy -= proportion * math.log(proportion, 2)
    return entropy

def getColorMoments(histogram, totalPixels):
    sumPixels = 0
    sumPixelsSquares = 0
    sumPixelsCubes = 0
    for pixels in histogram:
            sumPixels += pixels
    colorMean = float(sumPixels / totalPixels)

    for pixels in histogram:
        sumPixelsCubes += math.pow(pixels - colorMean, 3)
        sumPixelsSquares += math.pow(pixels - colorMean, 2)

    variance = float(sumPixelsSquares / totalPixels)
    stdDeviation = math.sqrt(variance)
    avgSumOfCubes = float(sumPixelsCubes / totalPixels)
    skewness = float(avgSumOfCubes ** (1. / 3.))
    return ColorMoments(colorMean, stdDeviation, skewness)

def getEuclideanDistance(currentColorMoments, previousColorMoments):
    distance = math.pow(currentColorMoments.mean - previousColorMoments.mean, 2) + math.pow(
        currentColorMoments.stdDeviation - previousColorMoments.stdDeviation, 2) + math.pow(
        currentColorMoments.skewness - previousColorMoments.skewness, 2)
    return distance

def getRegionOfInterest(image):
    lower = np.array([30, 30, 30])
    higher = np.array([250, 250, 250])
    mask = cv2.inRange(image, lower, higher)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(image, contours, -1, 255, 3)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, h, w = cv2.boundingRect(c)
        image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        image = image[y:y + h, x:x + w]

    #cv2.imshow('Whiteboard', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return image

def preprocess(img):
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny=cv2.Canny(imgBlur,200,200)
    kernel=np.ones((5,5))
    imgDial=cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres=cv2.erode(imgDial,kernel,iterations=1)
    return imgThres