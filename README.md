# TCXDist

Python program to embed distance metrics into a TCX file, so you can keep valid
distance, time, and heart rate statistics in Strava while using an indoor bike
trainer.

## Problem

If you don't have an external speed sensor hooked up to your wheel and you use
an indoor cycling trainer with a garmin watch, you have to choose between a 
couple of options in Strava:

1. Manually add an activity (accurate time and distance, no heart rate)
2. Upload the garmin activity (accurate heart rate and time, no distance)
3. Manually add an activity, and upload garmin activity (accurate heart rate 
and distance, doubled time)

There's no official solution that gives you all three.

## Solution

This is a quick Python script that takes a TCX file containing heart rate data
from Strava and embeds whatever distance metric you set. So if you know that
you did the equivalent of 60km on the trainer you can run:

```bash
# python tcxdist.py activity_XXXXX.tcx output.tcx 60
```

Then you'll end up with a TCX file you can upload to Strava that contains your
heart rate data and newly added distance data adding up to 60km. This lets you 
keep your stats in order and still use an indoor trainer, without having to 
purchase and set up a wheel sensor!
