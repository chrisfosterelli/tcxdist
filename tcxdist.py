#!/usr/bin/env python3

""" Manually add distance to a TCX file """

import argparse
import datetime
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('km')


def get_time(trackpoint):
    for child in trackpoint:
        if child.tag == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time':
            return datetime.datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S.%fZ")

if __name__ == '__main__':
    args = parser.parse_args()
    input_tree = etree.parse(args.input)

    prefix = '//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
    lap = prefix + 'Lap'
    trackpoint = prefix + 'Trackpoint'

    lap = input_tree.find(lap)
    for child in lap:
        if child.tag == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters':
            child.text = '{:.4f}'.format(float(args.km))

    trackpoints = input_tree.findall(trackpoint)

    start = get_time(trackpoints[0])
    end = get_time(trackpoints[-1])
    length = (end - start).total_seconds()
    distance = float(args.km) * 1000

    for trackpoint in trackpoints:
        time = get_time(trackpoint)
        for child in trackpoint:
            if child.tag == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters':
                child.text = '{:.4f}'.format(( (time - start).total_seconds() ) / length * distance)
            if child.tag == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Extensions':
                child.remove(child[0])
                el = etree.Element('jjTPX')
                b = etree.SubElement(el, 'jjSpeed')
                b.text = '7.40740'
                child.append(el)

    filename = '/tmp/test.tcx'
    input_tree.write(filename)
