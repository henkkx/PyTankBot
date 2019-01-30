import argparse
import random
import bot_classes
import time
import math
from Server_comms import *



def heading_to(x, y):
    heading = float(math.atan2((y - us.tank_Y), (x - us.tank_X)))  # returns heading in radians
    heading = float(math.degrees(heading))
    heading = math.fabs(heading - 360) % 360
    return heading

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
def initialize():
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
    global tank_dictionary, pickup_dictionary, message, us,our_id, time_left, snitch, GameServer, tanks
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


initialize()

while True:
    scout()
    fire_at_closest()
    time.sleep(2)






