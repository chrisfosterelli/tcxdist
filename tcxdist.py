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

def get_time(trackpoint):
    for child in trackpoint:
        if child.tag == '{:s}Time'.format(ns1):
            return datetime.datetime.strptime(child.text, date_str)


if __name__ == '__main__':

    args = parser.parse_args()
    tree = etree.parse(args.input)
    distance = float(args.km) * 1000

    laps = tree.find('//{:s}Lap'.format(ns1))
    trackpoints = tree.findall('//{:s}Trackpoint'.format(ns1))

    start, end = get_time(trackpoints[0]), get_time(trackpoints[-1])
    length = (end - start).total_seconds()

    for lap in laps:
        if lap.tag == '{:s}DistanceMeters'.format(ns1):
            lap.text = '{:.4f}'.format(float(args.km))

    for trackpoint in trackpoints:
        time = get_time(trackpoint)
        for child in trackpoint:
            if child.tag == '{:s}DistanceMeters'.format(ns1):
                cur_dist = ((time - start).total_seconds()) / length * distance
                child.text = '{:.4f}'.format(cur_dist)
            if child.tag == '{:s}Extensions'.format(ns1):
                el_tpx = etree.Element('{:s}TPX'.format(ns2))
                el_speed = etree.SubElement(el_tpx, '{:s}Speed'.format(ns2))
                el_speed.text = '{:.4f}'.format(distance / length)
                child.remove(child[0])
                child.append(el_tpx)

    tree.write(args.output, xml_declaration=True, encoding='utf-8')
    print('Wrote output XML to', args.output)
