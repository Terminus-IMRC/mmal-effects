#!/usr/bin/env python

SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080
HORIZ_NUM = 4
VERT_NUM  = 3
assert(SCREEN_WIDTH  % HORIZ_NUM == 0)
assert(SCREEN_HEIGHT % VERT_NUM  == 0)

EFFECTS = ['none', 'solarize', 'sketch', 'emboss',
        'oilpaint', 'hatch', 'gpen', 'pastel',
        'colourswap', 'posterise', 'colourpoint', 'cartoon']
assert(len(EFFECTS) >= 1)

from collections import OrderedDict
from math import ceil
import json


def calc_splitter():
    i = 1
    sum = 1
    num_final_splitters = int(ceil(len(EFFECTS) / 4.0))
    while num_final_splitters > 1:
        i += 1
        sum += num_final_splitters
        num_final_splitters = int(ceil(num_final_splitters / 4.0))
    return i


def main():

    splitter_depth = calc_splitter()
    capture_width  = SCREEN_WIDTH  // HORIZ_NUM
    capture_height = SCREEN_HEIGHT // VERT_NUM

    d = OrderedDict()

    d["camera"] = {
            "component": "vc.ril.camera",
            "control": {
                "camera_num": 0
            },
            "output0": {
                "connect_to": ["splitter0_0", 0],
                "width":  capture_width,
                "height": capture_height,
                "encoding": "i420"
            }
    }

    for depth in range(splitter_depth):
        n = int(4**depth)  # n. of splitters in this level
        for i in range(n):
            name = "splitter%d_%d" % (depth, i)
            d[name] = OrderedDict()
            d[name]["component"] = "vc.ril.video_splitter"
            d[name]["input0"] = {
                    "width": capture_width,
                    "height": capture_height,
                    "encoding": "i420"
            }
            for j in range(4):
                if i*4+j >= len(EFFECTS):
                    continue
                d[name]["output%d" % j] = {
                        "width": capture_width,
                        "height": capture_height,
                        "encoding": "i420"
                }
                if depth == splitter_depth - 1:
                    d[name]["output%d" % j]["connect_to"] = ("effect%d" % (i*4+j), 0)
                else:
                    d[name]["output%d" % j]["connect_to"] = ("splitter%d_%d" % (depth+1, i*4+j), 0)

    for i in range(len(EFFECTS)):
        d["effect%d" % i] = {
                "component": "vc.ril.image_fx",
                "input0": {
                    "width": capture_width,
                    "height": capture_height,
                    "encoding": "i420"
                },
                "output0": {
                    "effect": EFFECTS[i],
                    "connect_to": ("render%d" % i, 0),
                    "width": capture_width,
                    "height": capture_height,
                    "encoding": "i420"
                }
        }

    for i in range(len(EFFECTS)):
        x = i %  HORIZ_NUM
        y = i // HORIZ_NUM
        d["render%d" % i] = {
                "component": "vc.ril.video_render",
                "input0": {
                    "rect": {
                        "x": capture_width * x,
                        "y": capture_height * y,
                        "width": capture_width,
                        "height": capture_height
                    },
                    "width": capture_width,
                    "height": capture_height,
                    "encoding": "i420"
                }
        }


    print(json.dumps(d, indent=4))


if __name__ == '__main__':
    main()
