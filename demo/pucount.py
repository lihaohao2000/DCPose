import numpy as np
import math

def pullUpCount(new_coord,pullUpsCal,pullUpsFLAG,pullUpState):
    v1 = [new_coord[7][0],new_coord[7][1],new_coord[6][0],new_coord[6][1]]
    v2 = [new_coord[7][0],new_coord[7][1],new_coord[8][0],new_coord[8][1]]
    v3 = [new_coord[10][0],new_coord[10][1],new_coord[9][0],new_coord[9][1]]
    v4 = [new_coord[10][0],new_coord[10][1],new_coord[11][0],new_coord[11][1]]
    rightAngle = angle(v1,v2)
    leftAngle = angle(v3,v4)
    averageAngle = (leftAngle + rightAngle) / 2
    # print("rightAngle:")
    # print(rightAngle)
    # print("leftAngle:")
    # print(leftAngle)
    # print("averageAngle:")
    # print(averageAngle)
    pullUpsCal[pullUpsFLAG % 3] = averageAngle
    pullUpsFLAG = pullUpsFLAG + 1
    if(pullUpsFLAG >= 3):
        pullUpsFLAG = 0
    ave = np.mean(pullUpsCal)
    # print("real:")
    # print(ave)
    if(pullUpState == 1 and ave <= 100):
        pullUpState = 0
        return 1
    if(pullUpState == 0 and ave >= 150):
        pullUpState = 1
    return 0


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

