#!/usr/bin/env python
#
# Script to extract and process progress of liked (loved)
# message receipts
#
# Author: Asanga Udugama (adu@comnets.uni-bremen.de)
# Date: 11-oct-2017
#
# Author: Jens Dede (jd@comnets.uni-bremen.de)
# Date: 16-jan-2017
#
# TODO:
#
# - Do not create an output file in case of no results (wrong input file
#       format)
# - Store the information in a more generic way (-> NodeInformationHelpers)
# - ...

import sys, os, re
import argparse

# Include the upper directory to access the helper module
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from helper import NodeHelpers, FileHelpers


excluded_nodes = ["abc", "xyz"]
dump_frequency = 3600.0


class Event:
    def __init__(self, event_name, event_type):
        self.event_name = event_name
        self.event_type = event_type
        self.times_received = 0


class Node:
    def __init__(self, node_name):
        self.node_name = node_name
        self.events = []


def get_node(nodes, node_name):
    node_found = False
    for node in nodes:
        if node.node_name == node_name:
            node_found = True
            break

    if not node_found:
        print("Node does not exist when searching - ", node_name)
        sys.exit(2)
    else:
        return node


def add_node(nodes, node_name):
    node_found = False
    for node in nodes:
        if node.node_name == node_name:
            node_found = True
            break

    if not node_found:
        node = Node(node_name)
        nodes.append(node)

    return node


def get_event(node, event_name):
    event_found = False
    for event in node.events:
        if event.event_name == event_name:
            event_found = True
            break

    if not event_found:
        print("Event does not exist when searching - ", node.node_name, " ", event_name)
        sys.exit(2)
    else:
        return event



def add_event(node, event_name, event_type):
    event_found = False
    for event in node.events:
        if event.event_name == event_name:
            event_found = True
            break

    if not event_found:
        event = Event(event_name, event_type)
        node.events.append(event)
    else:
        print("Event exist when adding - ", node.node_name, " ", event_name)
        sys.exit(2)


def extract_from_log_and_accumilate_and_print(inputfilename, outputfilename):
    nodes = []

    last_dump_time = dump_frequency
    total_loved_first_copy = 0
    total_loved_additional_copies = 0

    last_loved_first_copy = 0
    last_loved_additional_copies = 0

    with open(inputfilename, "r") as inputfile, open(outputfilename, "w+") as outputfile:
        print("Input File:               ", inputfile.name)
        print("Loved Received Progress:  ", outputfile.name)



        outputfile.write("# sim time >!< total loved 1st copy >!< total loved 1st copies >!< last loved 1st copy >!< last loved 1st copies\n")

        current_time = 0.0
        for line in inputfile:

            if "INFO" in line and ("KKeetchiLayer" in line or "KRRSLayer" in line or "KEpidemicRoutingLayer" in line) \
                and ">!<LI>!<DM>!<" in line:
                words = line.split(">!<")
                current_time = float(words[1].strip())

            # check dump period and dump
            while last_dump_time < current_time:

                outputfile.write(str(last_dump_time) + " >!< " +  str(total_loved_first_copy) + " >!< "
                                    + str(total_loved_additional_copies) + " >!< " + str(last_loved_first_copy)
                                    + " >!< " + str(last_loved_additional_copies) + "\n")
                last_loved_first_copy = 0
                last_loved_additional_copies = 0

                last_dump_time += dump_frequency

            # identify events or accumilate
            if "INFO" in line and "KBasicUBM" in line and ">!<NE>!<" in line:
                words = line.split(">!<")

                if any(words[2].strip() in ex_node_name for ex_node_name in excluded_nodes):
                    continue
                else:
                    node = add_node(nodes, words[2].strip())
                    add_event(node, words[4].strip(), words[8].strip())

            elif "INFO" in line and ("KKeetchiLayer" in line or "KRRSLayer" in line or "KEpidemicRoutingLayer" in line) \
                and ">!<LI>!<DM>!<" in line:
                words = line.split(">!<")

                # accumilate
                if any(words[2].strip() in ex_node_name for ex_node_name in excluded_nodes):
                    pass
                else:
                    node = get_node(nodes, words[2].strip())
                    event = get_event(node, words[8].strip())

                    if event.event_type == "L":
                        if event.times_received == 0:
                            total_loved_first_copy += 1
                            last_loved_first_copy += 1
                        else:
                            total_loved_additional_copies += 1
                            last_loved_additional_copies += 1
                    event.times_received += 1



parser = argparse.ArgumentParser(description='Create statistics: process of progressing liked (loved) message receipts')
parser.add_argument('logfiles', type=str, nargs="+", help="The logfiles")
args = parser.parse_args()


for inputfile in args.logfiles:
    print("Processing", inputfile)

    fileHelper = FileHelpers.FileHelper(inputfile)

    extract_from_log_and_accumilate_and_print(
            fileHelper.getInputFile(),
            fileHelper.getGenericOutput(suffix="_lrp")
            )


