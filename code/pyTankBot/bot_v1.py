#!/usr/bin/python

import json
import socket
import logging
import binascii
import struct
import argparse
import random
import bot_classes
import time
import math

class ServerMessageTypes(object):
    TEST = 0
    CREATETANK = 1
    DESPAWNTANK = 2
    FIRE = 3
    TOGGLEFORWARD = 4
    TOGGLEREVERSE = 5
    TOGGLELEFT = 6
    TOGGLERIGHT = 7
    TOGGLETURRETLEFT = 8
    TOGGLETURRETRIGHT = 9
    TURNTURRETTOHEADING = 10
    TURNTOHEADING = 11
    MOVEFORWARDDISTANCE = 12
    MOVEBACKWARSDISTANCE = 13
    STOPALL = 14
    STOPTURN = 15
    STOPMOVE = 16
    STOPTURRET = 17
    OBJECTUPDATE = 18
    HEALTHPICKUP = 19
    AMMOPICKUP = 20
    SNITCHPICKUP = 21
    DESTROYED = 22
    ENTEREDGOAL = 23
    KILL = 24
    SNITCHAPPEARED = 25
    GAMETIMEUPDATE = 26
    HITDETECTED = 27
    SUCCESSFULLHIT = 28

    strings = {
        TEST: "TEST",
        CREATETANK: "CREATETANK",
        DESPAWNTANK: "DESPAWNTANK",
        FIRE: "FIRE",
        TOGGLEFORWARD: "TOGGLEFORWARD",
        TOGGLEREVERSE: "TOGGLEREVERSE",
        TOGGLELEFT: "TOGGLELEFT",
        TOGGLERIGHT: "TOGGLERIGHT",
        TOGGLETURRETLEFT: "TOGGLETURRETLEFT",
        TOGGLETURRETRIGHT: "TOGGLETURRENTRIGHT",
        TURNTURRETTOHEADING: "TURNTURRETTOHEADING",
        TURNTOHEADING: "TURNTOHEADING",
        MOVEFORWARDDISTANCE: "MOVEFORWARDDISTANCE",
        MOVEBACKWARSDISTANCE: "MOVEBACKWARDSDISTANCE",
        STOPALL: "STOPALL",
        STOPTURN: "STOPTURN",
        STOPMOVE: "STOPMOVE",
        STOPTURRET: "STOPTURRET",
        OBJECTUPDATE: "OBJECTUPDATE",
        HEALTHPICKUP: "HEALTHPICKUP",
        AMMOPICKUP: "AMMOPICKUP",
        SNITCHPICKUP: "SNITCHPICKUP",
        DESTROYED: "DESTROYED",
        ENTEREDGOAL: "ENTEREDGOAL",
        KILL: "KILL",
        SNITCHAPPEARED: "SNITCHAPPEARED",
        GAMETIMEUPDATE: "GAMETIMEUPDATE",
        HITDETECTED: "HITDETECTED",
        SUCCESSFULLHIT: "SUCCESSFULLHIT"
    }

    def toString(self, id):
        if id in self.strings.keys():
            return self.strings[id]
        else:
            return "??UNKNOWN??"


class ServerComms(object):
    '''
    TCP comms handler

    Server protocol is simple:

    * 1st byte is the message type - see ServerMessageTypes
    * 2nd byte is the length in bytes of the payload (so max 255 byte payload)
    * 3rd byte onwards is the payload encoded in JSON
    '''
    ServerSocket = None
    MessageTypes = ServerMessageTypes()

    def __init__(self, hostname, port):
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.connect((hostname, port))

    def readMessage(self):
        '''
        Read a message from the server
        '''
        messageTypeRaw = self.ServerSocket.recv(1)
        messageLenRaw = self.ServerSocket.recv(1)
        messageType = struct.unpack('>B', messageTypeRaw)[0]
        messageLen = struct.unpack('>B', messageLenRaw)[0]

        if messageLen == 0:
            messageData = bytearray()
            messagePayload = {'messageType': messageType}
        else:
            messageData = self.ServerSocket.recv(messageLen)
            logging.debug("*** {}".format(messageData))
            messagePayload = json.loads(messageData.decode('utf-8'))
            messagePayload['messageType'] = messageType
        logging.debug('Turned message {} into type {} payload {}'.format(
            binascii.hexlify(messageData),
            self.MessageTypes.toString(messageType),
            messagePayload))
        return messagePayload

    def sendMessage(self, messageType=None, messagePayload=None):
        '''
        Send a message to the server
        '''
        message = bytearray()

        if messageType is not None:
            message.append(messageType)
        else:
            message.append(0)

        if messagePayload is not None:
            messageString = json.dumps(messagePayload)
            message.append(len(messageString))
            message.extend(str.encode(messageString))

        else:
            message.append(0)

        logging.debug('Turned message type {} payload {} into {}'.format(
            self.MessageTypes.toString(messageType),
            messagePayload,
            binascii.hexlify(message)))
        return self.ServerSocket.send(message)


# def fire(my_x, my_y, my_turret, enemy):
#     correction = enemy.get_heading() // 90  # so I get the quarter the enemy tank is moving towards
#     my_turning = my_turret // 90  # the quarter my tank is looking at
#     corrected_turret = my_turret + my_turning - correction
#     GameServer.sendMessage()
#     GameServer.sendMessage(ServerMessageTypes.FIRE)
#     return corrected_turret

def heading_to(x, y):
    heading = float(math.atan2((y - us.tank_Y), (x - us.tank_X)))  # returns heading in radians
    heading = float(math.degrees(heading))
    heading = math.fabs(heading - 360) % 360
    return heading

 # TODO snitch hunt
def hunt_for_snitch(self, my_x, my_y):
    '''
    Params: x,y coords of tank bot, snitch coords, snitch ID
    Params: x,y coords of tank bot, snitch coords
    if during scout the tank locates snitch it starts moving towards
    the snitch
    '''
    # get snitch heading
    snitch_heading = heading_to(snitch[0], snitch[1])
    #get distance to snitch
    snitch_heading_X = snitch[0] - my_x
    snitch_heading_Y = snitch[1] - my_y
    snitch_distance = math.sqrt((snitch_heading_X ** 2) + (snitch_heading_Y ** 2))
    # start moving towards snitch
    GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {'Amount': snitch_heading})
    GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {'Amount': snitch_distance})

def fire_at_closest():
    tank_dict = tank_dictionary
    table = []
    for id in tank_dict:
        if id != our_id:
            table.append([tank_dict[id].get_distance(us.tank_X, us.tank_Y), id])  # add to list the distance & id of each tank
    turn_to = min(table)
    heading_to = tank_dict[turn_to[1]].heading_to(us.tank_X, us.tank_Y) # this will return the heading of the closest tank

    # no we will correct heading_to so that I shoot just in front of the enemy tank
    # correction = tank_dict[turn_to[1]].get_heading() // 90  # so I get the quarter the enemy tank is moving towards
    # my_turning = us.tank_turret_heading // 90  # the quarter my tank is looking at
    # heading_to = us.tank_turret_heading + my_turning - correction # should shoot 1-3 degrees in front of the enemy tank
    print(table)
    GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {'Amount':heading_to})
    GameServer.sendMessage(ServerMessageTypes.STOPALL)
    time.sleep(0.05)
    GameServer.sendMessage(ServerMessageTypes.FIRE)

def run_to_goal():
    if tank_dictionary[our_id].get_hp() > 2:
        if us.tank_Y >= 0:
            GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {'Amount': heading_to(0,100)})
            GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
        else:
            GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {'Amount': heading_to(0,-100)})
            GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
        if us.tank_X < -100 or us.tank_X > 100:
            GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {'Amount': 180})
            GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)



def read_data():
    global tank_dictionary, pickup_dictionary, snitch, time_left
    message = GameServer.readMessage()
    if "Type" in message:
        if message["Id"] == our_id:
            tank_dictionary[our_id].update(message["X"], message["Y"], message["Heading"],
                                                   message["TurretHeading"], message["Health"], message["Ammo"])
        elif message["Type"] == "Snitch":
            snitch = [message["X"], message["Y"]]
        elif message["Type"] == "Tank":
            if message["Id"] not in tank_dictionary:
                tank_dictionary[message["Id"]] = tanks(message["X"], message["Y"], message["Heading"],
                                                       message["TurretHeading"], message["Health"], message["Ammo"])
            else:
                tank_dictionary[message["Id"]].update(message["X"], message["Y"], message["Heading"],
                                                      message["TurretHeading"], message["Health"], message["Ammo"])
        else:
            pickup_dictionary[message["Id"]] = [message["Type"], message["X"], message["Y"]]
    else:
        time_left = message


def scout():
    print("kys leo")
    GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {'Amount': 0})
    time.sleep(0.3)
    read_data()
    GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {'Amount': 90})
    time.sleep(0.3)
    read_data()
    GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {'Amount': 180})
    time.sleep(0.3)
    read_data()
    GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {'Amount': 270})
    time.sleep(0.3)
    read_data()

# Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
parser.add_argument('-H', '--hostname', default='127.0.0.1', help='Hostname to connect to')
parser.add_argument('-p', '--port', default=8052, type=int, help='Port to connect to')
parser.add_argument('-n', '--name', default='RandomBot', help='Name of bot')
args = parser.parse_args()

# Set up console logging
if args.debug:
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

# Connect to game server
GameServer = ServerComms(args.hostname, args.port)

# Spawn our tank
logging.info("Creating tank with name '{}'".format(args.name))
GameServer.sendMessage(ServerMessageTypes.CREATETANK, {'Name': args.name})

# Main loop - read game messages, ignore them and randomly perform actions

tanks = bot_classes.Tanks
tank_dictionary = {}
pickup_dictionary = {}
snitch = []
time_left = 300

message = GameServer.readMessage()
our_id = message["Id"]
tank_dictionary[our_id] = tanks(message["X"], message["Y"], message["Heading"],
                                message["TurretHeading"], message["Health"], message["Ammo"])
us = tank_dictionary[our_id]
scout()
while True:
    scout()
    run_to_goal()
