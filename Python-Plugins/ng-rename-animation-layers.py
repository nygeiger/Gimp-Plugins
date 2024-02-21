#!/usr/bin/env python
# -*- coding: utf-8 -*-

# timepattern=r'(\(\s*(\d+)\s*ms\s*\))'

import sys,os,re,traceback
from collections import namedtuple
from gimpfu import *

debug='OFN_DEBUG' in os.environ
  
def trace(format,*args):
    if debug:
        print format % args

# 
        
# possibly have two menus, one for (combine) and another for (replace)
## Make Renaming Layer from Frame** to Frame **-** more efficient
def removeOptimizedTag(image):
    image.undo_group_start()
    combined_layer_tag = "(combine)"
    bg_layer_prefix = "Background"
    frame_prefix = "Frame "
    try:
        for layer in image.layers:
            if layer.name.startswith(bg_layer_prefix):
                layer.name=layer.name.replace(bg_layer_prefix,"Frame 1 ")
            layer.name=layer.name.replace(frame_prefix,"Frame 1-")
            layer.name=layer.name.replace(combined_layer_tag,"")
    except Exception as e:
        pdb.gimp_message('%s' % e)
        if debug:
            print traceback.format_exc()
        
    # restore stuff
    image.undo_group_end()

def removeUnoptimizedTag(image):
    image.undo_group_start()
    unoptimized_layer_tag = "(replace)"
    bg_layer_prefix = "Background"
    frame_prefix = "Frame "
    try:
        for layer in image.layers:
            if layer.name.startswith(bg_layer_prefix):
                layer.name=layer.name.replace(bg_layer_prefix,"Frame 1 ")
            layer.name=layer.name.replace(frame_prefix,"Frame 1-")
            layer.name=layer.name.replace(unoptimized_layer_tag,"")
    except Exception as e:
        pdb.gimp_message('%s' % e)
        if debug:
            print traceback.format_exc()
        
    # restore stuff
    image.undo_group_end()


### Registrations
author='Nyles Geiger'
year='2024'
menu='<Image>/Layer/NG Rename'
optimizedDesc='Remove tag from Layer name <(combine)>'
unoptimizedDesc='Remove tag from Layer name <(replace)>'
whoiam='\n'+os.path.abspath(sys.argv[0])

"""
Register Shape

register(
name
blurb
help
author
copyright
date
menupath
imagetypes
params
results
function
)

more info at::
locale -> /Users/nylesgeiger/Work/Photos/Gimp/Gimp Scripts/The Structure Of A Plugin.html
hyperlink -> https://www.gimp.org/docs/python/structure-of-plugin.html
"""

register(
    "ng-rename-optimized-animation-layers",
    optimizedDesc,optimizedDesc+whoiam,author,author,year,optimizedDesc+'...',
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
    ],
    [],
    removeOptimizedTag,
    menu,
)

register(
    "ng-rename-unoptimized-animation-layers",
    unoptimizedDesc,unoptimizedDesc+whoiam,author,author,year,unoptimizedDesc+'...',
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
    ],
    [],
    removeUnoptimizedTag,
    menu,
)

main()
