import os
from parameters import *
import pandas as pd
import robotDriver as rd

columns = ['name', 'x', 'y', 'z', 'roll', 'pitch', 'yaw', 'comment']

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
    if pointName not in points['name'].values:
      chose = input("1 - save coordinated, 2 - save joint angles, q - quit: ")
      # check if user input q
      if chose == 'q' or pointName == 'q':
        print("Closing program...")
        break

      elif chose == '1':
        # read current position of robot
        currentPosition = robot.getPosition()

        # save point to dataFrame with concat function
        points = pd.concat([points, pd.DataFrame([[pointName, currentPosition[0], currentPosition[1],
                                                  currentPosition[2], currentPosition[3], currentPosition[4],
                                                  currentPosition[5], 'coordinate']], columns=columns)], ignore_index=True)
    
      elif chose == '2':
        # read current position of robot
        currentJoints = robot.getJoints()

        # save point to dataFrame with concat function
        points = pd.concat([points, pd.DataFrame([[pointName, currentJoints[0], currentJoints[1],
                                                  currentJoints[2], currentJoints[3], currentJoints[4],
                                                  currentJoints[5], 'angle']], columns=columns)], ignore_index=True) 
      
    else:
      print("Point with this name already exists!")
      continue
    
        
  # save dataFrame to csv file
  points.to_csv(POINTS_PATH, index=False)

else:
  # make empty dataFrame
  points = pd.DataFrame(columns=columns)
  # make csf file from dataFrame
  points.to_csv(POINTS_PATH, index=False)