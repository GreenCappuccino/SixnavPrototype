import cadquery as cq
from cadquery import exporters

# Raspberry Pi Pico

# Dimensions
## Board Dimensions
d_width = 21
d_height = 51
d_thickness = 1
## Hole Dimensions
d_mounting_diameter = 2.1
d_mounting_spacing = 11.4
d_mounting_inset = 2
d_castellation_diameter = 1
d_tht_diameter = 1
d_tht_spacing = 2.54
d_tht_inset = 1.61
d_tht_inset_debug = 1.6
d_tht_offset = 1.37
## Connector Dimensions
d_usb_width = 8
d_usb_depth = 6.25
d_usb_height = 3
d_usb_offset = 1.3

# Modelling
## Board
p = cq.Workplane("XY") \
      .box(d_width,d_height,d_thickness)
## Mounting Holes
p = p.faces("+Z") \
     .workplane() \
     .pushPoints([ \
         (-d_mounting_spacing/2,d_height/2-d_mounting_inset), \
         (d_mounting_spacing/2,d_height/2-d_mounting_inset), \
         (-d_mounting_spacing/2,-d_height/2+d_mounting_inset), \
         (d_mounting_spacing/2,-d_height/2+d_mounting_inset),]) \
     .hole(d_mounting_diameter)
## THT Holes and Castellations
p = p.faces("+Z") \
     .workplane() \
     .pushPoints( \
         ### THT Pins 1-20
         [(-d_width/2+d_tht_inset,d_height/2-d_tht_offset-(i*d_tht_spacing)) for i in range(20)] + \
         ### Castellations of Pins 1-20
         [(-d_width/2,d_height/2-d_tht_offset-(i*d_tht_spacing)) for i in range(20)] + \
         ### THT Pins 21-40
         [(d_width/2-d_tht_inset,d_height/2-d_tht_offset-(i*d_tht_spacing)) for i in range(20)] + \
         ### Castellations of Pins 21-40
         [(d_width/2,d_height/2-d_tht_offset-(i*d_tht_spacing)) for i in range(20)] + \
         ### THT Debug
         [ \
             (-d_tht_spacing, -d_height/2 + d_tht_inset_debug), \
             (0, -d_height/2 + d_tht_inset_debug), \
             (d_tht_spacing, -d_height/2 + d_tht_inset_debug) \
         ] + \
         ### Castellations of Debug
         [ \
             (-d_tht_spacing, -d_height/2), \
             (0, -d_height/2), \
             (d_tht_spacing, -d_height/2) \
         ]) \
     .circle(d_tht_diameter/2) \
     .cutBlind(-d_thickness)
     
## USB Connector
p = p.faces("+Z") \
     .workplane(origin=(0,d_height/2-d_usb_depth/2+d_usb_offset,0)) \
     .rect(d_usb_width,d_usb_depth) \
     .extrude(d_usb_height)
## Center Pins 11 and 30 about X axis

result = p
exporters.export(result, 'build/Raspberry Pi Pico.step', exporters.ExportTypes.STEP)