"""Blender-Szene und Ansichten der Variantenstudie. Baut EIN Modell je Variante aus scripts/studie/varianten.py und rendert alle Ansichten daraus.
Aufruf: python3 blender_studie.py <A|B|C|D> [ansicht ...]   ansicht: persp aerial front rear west east   (Standard: alle)
Szene mit x' = -x gespiegelt (wie das B3-Modell: Platz-Ansicht zeigt den Kern rechts). Himmelsrichtung unbekannt (C-13). Fensteranordnung rein schematisch.
Ausgabe: studie_gebaeudeformen/<Variante>/ansichten/<ansicht>.png"""
import bpy, bmesh, os, sys, math
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import varianten as VA
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
KEY = argv[0]; VIEWS = argv[1:] or ["persp", "aerial", "front", "rear", "west", "east"]; v = VA.V[KEY]; K = VA.kennzahlen(KEY)
OUT = os.path.join(VA.ROOT, "studie_gebaeudeformen", KEY, "ansichten"); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; M = {}
def mat(name, c, rough=0.7, metal=0.0, spec=0.3):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal; M[name] = m
for n, c, r, me in (("klinker", (0.33, 0.15, 0.11), 0.85, 0), ("holz", (0.60, 0.40, 0.23), 0.6, 0), ("beton", (0.62, 0.62, 0.60), 0.85, 0), ("glas", (0.05, 0.08, 0.10), 0.05, 0), ("rahmen", (0.05, 0.05, 0.06), 0.5, 0.6), ("deck", (0.5, 0.5, 0.5), 0.9, 0), ("milch", (0.62, 0.78, 0.76), 0.3, 0),
                    ("boden", (0.42, 0.41, 0.39), 0.95, 0), ("asphalt", (0.2, 0.2, 0.21), 0.95, 0), ("linie", (0.92, 0.92, 0.9), 0.8, 0), ("grenze", (0.85, 0.15, 0.15), 0.8, 0), ("saeule", (0.78, 0.78, 0.76), 0.7, 0), ("dach", (0.3, 0.3, 0.32), 0.9, 0), ("vordach", (0.06, 0.06, 0.07), 0.5, 0.6)):
    mat(n, c, r, me)
M["grenze"].node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (0.85, 0.1, 0.1, 1); M["grenze"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.6
def X(x): return -x
def box(name, m, x, y, z):
    x0, x1 = x; y0, y1 = y; z0, z1 = z; bm = bmesh.new(); vs = [bm.verts.new((X(a), b, c)) for a in (x0, x1) for b in (y0, y1) for c in (z0, z1)]; bmesh.ops.convex_hull(bm, input=vs); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(M[m]); return o
def cyl(name, m, x, y, z0, z1, r):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=r, radius2=r, depth=z1 - z0); bmesh.ops.translate(bm, verts=bm.verts, vec=(X(x), y, (z0 + z1) / 2)); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(M[m]); return o
Z = VA.Z
def build():
    Zv = v.get("Z", Z)
    box("Gelaende", "boden", (-500, 500), (-500, 500), (-0.4, 0))
    px0, py0, px1, py1 = VA.PLOT
    # Grundstücksgrenze H1 (hypothetisch) als dünne rote Linien am Boden
    for (x0, y0, x1, y1) in ((px0, py0, px1, py0), (px0, py1, px1, py1), (px0, py0, px0, py1), (px1, py0, px1, py1)):
        box("Grenze-H1", "grenze", (min(x0, x1) - 0.12, max(x0, x1) + 0.12), (min(y0, y1) - 0.12, max(y0, y1) + 0.12), (0, 0.03))
    a0 = v.get("asphalt", (0, 18, 32, 29)); box("Stellplatzflaeche-H1", "asphalt", (a0[0], a0[2]), (a0[1], a0[3]), (0, 0.01))
    for st in v.get("stalls", VA.B3["parking"]["stalls"]):
        x0, y0, x1, y1 = st
        for xa in (x0, x1 - 0.08): box("Stellplatz", "linie", (xa, xa + 0.08), (y0, y1), (0.01, 0.025))
    for (x0, y0, x1, y1) in v["eg"]: box("EG", "klinker", (x0, x1), (y0, y1), Zv["EG"])
    for (x0, y0, x1, y1) in v["og1"]:
        box("OG1", "klinker", (x0, x1), (y0, y1), Zv["OG1"]); box("Decke-unter-OG1", "beton", (x0 - 0.04, x1 + 0.04), (y0 - 0.04, y1 + 0.04), (Zv["OG1"][0] - 0.3, Zv["OG1"][0])); box("Decke-ueber-OG1", "beton", (x0 - 0.04, x1 + 0.04), (y0 - 0.04, y1 + 0.04), (Zv["OG1"][1] - 0.3, Zv["OG1"][1])); box("Dachfläche-OG1", "deck", (x0, x1), (y0, y1), (Zv["OG1"][1], Zv["OG1"][1] + 0.03))
    for (x0, y0, x1, y1) in v["st"]:
        box("Staffel", v.get("st_mat", "holz"), (x0, x1), (y0, y1), Zv["ST"]); box("Attika", "beton", (x0 - 0.04, x1 + 0.04), (y0 - 0.04, y1 + 0.04), (Zv["ATT"][0], Zv["ATT"][1])); box("Dach", "dach", (x0, x1), (y0, y1), (Zv["ATT"][1], Zv["ATT"][1] + 0.03))
    # Glasfront EG zum Platz (x 4–32), schematisch
    gf = v.get("glas_front", (4, 32, 0.0)); gh = Zv["EG"][1] - 0.4; box("EG-Glas", "glas", (gf[0], gf[1]), (gf[2] - 0.03, gf[2]), (0, gh)); box("EG-Rahmen-oben", "rahmen", (gf[0], gf[1]), (gf[2] - 0.08, gf[2]), (gh, gh + 0.1))
    for xr in ((4, 17, 19, 31.97) if "glas_front" not in v else [gf[0] + (gf[1] - gf[0]) * i / 8 for i in range(9)]): box("EG-Rahmen", "rahmen", (xr - 0.04, xr + 0.04), (gf[2] - 0.08, gf[2]), (0, gh))
    # schematische Fenster der Wohngeschosse (Modul 5,6 m vorn / 7,0 m hinten, Lage rein schematisch)
    for lvl, (z0, z1) in (("og1", (Zv["OG1"][0] + 0.4, Zv["OG1"][1] - 0.4)), ("st", (Zv["ST"][0] + 0.4, Zv["ST"][1] - 0.6))):
        xs, y0, x1, y1 = v["wohn"][lvl]; L = x1 - xs
        for (face, mod, yface, sgn) in (("v", 5.6, y0, -1), ("h", 7.0, y1, 1)):
            n = int(L // mod); w = L / n if n else 0
            for i in range(n):
                cx = xs + w * (i + 0.5); ww = min(w - 1.8, 4.2)
                box("Fenster", "glas", (cx - ww / 2, cx + ww / 2), ((yface - 0.03, yface) if sgn < 0 else (yface, yface + 0.03)), (z0, z1))
                for xr in (cx - ww / 2, cx + ww / 2): box("Fensterrahmen", "rahmen", (xr - 0.04, xr + 0.04), ((yface - 0.07, yface) if sgn < 0 else (yface, yface + 0.07)), (z0, z1))
    # Balkone zum Platz (A, D): fünf Balkone 2,70 x 1,50 m wie B3
    if v["balkone"] == "front":
        for b in VA.B3["balconies"]:
            x0, _, x1, _ = b["rect"]; box("Balkon", "beton", (x0, x1), (-1.5, 0), (3.2, 3.5)); box("Balkon-Bruestung", "milch", (x0, x1), (-1.5, -1.44), (3.5, 4.6)); box("Balkon-Bruestung", "milch", (x0, x0 + 0.06), (-1.5, 0), (3.5, 4.6)); box("Balkon-Bruestung", "milch", (x1 - 0.06, x1), (-1.5, 0), (3.5, 4.6))
    if v["vordach"]: box("Vordach", "vordach", (6, 30), (-3.6, 0), (3.0, 3.1))
    # Dachterrassen-Brüstungen (Milchglas 1,10 m)
    for (x0, y0, x1, y1) in v["bruestung"]: box("Bruestung", "milch", (min(x0, x1) - 0.04, max(x0, x1) + 0.04), (min(y0, y1) - 0.04, max(y0, y1) + 0.04), (Zv["OG1"][1], Zv["OG1"][1] + 1.1))
    for (x, y) in K["saeulen"]: cyl("Saeule", "saeule", x, y, 0.0, Zv["OG1"][0] - 0.3, 0.2)
build()
# Beleuchtung
def world(vec):
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; nt = w.node_tree; sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.sun_disc = False; sky.sun_direction = vec
    nt.links.new(sky.outputs["Color"], nt.nodes["Background"].inputs["Color"]); nt.nodes["Background"].inputs["Strength"].default_value = 0.55
def sun(vec, energy):
    s = bpy.data.lights.new("sun", "SUN"); s.energy = energy; s.angle = math.radians(2); o = bpy.data.objects.new("sun", s); sc.collection.objects.link(o); o.rotation_euler = Vector(vec).normalized().to_track_quat("Z", "Y").to_euler()
def common(): sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 24; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 4; sc.view_settings.view_transform = "AgX"; sc.view_settings.exposure = -0.5
def persp(name, p, t, lens):
    for o in [o for o in bpy.data.objects if o.type in ("CAMERA", "LIGHT")]: bpy.data.objects.remove(o)
    cam = bpy.data.cameras.new("c"); cam.lens = lens; cam.sensor_width = 36; co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); co.location = (X(p[0]), p[1], p[2]); co.rotation_euler = (Vector((X(t[0]), t[1], t[2])) - co.location).to_track_quat("-Z", "Y").to_euler(); sc.camera = co
    vec = Vector((0.55, -0.55, 0.62)); world(vec); sun(vec, 3.4); common(); sc.render.resolution_x, sc.render.resolution_y = 2000, 1125; sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True)
def ortho(name, side):
    for o in [o for o in bpy.data.objects if o.type in ("CAMERA", "LIGHT")]: bpy.data.objects.remove(o)
    W, Hh, ppm = 42.0, (14.0 if v.get("Z") else 12.5), 50
    if side in ("west", "east"): W = 32.0
    cam = bpy.data.cameras.new("o"); cam.type = "ORTHO"; cam.ortho_scale = W; co = bpy.data.objects.new("o", cam); sc.collection.objects.link(co); sc.camera = co; cz = (6.0 if v.get("Z") else 5.2)
    if side == "front": co.location = (-16, -100, cz); co.rotation_euler = (math.radians(90), 0, 0); vec = Vector((0.5, -0.7, 0.55))
    if side == "rear": co.location = (-16, 100, cz); co.rotation_euler = (math.radians(90), 0, math.radians(180)); vec = Vector((-0.5, 0.7, 0.55))
    if side == "west": co.location = (100, 11.5, cz); co.rotation_euler = (math.radians(90), 0, math.radians(90)); vec = Vector((0.7, 0.5, 0.55))
    if side == "east": co.location = (-100, 11.5, cz); co.rotation_euler = (math.radians(90), 0, math.radians(-90)); vec = Vector((-0.7, -0.4, 0.55))
    world(vec); sun(vec, 3.0); common(); sc.render.resolution_x, sc.render.resolution_y = int(W * ppm), int(Hh * ppm); sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True)
for vw in VIEWS:
    if vw == "persp": persp("persp", (46, -36, 8.0), (15, 7, 4.2), 30)
    elif vw == "aerial": persp("aerial", (58, 50, 28), (14, 9, 3.0), 34)
    else: ortho(vw, vw)
    print("ok", KEY, vw, flush=True)
