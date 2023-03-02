import os
from parameters import *
import pandas as pd

class pointHandler:
  def __init__(self):
    # variables
    self.columns = ['name', 'x', 'y', 'z', 'roll', 'pitch', 'yaw', 'type']

    # check if csv file with points exists
    if os.path.isfile(POINTS_PATH):
      # read csv file with points
      self.points = pd.read_csv(POINTS_PATH)
      print(self.points)

    else:
      # make empty dataFrame
      self.points = pd.DataFrame(columns=self.columns)
      # make csf file from dataFrame
      self.points.to_csv(POINTS_PATH, index=False)


  def addPoint(self, pointName, pointType, pointPosition):
    # check if point with this name already exists
    if pointName not in self.points['name'].values:
      # save point to dataFrame with concat function
      self.points = pd.concat([self.points, pd.DataFrame([
                              [pointName, pointPosition[0], pointPosition[1], pointPosition[2], 
                               pointPosition[3], pointPosition[4], pointPosition[5], pointType]],
                               columns=self.columns)], ignore_index=True)

      print("Point added!")
      
    else:
      print("Point with this name already exists!")
      return False
    
  def editPoint(self, pointName, pointType, pointPosition):
    # check if point with this name already exists
    if pointName in self.points['name'].values:
      # save point to dataFrame with concat function
      self.points = pd.concat([self.points, pd.DataFrame([
                              [pointName, pointPosition[0], pointPosition[1], pointPosition[2], 
                               pointPosition[3], pointPosition[4], pointPosition[5], pointType]],
                               columns=self.columns)], ignore_index=True)
      
    else:
      print("Point with this name doesn't exist!")
      return False
    
  def deletePoint(self, pointName):
    # check if point with this name already exists
    if pointName in self.points['name'].values:
      # delete point from dataFrame
      self.points = self.points[self.points.name != pointName]

    else:
      print("Point with this name doesn't exist!")
      return False
    
  def __del__(self):
    # save dataFrame to csv file
    self.points.to_csv(POINTS_PATH, index=False)


if __name__ == "__main__":
  # init pointHandler
  point = pointHandler()

  # delete point
  point.deletePoint('start')

  # close pointHandler
  del point