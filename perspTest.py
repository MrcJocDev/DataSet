import cv2 #type:ignore
import numpy as np #type:ignore

from use import gauge_coords

img = cv2.imread('2.jpg')

def getImageInfo():
    shapeInfo = img.shape
    w = img.shape[0]
    h = img.shape[1]
    
    return w, h

def getThetaRads():
    """Calculate theta"""
        
    gCoords = gauge_coords
    x1, y1, x2, y2 = gCoords
    
    dx = x2 - x1 
    dy = y2 - y1
    theta_radians = np.arctan2(dy, dx)
    theta_degrees = np.degrees(theta_radians)
    
    return theta_radians

def getACDist():
    
    gCoords = gauge_coords
    x1, y1, x2, y2 = gCoords
    
    """Calculate Diagonal Distance"""
    aC = np.sqrt((x1-x2)^2 + (y1-y2)^2)
    return aC

def getCosTheta():
    gCoords = gauge_coords
    x1, y1, x2, y2 = gCoords

    blbr = np.cos(getThetaRads) * getACDist()
        

imgArr = getImageInfo()
imgW = imgArr[0]
imgH = imgArr[1]

theta_degress = getThetaRads()
aCDist = getACDist()


tl = [37, 36]
bl = [35, 154]
tr = [140, 42]
br = [139, 153]

cv2.circle(img, tl, 5, (0,0,255), -1)
cv2.circle(img, bl, 5, (0,0,255), -1)
cv2.circle(img, tr, 5, (0,0,255), -1)
cv2.circle(img, br, 5, (0,0,255), -1)

# Apply Geometrical Transformation 
pts1 = np.float32([tl, bl, tr, br])
pts2 = np.float32([[0, 0], [0, imgW], [imgH, 0], [imgH, imgW]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
transformed_image = cv2.warpPerspective(img, matrix, (241, 244))

print(dxPT, dyPT, theta_degress)
cv2.imshow("ORIGNAL", img)
cv2.imshow("FIXED", transformed_image)
cv2.waitKey(0)
