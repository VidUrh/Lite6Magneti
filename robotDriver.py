"""
Skripta, ki vsebuje robotski cikel. Skrbi za premikanje robota preko XArm API-ja

PREDPRIPRAVA:
- [ ] Robot zazene zaznavo objektov
- [ ] Robot resetira svoje errorje in postavi na "ZERO" position

CIKEL:
- [ ] Robot se umakne na "home" pozicijo
- [ ] Robot prebere koordinate objektov, ce ni nobenega, cez 5 sekund poskusi znova
- [ ] Robot vsak objekt pobere in spusti na predolocenem mestu
"""

from commonUtils import *
from loadPoints import *
from pprint import pprint
import time
import numpy as np
import logging

from parameters import *

from xarm.wrapper import XArmAPI


"""
    This script contains the Pallet class, which is used to replicate the palletizing solution
    used in UR robots.
    The pallet is defined by four corners and the number of rows and columns and its name.
    It contains methods for movements relative to current element of the pallet.
    It contains the counter variable which stores the current element. At the beginning it is set to 0.
    At the end of each palletizing movement, the counter is incremented by 1 (moving to next element).
"""


class Pallet:
    def __init__(self, name: str, topleft: Point, topright: Point, bottomright: Point, bottomleft: Point,  rows: int, columns: int):
        self.name = name
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = topleft, topright, bottomleft, bottomright
        self.corners = [topleft, topright, bottomleft, bottomright]
        self.counter = 0
        self.rows = rows
        self.columns = columns

        self.offsetX = 2.15
        self.offsetY = 8.3
        self.offsetZ = -0.1

        self.localPositions = []
        self.rotation = self.getRotation()
        self.width = getDistance(self.topLeft, self.topRight)
        self.height = getDistance(self.topLeft, self.bottomLeft)
        self.localPositions = self.calculateLocalPositions(
            self.width, self.height)

        self.worldOffset = [-topleft.x, topleft.y,
                            topleft.z + self.offsetZ, 180, 0, self.rotation]

    def calculateLocalPositions(self, width, height):
        """Function that calculates the local positions of the pallet elements by dividing the pallet into rows and columns.

        Args:
            width (float): the width of the pallet
            height (float): the height of the pallet

        Returns:
            localPositions (list): a list of local positions of the pallet elements
        """
        # calculate the local positions of the elements
        localPositions = []
        for i in range(self.rows):
            for j in range(self.columns):
                localPositions.append(
                    Point("temp",
                          j*width/(self.rows-1) + self.offsetX,
                          -i*height/(self.columns-1) + self.offsetY,
                          0,
                          0,
                          0,
                          0
                          )
                )
        return localPositions

    def getRotation(self):
        """
            Function that returns the rotation of the pallet, calculated from its corners.
        """
        return getAngle(self.topLeft, self.topRight)


class Robot:
    def __init__(self, ip, coordOffset=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Connecting to robot...")
        self.robot = XArmAPI(ip)
        self.robot.clean_error()
        self.robot.motion_enable(enable=True)
        self.robot.set_mode(0)
        self.robot.set_state(state=0)
        self.logger.info("Robot connected!")
        self.coordOffset = coordOffset
        self.counter = 0

        if coordOffset != None:
            self.setWorldOffset(coordOffset)

    # move roboto set default parameters
    def move(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None, speed=SPEED_MIDDLE, mvacc=None, wait=True, timeout=0):
        self.robot.set_position(
            x, y, z, roll, pitch, yaw, speed=speed, mvacc=mvacc, wait=wait, timeout=timeout)

    def pick(self):
        self.robot.open_lite6_gripper()
        time.sleep(1)

    def drop(self):
        self.robot.close_lite6_gripper()

    def gripperClose(self):
        self.robot.close_lite6_gripper()

    def gripperOpen(self):
        self.robot.open_lite6_gripper()

    def home(self):
        self.robot.move_gohome(wait=True)

    def move_todrop(self):
        self.robot.set_servo_angle(
            angle=[-122, 24, 58.9, -9.7, 32.9, -66.9], speed=SPEED_VERY_FAST, acceleration=5, is_radian=False, wait=True)

    def close(self):
        self.robot.disconnect()

    def standby(self):
        self.robot.set_servo_angle(
            angle=[-90, 0, 90, 0.0, 90, 0], speed=SPEED_SLOW, acceleration=5, is_radian=False, wait=True)

    def getPosition(self):
        return self.robot.get_position()[1]

    def getJoints(self):
        return self.robot.get_servo_angle()[1]

    def set_position(self, x, y, z, speed, relative=False, wait=True):
        self.robot.set_position(
            x=x, y=y, z=z, speed=speed, relative=relative, wait=wait)

    def calibrateUserOrientationOffset(self, points, mode=0, trust_ind=0, input_is_radian=False, return_is_radian=False):
        return self.robot.calibrate_user_orientation_offset(points, mode, trust_ind, input_is_radian, return_is_radian)

    def setState(self, state=0):
        self.robot.set_state(state)

    def getState(self):
        return self.robot.get_state()

    def getIsMoving(self):
        return self.robot.get_is_moving()

    def setWorldOffset(self, offset=None, is_radian=False):
        '''
        ce zelimo uporabiti ze shranjene skalibrirane world coordinate izberi worldCoordRobot class
        in potem nekje v kodi naredi:
        setWorldOffset()

        Dobro je dodati nekaj deleje za to nastavitvijo preden premaknemo robota.
        '''
        if offset == None:
            offset = self.coordOffset

        ret = self.robot.set_world_offset(offset, is_radian)
        self.setState(0)

    def stop(self):
        self.setState(4)

    def moveL(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None, pose=None, speed=None,
              relative=False, wait=True, radius=0, is_radian=False):
        '''
        Move robot to position in linear motion

        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :param roll: roll angle
        :param pitch: pitch angle
        :param yaw: yaw angle
        :param pose: list of x, y, z, roll, pitch, yaw (alternative to separate parameters)
        :param speed: speed of motion
        :param relative: if True, move relative to current position
        :param wait: if True, wait for motion to complete
        :param is_radian: if True, angles are in radians
        :return: None
        '''
        if pose != None:
            x, y, z, roll, pitch, yaw = pose

        self.robot.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, speed=speed,
                                relative=relative, radius=radius, wait=wait, mv_cmd=1)

    def moveJ(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None, pose=None, pointType=None, 
              speed=None, wait=True, radius=0, is_radian=False):
        '''
        Move robot to position in joint motion

        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :param roll: roll angle
        :param pitch: pitch angle
        :param yaw: yaw angle
        :param pose: list of x, y, z, roll, pitch, yaw, (pointType) (alternative to separate parameters)
        :param pointType: 'coordinate' or 'angle' (angle if point is store in joint angles)
        :param speed: speed of motion
        :param wait: if True, wait for motion to complete
        :param is_radian: if True, angles are in radians
        :return: None
        '''

        if len(pose) == 7:
            # get pointType from pose
            pointType = pose[6]
            
            # remove pointType from pose
            pose = pose[:6]

        if pointType == 'coordinate':
            if pose == None:
                self.currentPosition = self.robot.get_position()
                # check if any of the parameters are None and set them to current position
                if x == None:
                    x = self.currentPosition[1][0]
                if y == None:
                    y = self.currentPosition[1][1]
                if z == None:
                    z = self.currentPosition[1][2]
                if roll == None:
                    roll  = self.currentPosition[1][3]
                if pitch == None:
                    pitch = self.currentPosition[1][4]
                if yaw == None:
                    yaw   = self.currentPosition[1][5]

                pose = [x, y, z, roll, pitch, yaw]

            code, pose = self.robot.get_inverse_kinematics(pose, input_is_radian=is_radian, return_is_radian=False)
            self.robot.set_servo_angle(angle=pose, speed=speed, wait=wait, radius=radius, is_radian=False)

        elif pointType == 'angle':
            if pose != None:
                self.robot.set_servo_angle(angle=pose , speed=speed, wait=wait, radius=radius, is_radian=False)
        else:
            raise Exception('Wrong point type')

    def moveJoint(self, joint1=None, joint2=None, joint3=None, joint4=None, joint5=None, joint6=None,
                  speed=None, pose=None, pointType=None, wait=True, radius=0, is_radian=False):
        '''
        Move robot to position with joint angles

        :param joint1: joint 1 angle
        :param joint2: joint 2 angle
        :param joint3: joint 3 angle
        :param joint4: joint 4 angle
        :param joint5: joint 5 angle
        :param joint6: joint 6 angle
        :param pose: list of joint angles (alternative to separate parameters)
        :param pointType: 'coordinate' or 'angle' (angle if point is store in joint angles)
        :param speed: speed of motion
        :param wait: if True, wait for motion to complete
        :param radius: radius of circular motion
        :param is_radian: if True, angles are in radians
        :return: None
        '''
        if pointType == 'angle':
            if pose == None:
                pose = [joint1, joint2, joint3, joint4, joint5, joint6]

            self.robot.set_servo_angle(angle=pose, speed=speed, wait=wait, radius=radius, is_radian=is_radian)
        else:
            raise Exception('Wrong point type')

    def pallet(self, pallet, robot, index=None):
        self.setWorldOffset(pallet.worldOffset, is_radian=False)

        if index == None:
            index = pallet.counter

        position = pallet.localPositions[index].pose()
        position[2] -= 10

        robot.moveJ(pose=position, speed=SPEED_VERY_VERY_FAST, wait=True)
        robot.moveL(z=10, relative=True, speed=SPEED_SLOW, wait=True)
        robot.gripperOpen()
        robot.moveL(z=-10, relative=True, speed=SPEED_SLOW, wait=True)
        
        self.robot.set_servo_angle(
            angle=pose, speed=speed, wait=wait, radius=radius, is_radian=is_radian)

    def pallet(self, pallet, robot, index=None):
        self.setWorldOffset(pallet.worldOffset, is_radian=False)

        if index == None:
            index = pallet.counter

        position = pallet.localPositions[index].pose()
        position[2] -= 10

        robot.moveJ(pose=position, speed=SPEED_VERY_VERY_FAST, wait=True)
        robot.moveL(z=10, relative=True, speed=SPEED_SLOW, wait=True)
        robot.gripperOpen()
        robot.moveL(z=-10, relative=True, speed=SPEED_SLOW, wait=True)

        pallet.counter += 1
        self.setWorldOffset([0, 0, 0, 0, 0, 0], is_radian=False)


if __name__ == '__main__':
    robot = Robot(ROBOT_IP)

    robot.moveJ(pose=points["start"].pose(), speed=SPEED_MIDDLE, wait=True)
