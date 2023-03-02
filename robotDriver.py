"""
Skripta, ki vsebuje robotski cikel. Skrbi za premikanje robota preko XArm API-ja

PREDPRIPRAVA:
- [ ] Robot zažene zaznavo objektov
- [ ] Robot resetira svoje errorje in postavi na "ZERO" position

CIKEL:
- [ ] Robot se umakne na "home" pozicijo
- [ ] Robot prebere koordinate objektov, če ni nobenega, čez 5 sekund poskusi znova
- [ ] Robot vsak objekt pobere in spusti na predoločenem mestu
"""

import time
import numpy as np
import logging

from parameters import *

from xarm.wrapper import XArmAPI


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
        Če želimo uporabiti že shranjene skalibrirane world coordinate izberi worldCoordRobot class
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

    def moveJ(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None, pose=None, speed=None,
              wait=True, radius=0, is_radian=False):
        '''
        Move robot to position in joint motion
        
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :param roll: roll angle
        :param pitch: pitch angle
        :param yaw: yaw angle
        :param pose: list of x, y, z, roll, pitch, yaw (alternative to separate parameters)
        :param speed: speed of motion
        :param wait: if True, wait for motion to complete
        :param is_radian: if True, angles are in radians
        :return: None
        '''
        self.currentPosition = self.robot.get_position()
        if pose == None:
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
        else:
            pose = pose

        code, pose = self.robot.get_inverse_kinematics(pose, input_is_radian=is_radian, return_is_radian=False)
        self.robot.set_servo_angle(angle=pose, speed=speed, wait=wait, radius=radius, is_radian=False)

    def moveJoint(self, joint1=None, joint2=None, joint3=None, joint4=None, joint5=None, joint6=None,
                  speed=None, pose=None, wait=True, radius=0, is_radian=False):
        '''
        Move robot to position with joint angles
        
        :param joint1: joint 1 angle
        :param joint2: joint 2 angle
        :param joint3: joint 3 angle
        :param joint4: joint 4 angle
        :param joint5: joint 5 angle
        :param joint6: joint 6 angle
        :param pose: list of joint angles (alternative to separate parameters)
        :param speed: speed of motion
        :param wait: if True, wait for motion to complete
        :param radius: radius of circular motion
        :param is_radian: if True, angles are in radians
        :return: None
        '''
        if pose == None:
            pose = [joint1, joint2, joint3, joint4, joint5, joint6]

        self.robot.set_servo_angle(angle=pose, speed=speed, wait=wait, radius=radius, is_radian=is_radian)

    def pallet(self):
        self.setWorldOffset([268.989075, 108.34774, -10.139146, -
                            178.883382, 0.323492, 1.800291], is_radian=False)

        indexX = self.counter % 4
        indexY = self.counter // 4
        width = 75.2957723090656 / 3
        height = 74.3286143020664 / 3
        self.moveJ(x=width * indexX, y=height * indexY, z=0, roll=0,
                   pitch=0, yaw=0, speed=SPEED_FAST, wait=True)

        self.counter += 1
        self.setWorldOffset([0, 0, 0, 0, 0, 0], is_radian=False)