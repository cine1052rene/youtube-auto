# 곰곰한 마음 — 로봇 컨셉 무료 시험 (블렌더 단독, 크레딧 0)
# 실행: blender -b --factory-startup -P robot_v1.py -- <out_dir> <still|anim> [scale]
import bpy, bmesh, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(argv[0] if argv else "render")
MODE = argv[1] if len(argv) > 1 else "still"
SCALE = int(argv[2]) if len(argv) > 2 else 50
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------- 재질 ----------
def mat(name, color, rough=0.45, metal=0.0, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if coat and "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m

CREAM = mat("cream", (0.98, 0.84, 0.62), 0.38, coat=0.4)
CREAM2 = mat("cream_dark", (0.80, 0.70, 0.57), 0.5)
SCREEN = mat("screen", (0.05, 0.06, 0.09), 0.15, coat=1.0)
EYE = mat("eye", (1, 0.95, 0.8), emit=(1.0, 0.88, 0.62), strength=6)
BLUSH = mat("blush", (1, 0.5, 0.5), emit=(1.0, 0.45, 0.45), strength=2.5)
BROWN = mat("bag", (0.33, 0.18, 0.10), 0.7)
STAR = mat("star", (1.0, 0.78, 0.18), 0.4, emit=(1.0, 0.7, 0.1), strength=0.3)
YEL = mat("kong", (1.0, 0.72, 0.05), 0.35, coat=0.5)
ORANGE = mat("beak", (1.0, 0.5, 0.12), 0.4)
GREEN = mat("sprout", (0.45, 0.75, 0.25), 0.5)
WOOD = mat("wood", (0.42, 0.25, 0.13), 0.55)
WALL = mat("wall", (0.98, 0.80, 0.62), 0.9)
POT = mat("pot", (0.85, 0.48, 0.32), 0.7)
LEAF = mat("leaf", (0.30, 0.55, 0.25), 0.6)
MUG = mat("mug", (0.62, 0.80, 0.78), 0.3, coat=0.6)
BOOK1 = mat("book1", (0.85, 0.40, 0.35), 0.6); BOOK2 = mat("book2", (0.40, 0.55, 0.75), 0.6)

def put(o, m, parent=None, smooth=True):
    o.data.materials.append(m)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if parent: o.parent = parent
    return o

def rbox(name, size, loc, m, bevel=0.3, parent=None, seg=6):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    md = o.modifiers.new("bv", "BEVEL"); md.width = bevel * min(size); md.segments = seg; md.limit_method = "NONE"
    return put(o, m, parent)

def ball(name, r, loc, m, parent=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24); o = bpy.context.object
    o.name = name; o.scale = scale; return put(o, m, parent)

def cyl(name, r, d, loc, m, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=48); o = bpy.context.object
    o.name = name; md = o.modifiers.new("bv", "BEVEL"); md.width = r * 0.25; md.segments = 4
    return put(o, m, parent)

def star(name, r, depth, loc, m, parent=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append(bm.verts.new((rr * math.cos(a), 0, rr * math.sin(a))))
    f = bm.faces.new(pts); r_ = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r_["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.y -= depth
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    o.location = loc; md = o.modifiers.new("bv", "BEVEL"); md.width = depth * 0.4; md.segments = 3
    return put(o, m, parent, smooth=False)

# ---------- 로봇 곰곰이 ----------
root = bpy.data.objects.new("robot_root", None); sc.collection.objects.link(root)
body = rbox("body", (1.0, 0.8, 0.9), (0, 0, 0.75), CREAM, 0.42, root)
bpy.ops.object.select_all(action="DESELECT"); body.select_set(True); bpy.context.view_layer.objects.active = body
bpy.ops.object.transform_apply(location=True)  # 원점을 바닥으로 → 몸 부품 좌표 = 실제 위치
belly = rbox("belly", (0.55, 0.05, 0.45), (0, -0.39, 0.72), CREAM2, 0.45, body)
for sx in (-1, 1):
    cyl(f"leg{sx}", 0.17, 0.35, (sx * 0.27, 0, 0.2), CREAM2, parent=root)
    ball(f"foot{sx}", 0.2, (sx * 0.27, -0.05, 0.05), CREAM, root, (1, 1.25, 0.55))
    arm = cyl(f"arm{sx}", 0.12, 0.5, (sx * 0.6, 0, 0.78), CREAM, rot=(0, sx * 0.35, 0), parent=body)
    ball(f"hand{sx}", 0.15, (sx * 0.68, -0.02, 0.52), CREAM2, body)
head_piv = bpy.data.objects.new("head_pivot", None); sc.collection.objects.link(head_piv)
head_piv.location = (0, 0, 1.2); head_piv.parent = root
head = rbox("head", (1.5, 1.1, 1.15), (0, 0, 0.62), CREAM, 0.42, head_piv)
face = rbox("face", (1.18, 0.08, 0.8), (0, -0.53, 0.6), SCREEN, 0.4, head_piv)
eyes = []
for sx in (-1, 1):
    eyes.append(ball(f"eye{sx}", 0.11, (sx * 0.26, -0.585, 0.68), EYE, head_piv, (1, 0.35, 1.25)))
    ball(f"blush{sx}", 0.09, (sx * 0.43, -0.585, 0.46), BLUSH, head_piv, (1.3, 0.2, 0.6))
    ball(f"ear{sx}", 0.2, (sx * 0.78, 0, 0.75), CREAM2, head_piv, (0.45, 1, 1))
bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.022, location=(0, -0.585, 0.47), rotation=(math.pi / 2, 0, 0))
mouth = bpy.context.object; mouth.name = "mouth"; put(mouth, EYE, head_piv)
bm = bmesh.new(); bm.from_mesh(mouth.data)                      # 위쪽 절반을 지워 웃는 입
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.005], context="VERTS"); bm.to_mesh(mouth.data); bm.free()
ant_piv = bpy.data.objects.new("antenna_pivot", None); sc.collection.objects.link(ant_piv)
ant_piv.location = (0.32, 0, 1.18); ant_piv.parent = head_piv
cyl("antenna", 0.025, 0.28, (0, 0, 0.14), CREAM2, parent=ant_piv); ball("antenna_tip", 0.07, (0, 0, 0.3), STAR, ant_piv)
# 상징 소품: 갈색 가방 + 노란 별 배지
strap = rbox("strap", (0.09, 0.03, 1.0), (0.04, -0.43, 0.83), BROWN, 0.3, body)
bpy.ops.object.select_all(action="DESELECT"); strap.select_set(True); bpy.context.view_layer.objects.active = strap
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
strap.rotation_euler = (0, math.radians(-50), 0)
rbox("bag", (0.38, 0.16, 0.32), (0.42, -0.42, 0.42), BROWN, 0.3, body)
star("badge", 0.13, 0.04, (-0.26, -0.43, 0.95), STAR, body)

# ---------- 콩이 (머리 꼭대기 한가운데, 머리 폭의 약 1/3) ----------
kong = bpy.data.objects.new("kong_root", None); sc.collection.objects.link(kong)
kong.location = (0, 0, 1.2 + 0.62 + 0.575); kong.parent = root
kb = ball("kong_body", 0.24, (0, 0, 0.22), YEL, kong, (1, 0.95, 0.95))
for sx in (-1, 1):
    ball(f"k_eye{sx}", 0.032, (sx * 0.09, -0.215, 0.27), SCREEN, kong)
    ball(f"k_wing{sx}", 0.09, (sx * 0.22, 0, 0.2), YEL, kong, (0.4, 0.8, 1))
    ball(f"k_foot{sx}", 0.05, (sx * 0.08, -0.05, 0.0), ORANGE, kong, (1, 1.4, 0.4))
bpy.ops.mesh.primitive_cone_add(radius1=0.05, depth=0.09, location=(0, -0.27, 0.21), rotation=(math.pi / 2, 0, 0))
put(bpy.context.object, ORANGE, kong)
cyl("k_stem", 0.012, 0.12, (0, 0, 0.5), GREEN, parent=kong)
for sx in (-1, 1): ball(f"k_leaf{sx}", 0.06, (sx * 0.06, 0, 0.57), GREEN, kong, (1, 0.35, 0.55))

# ---------- 미니어처 방 ----------
rbox("desk", (7, 4, 0.3), (0, 0.6, -0.15), WOOD, 0.05)
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 3.0, 5), rotation=(math.pi / 2, 0, 0)); put(bpy.context.object, WALL, smooth=False)
rbox("shelf", (3.2, 0.5, 0.12), (-0.6, 2.7, 3.1), WOOD, 0.1)
for i, (m_, h) in enumerate([(BOOK1, 0.7), (BOOK2, 0.6), (BOOK1, 0.75), (CREAM2, 0.55)]):
    rbox(f"book{i}", (0.18, 0.4, h), (-1.6 + i * 0.22, 2.65, 3.16 + h / 2), m_, 0.08)
cyl("pot", 0.28, 0.4, (1.9, 0.9, 0.2), POT)
for i, (x, y, z) in enumerate([(1.9, 0.9, 0.55), (1.75, 0.85, 0.7), (2.05, 0.95, 0.68), (1.9, 0.8, 0.85)]):
    ball(f"leafb{i}", 0.22, (x, y, z), LEAF, scale=(1, 1, 1.2))
cyl("mug", 0.2, 0.36, (-1.7, 0.2, 0.18), MUG)
bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.03, location=(-1.92, 0.2, 0.2), rotation=(math.pi / 2, 0, math.pi / 2)); put(bpy.context.object, MUG)
for i in range(3): rbox(f"block{i}", (0.3, 0.3, 0.3), (-1.1 + i * 0.05, -0.6, 0.15 + i * 0.3), [BOOK1, STAR, BOOK2][i], 0.25)

rbox("frame", (1.0, 0.06, 0.8), (1.6, 2.95, 2.6), WOOD, 0.08)
rbox("frame_in", (0.8, 0.02, 0.6), (1.6, 2.9, 2.6), MUG, 0.05)
cyl("lamp_stem", 0.04, 1.1, (2.4, 1.6, 0.55), WOOD); ball("lamp_shade", 0.35, (2.4, 1.6, 1.2), mat("shade", (1, 0.9, 0.7), emit=(1, 0.8, 0.5), strength=4), scale=(1, 1, 0.7))
# ---------- 조명·카메라 ----------
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND"); bg.inputs[0].default_value = (1.0, 0.85, 0.7, 1); bg.inputs[1].default_value = 0.5
def area(name, loc, rot, energy, color, size):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.color = color; d.size = size
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot
area("key", (-3, -4, 5), (math.radians(50), 0, math.radians(-35)), 1300, (1, 0.8, 0.6), 3)
area("fill", (4, -3, 2.5), (math.radians(70), 0, math.radians(50)), 250, (0.85, 0.9, 1), 3)
area("rim", (1.5, 3, 4), (math.radians(-40), 0, math.radians(160)), 500, (1, 0.8, 0.6), 2)
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 50
cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 2.8
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
target = bpy.data.objects.new("target", None); sc.collection.objects.link(target); target.location = (0, 0, 1.55)
tc = cam.constraints.new("TRACK_TO"); tc.target = target; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
cam_d.dof.focus_object = target
rig = bpy.data.objects.new("cam_rig", None); sc.collection.objects.link(rig); cam.parent = rig
cam.location = (0, -8.2, 1.9)

# ---------- 움직임 (4초, 24fps) — 고개 갸웃·눈 깜빡·안테나 흔들·콩이 폴짝·카메라 옆으로 돎 ----------
sc.render.fps = 24; sc.frame_start = 1; sc.frame_end = 96
def key(o, path, frame, val):
    setattr(o, path, val) if not isinstance(val, tuple) else None
    if isinstance(val, tuple):
        getattr(o, path)[:] = val
    o.keyframe_insert(path, frame=frame)
for f, a in [(1, -18), (96, 14)]: key(rig, "rotation_euler", f, (0, 0, math.radians(a)))
for f, t in [(1, 0), (30, 9), (55, 9), (80, -5), (96, 0)]: key(head_piv, "rotation_euler", f, (0, math.radians(t), 0))
for f, t in [(1, 0), (12, 14), (24, -10), (36, 8), (48, -4), (60, 0), (96, 0)]: key(ant_piv, "rotation_euler", f, (0, math.radians(t), 0))
for e in eyes:
    for f, s in [(1, 1.25), (40, 1.25), (43, 0.1), (46, 1.25), (96, 1.25)]: key(e, "scale", f, (1, 0.35, s))
base = kong.location.z
for f, z in [(1, 0), (60, 0), (66, 0.25), (72, 0), (76, 0.08), (80, 0), (96, 0)]: key(kong, "location", f, (0, 0, base + z))
for f, s in [(1, 1), (58, 1), (60, 0.85), (64, 1.05), (72, 0.85), (75, 1), (96, 1)]: key(kong, "scale", f, (1 / s ** 0.5, 1 / s ** 0.5, s))

# ---------- 렌더 ----------
r = sc.render; r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y, r.resolution_percentage = 1080, 1920, SCALE
try: sc.view_settings.view_transform = "AgX"
except TypeError: pass
for lk in ("AgX - Punchy", "Punchy", "AgX - Medium High Contrast"):
    try: sc.view_settings.look = lk; break
    except TypeError: pass
try: sc.eevee.taa_render_samples = 64
except Exception: pass
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(OUT, "..", "robot_v1.blend")))
if MODE == "still":
    for f in (1, 48, 66):
        sc.frame_set(f); r.filepath = os.path.join(OUT, f"still_{f:03d}.png"); bpy.ops.render.render(write_still=True)
else:
    r.image_settings.file_format = "PNG"; r.filepath = os.path.join(OUT, "f_"); bpy.ops.render.render(animation=True)
print("DONE")
