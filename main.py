import robotDriver as rd
from parameters import *
import pandas as pd
import time

STEVILO_OHISIJ = 4

def readPoints():
    # read csv file
    with open(POINTS_PATH, 'r') as f:
        points = pd.read_csv(f)

    return points

def main():
    robot = rd.Robot(ROBOT_IP)

    points = readPoints()

    # print point with name "start"
    startPoint = points[points['name'] == 'start']

    # save start point to tuple
    startPoint = tuple(startPoint.values[0][1:])
    print(print(startPoint))
    robot.moveJ(pose = tuple(points[points['name'] == 'start'].values[0][1:]), speed=SPEED_MIDDLE, wait=True)
      

    for i in range(STEVILO_OHISIJ):
      ###############################
      # start counting time
      # move to start    
      robot.gripperOpen()
      start = time.time()
      robot.moveJ(pose = tuple(points[points['name'] == 'start'].values[0][1:]), speed=SPEED_VERY_VERY_FAST, radius=250, wait=False)
      time.sleep(0.2)
      # move to ohisje
      robot.moveJ(pose = tuple(points[points['name'] == 'nadOhisjem'].values[0][1:]), speed=SPEED_VERY_VERY_FAST, wait=True)
      robot.moveL(pose = tuple(points[points['name'] == 'prijemOhisja'].values[0][1:]), speed=SPEED_FAST, wait=True)
      robot.gripperClose()
      time.sleep(0.1)
      robot.moveL(pose = tuple(points[points['name'] == 'pritisneOhisje'].values[0][1:]), speed=SPEED_SLOW, wait=True)
      robot.moveL(pose = tuple(points[points['name'] == 'nadOhisjem2'].values[0][1:]), speed=SPEED_MIDDLE, radius=20, wait=False)

      # move to lepljenje
      robot.moveJoint(pose = tuple(points[points['name'] == 'doLepila1.1'].values[0][1:]), speed=SPEED_FAST, radius=40, wait=False)
      #robot.moveJ(pose = tuple(points[points['name'] == 'doLepila1.1'].values[0][1:]), speed=SPEED_VERY_SLOW, radius=25, wait=False)
      robot.moveJ(pose = tuple(points[points['name'] == 'doLepila2'].values[0][1:]), speed=SPEED_FAST, radius=60, wait=False)
      robot.moveJoint(pose = tuple(points[points['name'] == 'podLepilom'].values[0][1:]), speed=SPEED_VERY_FAST, wait=True)

      robot.moveL(pose = tuple(points[points['name'] == 'nanesiLepilo'].values[0][1:]), speed=10, wait=True)
      time.sleep(0.1)
      robot.moveL(pose = tuple(points[points['name'] == 'podLepilom2'].values[0][1:]), speed=SPEED_MIDDLE, wait=True)

      # magnet
      robot.moveJoint(pose = tuple(points[points['name'] == 'nadMagnetom'].values[0][1:]), speed=180, wait=True)
      robot.moveL(pose = tuple(points[points['name'] == 'magnet'].values[0][1:]), speed=SPEED_SLOW, wait=True)
      robot.gripperOpen()
      time.sleep(0.1)
      robot.moveL(pose = tuple(points[points['name'] == 'nadMagnetom2'].values[0][1:]), speed=SPEED_VERY_FAST, radius=5, wait=False)
      time.sleep(0.1)

      # calculate time
      end = time.time()
      print("Time: ", end - start)

if __name__ == "__main__":
    main()