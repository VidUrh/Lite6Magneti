import robotDriver as rd
from parameters import *
import pandas as pd
import time
from loadPoints import *

STEVILO_OHISIJ = 7


def main():
    robot = rd.Robot(ROBOT_IP)

    pallet = rd.Pallet("4x4", points["pallet1.1"], points["pallet1.2"],
                       points["pallet1.3"], points["pallet1.4"], 4, 4)

    # print point with name "start"
    startPoint = points['start'].pose()

    # save start point to tuple
    startPoint = tuple(startPoint)

    robot.moveJ(pose=tuple(points["start"].pose()),
                speed=SPEED_MIDDLE, wait=True)

    for i in range(STEVILO_OHISIJ):
        ###############################
        # start counting time
        # move to start
        start = time.time()
        robot.gripperOpen()

        robot.moveJ(pose=tuple(points["start"].pose(
        )), speed=SPEED_VERY_VERY_FAST, radius=250, wait=False)

        time.sleep(0.2)
        # move to ohisje
        robot.moveJ(pose=tuple(points["nadOhisjem2"].pose()),
                    speed=SPEED_VERY_VERY_FAST, wait=True)

        robot.moveL(pose=tuple(
            points["prijemOhisja"].pose()), speed=SPEED_FAST, wait=True)
        robot.gripperClose()

        time.sleep(0.1)
        robot.moveL(pose=tuple(
            points["pritisneOhisje"].pose()), speed=SPEED_SLOW, wait=True)

        robot.moveL(pose=tuple(points["nadOhisjem2"].pose(
        )), speed=SPEED_MIDDLE, radius=20, wait=False)

        # move to lepljenje
        robot.moveJoint(pose=tuple(
            points["doLepila1.1"].pose()), speed=SPEED_FAST, radius=40, wait=False)
        # robot.moveJ(pose = tuple(points[points['name'] == 'doLepila1.1'].values[0][1:]), speed=SPEED_VERY_SLOW, radius=25, wait=False)
        robot.moveJ(pose=tuple(points["doLepila2"].pose()),
                    speed=SPEED_FAST, radius=60, wait=False)
        robot.moveJoint(pose=tuple(
            points["podLepilom"].pose()), speed=SPEED_VERY_FAST, wait=True)

        robot.moveL(pose=tuple(
            points["nanesiLepilo"].pose()), speed=10, wait=True)
        time.sleep(0.1)
        robot.moveL(pose=tuple(
            points["podLepilom2"].pose()), speed=SPEED_MIDDLE, wait=True)

        robot.moveJ(pose=tuple(
            points["nadMagneti"].pose()), speed=SPEED_VERY_VERY_FAST, radius=250, wait=False)

        robot.pallet(pallet=pallet, robot=robot)

        # calculate time
        end = time.time()
        print("Time: ", end - start)

    robot.moveJ(pose=tuple(
        points["start"].pose()), speed=SPEED_MIDDLE, wait=True)


if __name__ == "__main__":
    main()
