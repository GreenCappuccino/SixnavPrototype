import cadquery as cq
from cadquery import exporters

# X908-7C-F (IR908-7C-F, PT908-7C-F)

# Dimensions
## Package Dimensions
d_width             = 4.5
d_height            = 5.7
d_thickness         = 1.5
## Lens Dimensions
d_lens_height       = 4.5
d_lens_diameter     = 1.5
## Lead Dimensions
d_lead_spacing      = 2.54
d_lead_width        = 0.4
### Datasheet length 10.0 mm
### leads shortened for CAD
d_lead_length       = 2.5
d_lead_front_offset = 0.8

# Modelling
## Package (offset so that leads are centered)
p = cq.Workplane("XY", (0.8-1.5/2,0,d_height/2)) \
      .box(d_thickness, d_width, d_height)
## Lens
p = p.faces("+X") \
     .workplane(origin=(0,0,d_lens_height)) \
     .sphere(d_lens_diameter/2)
## Leads
p = p.faces("-Z") \
     .workplane(origin=(0,0,0)) \
     .pushPoints([(0,d_lead_spacing/2),(0,-d_lead_spacing/2)]) \
     .rect(d_lead_width,d_lead_width,centered=True) \
     .extrude(d_lead_length)
## Move over to center over lead
## (Pin 1 of PT908-7C-F)
## (Pin 2 of IR908-7C-F)
p = p.translate((0,d_lead_spacing/2,0))

result = p
exporters.export(result, 'build/X908-7C-F.step', exporters.ExportTypes.STEP)