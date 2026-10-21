import bpy, os
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else ".", "render", "robot_v1.blend"))
bpy.context.scene.frame_set(48)
for n in ["body","strap","bag","badge","belly","arm-1","arm1","head","kong_body"]:
    o=bpy.data.objects.get(n)
    if not o: print("XX",n,"none");continue
    c=[o.matrix_world@Vector(b) for b in o.bound_box]
    print("XX",n,o.parent.name if o.parent else None,[round(min(v[i] for v in c),2) for i in range(3)],[round(max(v[i] for v in c),2) for i in range(3)])
