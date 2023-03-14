import sys
sys.path.append('C:/Users/mohor/Documents/1_PROJEKTI/Lite6Magneti')
import robotDriver as rd
from parameters import *
import pandas as pd
import time
from loadPoints import *
import stepperSerial

STEVILO_OHISIJ_Y = 2
STEVILO_OHISIJ_X = 5
OHISJE_OFFSET_X = 26
OHISJE_OFFSET_Y = -18

SPEED_FACTOR = 1.5
SPEED_VERY_SLOW = SPEED_VERY_SLOW*SPEED_FACTOR
SPEED_SLOW = SPEED_SLOW*SPEED_FACTOR
SPEED_MIDDLE = SPEED_MIDDLE*SPEED_FACTOR
SPEED_FAST = SPEED_FAST*SPEED_FACTOR
SPEED_VERY_FAST = SPEED_VERY_FAST*SPEED_FACTOR
SPEED_VERY_VERY_FAST = SPEED_VERY_VERY_FAST*SPEED_FACTOR

def readPoints():
    # read csv file
    with open(POINTS_PATH, 'r') as f:
        points = pd.read_csv(f)

    return points

def main():
    robot = rd.Robot(ROBOT_IP)
    stepper = stepperSerial.StepperSerial()
    pallet = rd.Pallet("4x4", points["pallet1.1"], points["pallet1.2"],
                      points["pallet1.3"], points["pallet1.4"], 4, 4)

    # print point with name "start"

    robot.gripperClose()
    time.sleep(1)
    #robot.moveJ(pose = tuple(points[points['name'] == 'start'].values[0][1:]), speed=SPEED_MIDDLE, wait=True)
    robot.moveJ(pose = points['nadMagnetom3'].pose(), pointType=points['nadMagnetom3'].pointType(), speed=50, wait=True)
    robot.gripperOpen()
    
    for i in range(STEVILO_OHISIJ_Y):
      odloziMagnet = points['odloziMagnet'].pose()
      odloziMagnet[1] = odloziMagnet[1] + OHISJE_OFFSET_Y*i
      for i in range(STEVILO_OHISIJ_X):
        start = time.time()
        ###############################
        # start counting time
        # move to start    
        #robot.moveJ(pose = tuple(points[points['name'] == 'start'].values[0][1:]), speed=SPEED_VERY_VERY_FAST, radius=250, wait=False)
        # move to ohisje
        
        robot.moveL(pose = points['nadOhisjeRel'].pose(), relative=True, speed=SPEED_VERY_FAST, radius=2, wait=False)
        robot.moveJ(pose = points['nadMagnetom3'].pose(), pointType=points['nadMagnetom3'].pointType(), speed=SPEED_VERY_VERY_FAST, radius=50, wait=False)
        robot.moveJ(pose = points["nadOhisjem"].pose(), pointType=points["nadOhisjem"].pointType(), speed=SPEED_VERY_VERY_FAST, radius=3, wait=False)
        robot.moveL(pose=points["prijemOhisja"].pose(), speed=SPEED_SLOW, wait=True)
        robot.gripperClose()
        time.sleep(0.1)
        robot.moveL(pose=points['pritisneOhisje'].pose(), relative=True, speed=SPEED_SLOW, wait=True)
        robot.moveL(pose=points['nadOhisjem2'].pose(), relative=True, speed=SPEED_MIDDLE, radius=1, wait=False)
        robot.moveL(pose=points['doLepila1'].pose(), relative=True, speed=SPEED_FAST, radius=1, wait=False)
        robot.moveL(pose=points['nanesiLepilo'].pose(), relative=True, speed=5, wait=True)

        time.sleep(0.1)
        robot.moveL(pose=points['podLepilom2'].pose(), relative=True, speed=SPEED_FAST, radius=4, wait=False)

        # magnet
      
        #robot.pallet(pallet=pallet, robot=robot, speedFactor=SPEED_FACTOR)
        
        #robot.moveJ(pose = points['nadKovinskoPlosco'].pose(), pointType=points['nadKovinskoPlosco'].pointType() , speed=SPEED_VERY_VERY_FAST, radius=150, wait=False)
        stepper.send()
        odloziMagnet[0] = odloziMagnet[0] + OHISJE_OFFSET_X
        print(odloziMagnet)
        robot.moveJ(pose = odloziMagnet, pointType=points['odloziMagnet'].pointType(), speed=SPEED_VERY_FAST, radius=2, wait=False)
        robot.moveL(pose = points['odloziMagnetRel'].pose(), relative=True, speed=SPEED_MIDDLE, wait=True)
        robot.moveL(pose = points['nadOdlozenMagnetRel'].pose(), relative=True, speed=SPEED_FAST, wait=False)
        robot.moveL(pose = points['ohisjeNadMagKot'].pose(), relative=True, speed=SPEED_MIDDLE, wait=False)
        robot.moveL(pose = points['ohisjeNadMagnetRel'].pose(), relative=True, speed=SPEED_MIDDLE, wait=True)
        robot.moveL(pose = points['poloziOhisjeRel'].pose(), relative=True, speed=SPEED_SLOW, wait=True)
        robot.moveJ(pose = points['poloziOhisjeRot'].pose(), pointType=points['poloziOhisjeRot'].pointType(), relative=True, speed=SPEED_VERY_FAST, wait=True)
        robot.gripperOpen()
        time.sleep(0.1)

        # calculate time
        end = time.time()
        print("Time: ", end - start)
      


    for i in range(STEVILO_OHISIJ_Y):
      odloziMagnet = points['odloziMagnet'].pose()
      odloziMagnet[1] = odloziMagnet[1] + OHISJE_OFFSET_Y*i
      for i in range(STEVILO_OHISIJ_X):
        start = time.time()
        odloziMagnet[0] = odloziMagnet[0] + OHISJE_OFFSET_X

    robot.moveJ(pose = points['nadMagnetom3'].pose(), pointType=points['nadMagnetom3'].pointType(), speed=50, wait=True)
    

def pallet():
    robot = rd.Robot(ROBOT_IP)

    pallet = rd.Pallet("4x4", points["pallet1.4"], points["pallet1.3"],
                       points["pallet1.2"], points["pallet1.1"], 4, 4)
    robot.pallet(pallet=pallet, robot=robot, speedFactor=SPEED_FACTOR)

if __name__ == "__main__":
    main()
    #pallet()