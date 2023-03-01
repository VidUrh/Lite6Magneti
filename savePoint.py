import os
from parameters import *
import pandas as pd
import robotDriver as rd

# check if csv file with points exists
if os.path.isfile(POINTS_PATH):
  # read csv file with points
  points = pd.read_csv(POINTS_PATH)
  print(points)

  # init robot
  robot = rd.Robot(ROBOT_IP)

  # wait for user to input name of point
  while True:
    pointName = input("Name of point: ")
    # check if user input q
    if pointName == 'q':
      print("Closing program...")
      break

    else:
      if pointName not in points['point name'].values:
        
        # read current position of robot
        currentPosition = robot.getPosition()

        # save point to dataFrame with concat function
        points = pd.concat([points, pd.DataFrame([[pointName, currentPosition[0], currentPosition[1], currentPosition[2], currentPosition[3], currentPosition[4], currentPosition[5]]], columns=['point name', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'])], ignore_index=True)

      else:
        print("Point with this name already exists!")
        continue
        
  # save dataFrame to csv file
  points.to_csv(POINTS_PATH, index=False)

else:
  # make empty dataFrame
  points = pd.DataFrame(columns=['name', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'])
  # make csf file from dataFrame
  points.to_csv(POINTS_PATH, index=False)
    