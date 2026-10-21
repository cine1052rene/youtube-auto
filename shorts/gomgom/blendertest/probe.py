import bpy
p=bpy.types.RenderSettings.bl_rna.properties["engine"]
print("ENGINES",[i.identifier for i in p.enum_items])
print("VER",bpy.app.version_string)
