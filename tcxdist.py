#!/usr/bin/env python3

""" Manually add distance to a TCX file """

import argparse
import datetime
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
parser.add_argument('km')

date_str = '%Y-%m-%dT%H:%M:%S.%fZ'
ns1 = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
ns2 = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}'

def get_lap_length(lap):
    for child in lap:
        if child.tag == '{:s}TotalTimeSeconds'.format(ns1):
            return float(child.text)

def get_trackpoint_datetime(trackpoint):
    for child in trackpoint:
        if child.tag == '{:s}Time'.format(ns1):
            return datetime.datetime.strptime(child.text, date_str)


if __name__ == '__main__':

    args = parser.parse_args()
    tree = etree.parse(args.input)
    distance = float(args.km) * 1000

    laps = tree.findall('//{:s}Lap'.format(ns1))
    trackpoints = tree.findall('//{:s}Trackpoint'.format(ns1))

    start = get_trackpoint_datetime(trackpoints[0])
    end = get_trackpoint_datetime(trackpoints[-1])
    total_length = (end - start).total_seconds()

    for lap in laps:
        lap_length = get_lap_length(lap)
        for child in lap:
            if child.tag == '{:s}DistanceMeters'.format(ns1):
                child.text = '{:.4f}'.format(
                    lap_length / total_length * distance
                )

    for trackpoint in trackpoints:
        timestamp = get_trackpoint_datetime(trackpoint)
        for child in trackpoint:
            if child.tag == '{:s}DistanceMeters'.format(ns1):
                cur_length = (timestamp - start).total_seconds()
                cur_dist = cur_length / total_length * distance
                child.text = '{:.4f}'.format(cur_dist)
            if child.tag == '{:s}Extensions'.format(ns1):
                el_tpx = etree.Element('{:s}TPX'.format(ns2))
                el_speed = etree.SubElement(el_tpx, '{:s}Speed'.format(ns2))
                el_speed.text = '{:.4f}'.format(distance / total_length)
                child.remove(child[0])
                child.append(el_tpx)

    tree.write(args.output, xml_declaration=True, encoding='utf-8')
    print('Wrote output XML to', args.output)
