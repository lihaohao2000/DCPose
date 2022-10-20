import numpy as np
import math


truckDetectionCal = [[40,40,40],[40,40,40]]
truckDetectionFlag = 0

disshankleCal = [0.18,0.18,0.18]
disshankleFlag = 0

def init():
  truckDetectionCal = [[40,40,40],[40,40,40]]
  truckDetectionFlag = 0

  disshankleCal = [0.18,0.18,0.18]
  disshankleFlag = 0

def truckDetection(new_coord):
    global truckDetectionCal, truckDetectionFlag
    v1 = [new_coord[0][0],new_coord[0][1],new_coord[1][0],new_coord[1][1]]
    v2 = [new_coord[1][0],new_coord[1][1],new_coord[2][0],new_coord[2][1]]
    v3 = [new_coord[5][0],new_coord[5][1],new_coord[4][0],new_coord[4][1]]
    v4 = [new_coord[4][0],new_coord[4][1],new_coord[3][0],new_coord[3][1]]
    rightAngle = angle(v1,v2)
    leftAngle = angle(v3,v4)
    # if new_coord[12][0] < new_coord[2][0]:#left
    #     averageAngle = leftAngle
    # else:#right
    #     averageAngle = rightAngle
    averageAngle = (leftAngle + rightAngle) / 2

    truckDetectionCal[0][truckDetectionFlag % 3] = averageAngle
    ave_knee = np.mean(truckDetectionCal[0])

    v1 = [new_coord[0][0],new_coord[0][1],new_coord[2][0],new_coord[2][1]]
    v2 = [new_coord[2][0],new_coord[2][1],new_coord[8][0],new_coord[8][1]]
    v3 = [new_coord[5][0],new_coord[5][1],new_coord[3][0],new_coord[3][1]]
    v4 = [new_coord[3][0],new_coord[3][1],new_coord[9][0],new_coord[9][1]]
    rightAngle = angle(v1,v2)
    leftAngle = angle(v3,v4)
    # if new_coord[12][0] < new_coord[2][0]:#left
    #     averageAngle = leftAngle
    # else:#right
    #     averageAngle = rightAngle
    averageAngle = (leftAngle + rightAngle) / 2

    truckDetectionCal[1][truckDetectionFlag % 3] = averageAngle
    truckDetectionFlag = truckDetectionFlag + 1
    if(truckDetectionFlag >= 3):
        truckDetectionFlag = 0
    ave_hip = np.mean(truckDetectionCal[1])

    if ave_knee <= 40 and ave_hip <= 40:
      return True
    return False


def shankleDetection(new_coord):
  global disshankleCal, disshankleFlag
  sh = distance(new_coord[8][0],new_coord[8][1],new_coord[9][0],new_coord[9][1])
  L_shankle = distance(new_coord[5][0],new_coord[5][1],new_coord[9][0],new_coord[9][1])
  R_shankle = distance(new_coord[8][0],new_coord[8][1],new_coord[0][0],new_coord[0][1])
  ave_shankle = (L_shankle + R_shankle) / 2
  shankle = sh / ave_shankle
  disshankleCal[disshankleFlag % 3] = shankle
  disshankleFlag = disshankleFlag + 1
  if(disshankleFlag >= 3):
      disshankleFlag = 0
  ave = np.mean(disshankleCal)

  if ave <= 0.1:
    return True
  return False


    
def angle(v1, v2):
  dx1 = v1[2] - v1[0]
  dy1 = v1[3] - v1[1]
  dx2 = v2[2] - v2[0]
  dy2 = v2[3] - v2[1]
  angle1 = math.atan2(dy1, dx1)
  angle1 = int(angle1 * 180/math.pi)
  # print(angle1)
  angle2 = math.atan2(dy2, dx2)
  angle2 = int(angle2 * 180/math.pi)
  # print(angle2)
  if angle1*angle2 >= 0:
    included_angle = abs(angle1-angle2)
  else:
    included_angle = abs(angle1) + abs(angle2)
    if included_angle > 180:
      included_angle = 360 - included_angle
  return included_angle


def distance(x1, y1, x2, y2):
  x = x1 - x2
  y = y1 - y2
  len = math.sqrt((x**2)+(y**2))
  return len