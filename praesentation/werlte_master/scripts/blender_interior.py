"""Gastro-Innenraum aus dem Modell (Grundriss Blatt 21, Layout normal): Gastraum x 4–32, y 0–10, Höhe 3,2 m; Bar x 5–15 / y 8,6–10; 12 Barhocker, Tische 1,2 x 0,8 m mit Stühlen 0,45 m.
Nicht im Plan und deshalb NICHT dargestellt: Pfeiler/Stützen, Glas-Stahl-Trennung, Bänke (Möblierung nur Tische, Stühle, Hocker).
Aufruf: python3 blender_interior.py clay|mat  -> visualisierungen/higgsfield/referenzen/<modus>_07_gastro.png"""
import bpy, bmesh, json, os, sys, math
from mathutils import Vector
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HF = os.path.join(ROOT, "visualisierungen", "higgsfield")
D = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json"))); FURN = D["furnishing"]["normal"]
MODE = sys.argv[1] if len(sys.argv) > 1 else "mat"; clay = MODE == "clay"
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; MAT = {}
def mat(name, color, rough=0.6, metal=0.0, trans=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if trans: b.inputs["Transmission Weight"].default_value = trans
    if emit: b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = emit
    MAT[name] = m; return m
if clay:
    for n, c in (("boden", (0.55, 0.40, 0.27)), ("decke", (0.93, 0.92, 0.88)), ("oliv", (0.42, 0.45, 0.30)), ("glas", (0.78, 0.88, 0.95)), ("rahmen", (0.1, 0.11, 0.13)), ("eiche", (0.72, 0.58, 0.4)), ("bar", (0.2, 0.14, 0.1)), ("cognac", (0.45, 0.2, 0.17)), ("bordeaux", (0.35, 0.1, 0.12)), ("messing", (0.7, 0.55, 0.25)), ("lampe", (0.9, 0.8, 0.6))): mat(n, c, 0.9)
else:
    mat("boden", (0.42, 0.41, 0.4), 0.45); mat("decke", (0.92, 0.9, 0.85), 0.9); mat("oliv", (0.2, 0.25, 0.14), 0.7); mat("glas", (0.85, 0.92, 0.95), 0.03, 0, 1.0); mat("rahmen", (0.07, 0.075, 0.085), 0.4, 0.6)
    mat("eiche", (0.55, 0.4, 0.25), 0.5); mat("bar", (0.07, 0.06, 0.055), 0.4); mat("cognac", (0.5, 0.24, 0.1), 0.85); mat("bordeaux", (0.28, 0.04, 0.07), 0.85); mat("messing", (0.7, 0.52, 0.22), 0.3, 1.0)
    mat("lampe", (1.0, 0.75, 0.45), 0.5, 0, 0, 12.0)
    nt = MAT["boden"].node_tree; b = nt.nodes["Principled BSDF"]; tc = nt.nodes.new("ShaderNodeTexCoord"); n = nt.nodes.new("ShaderNodeTexNoise"); r = nt.nodes.new("ShaderNodeValToRGB"); n.inputs["Scale"].default_value = 3.0; n.inputs["Detail"].default_value = 10
    r.color_ramp.elements[0].color = (0.33, 0.32, 0.31, 1); r.color_ramp.elements[1].color = (0.48, 0.47, 0.46, 1); nt.links.new(tc.outputs["Object"], n.inputs["Vector"]); nt.links.new(n.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], b.inputs["Base Color"])
def X(x): return -x
def box(x0, x1, y0, y1, z0, z1, m, name="b", shape="cube"):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    xa, xb = sorted((X(x0), X(x1))); o.location = ((xa + xb) / 2, (y0 + y1) / 2, (z0 + z1) / 2); o.scale = (xb - xa, y1 - y0, z1 - z0); o.data.materials.append(MAT[m]); return o
def cyl(x, y, z0, z1, r, m, name="c"):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=r, radius2=r, depth=1.0); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    o.location = (X(x), y, (z0 + z1) / 2); o.scale = (1, 1, z1 - z0); o.data.materials.append(MAT[m]); return o
x0, x1, y0, y1, H = 4.0, 32.0, 0.0, 10.0, 3.2
box(x0, x1, y0, y1, -0.1, 0, "boden"); box(x0, x1, y0, y1, H, H + 0.1, "decke")
box(x0 - 0.1, x0, y0, y1, 0, H, "oliv"); box(x1, x1 + 0.1, y0, y1, 0, H, "oliv"); box(x0, x1, y1, y1 + 0.1, 0, H, "oliv")
# Platzseite: Glasfront 0–3,1 m, Pfosten alle 1,4 m (wie Außenmodell), Türen x 17–19 und 29,5–31 (Fluchtwege laut Blatt 21)
box(x0, x1, y0 - 0.02, y0, 0, 3.1, "glas"); box(x0, x1, y0 - 0.05, y0, 3.1, H, "rahmen")
import numpy as np
for x in np.arange(5.4, 32, 1.4): box(x - 0.03, x + 0.03, y0 - 0.08, y0 + 0.04, 0, 3.1, "rahmen")
# Barthresen: x 5–15, y 8,6–10 mit geriffelter Front (Lamellen), Eichenplatte, Messingleiste, Regal
box(5, 15, 9.0, 10, 0, 1.05, "bar"); box(5, 15, 8.9, 10, 1.05, 1.1, "eiche")
for i in range(int(10 / 0.12)): box(5 + i * 0.12, 5 + i * 0.12 + 0.06, 8.85, 9.0, 0.05, 1.0, "bar")
box(5, 15, 8.85, 8.9, 0.95, 1.0, "messing"); box(5.5, 14.5, 9.85, 10.0, 1.4, 2.5, "bar"); [box(5.7 + i * 0.9, 5.75 + i * 0.9, 9.75, 9.85, 1.5 + 0.35 * j, 1.52 + 0.35 * j, "messing") for i in range(10) for j in range(3)]
for sx, sy in FURN["stools"]: cyl(sx, sy, 0, 0.72, 0.19, "bordeaux", "Barhocker"); cyl(sx, sy, 0.72, 0.78, 0.22, "cognac", "Sitz")
for t in FURN["tables"]:
    box(t["x"], t["x"] + 1.2, t["y"], t["y"] + 0.8, 0.72, 0.76, "eiche", "Tisch"); box(t["x"] + 0.55, t["x"] + 0.65, t["y"] + 0.35, t["y"] + 0.45, 0, 0.72, "rahmen", "Fuss")
    for cx in (t["x"] + 0.15, t["x"] + 0.6):
        for cy in (t["y"] - 0.45, t["y"] + 0.8):
            box(cx, cx + 0.45, cy, cy + 0.45, 0.42, 0.48, "cognac", "Stuhl"); box(cx, cx + 0.45, cy + (0.4 if cy < t["y"] else 0), cy + (0.45 if cy < t["y"] else 0.05), 0.48, 0.9, "cognac", "Lehne")
            for dx in (0.02, 0.4):
                for dy in (0.02, 0.4): box(cx + dx, cx + dx + 0.03, cy + dy, cy + dy + 0.03, 0, 0.42, "rahmen", "Bein")
# Pendelleuchten über Tischen (Messing/Opal)
for t in FURN["tables"]:
    cx, cy = t["x"] + 0.6, t["y"] + 0.4; box(cx - 0.005, cx + 0.005, cy - 0.005, cy + 0.005, 1.9, H, "messing", "Kabel"); cyl(cx, cy, 1.75, 1.95, 0.14, "lampe", "Leuchte")
# Welt, Kamera, Licht
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.82, 0.92, 1); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8
cam = bpy.data.cameras.new("c"); cam.lens = 21; cam.sensor_width = 36; co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); co.location = (X(30.5), 1.4, 1.5)
d = Vector((X(11.0), 8.0, 1.2)) - co.location; co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); sc.camera = co
area = bpy.data.lights.new("a", "AREA"); area.energy = 900 if not clay else 400; area.size = 20; area.size_y = 8; ao = bpy.data.objects.new("a", area); sc.collection.objects.link(ao); ao.location = (X(18), 5, H - 0.05)
sc.render.resolution_x, sc.render.resolution_y = 2400, 1350; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 12 if clay else 48; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3 if clay else 6
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = 1.6 if clay else -0.5
os.makedirs(os.path.join(HF, "referenzen"), exist_ok=True); sc.render.filepath = os.path.join(HF, "referenzen", f"{MODE}_07_gastro.png"); bpy.ops.render.render(write_still=True); print("ok gastro")
