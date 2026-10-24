"""Verbindliches 3D-Modell Baufeld 3 (B3, Alternative K) in Blender (bpy) – Quelle der Wahrheit für alle Außenansichten.
Geometrie ausschließlich aus geometry/variant_B3.json (+ Öffnungen wie in scripts/render_ref.py). Koordinaten Modell: x West->Ost, y Platzfassade->Rückseite, z oben.
Szene wird in Blender mit x' = -x aufgebaut, damit eine Kamera von der Platzseite (Blick +y) den Kern (x=0) rechts zeigt (Plan als Karte gelesen, Platz im Norden).
Aufruf: python3 blender_model.py <modus> <ansicht...>   modus: clay | mat | night ; ansicht: 01_front 03_rueck 04_west 05_ost 06_luft 08_terrasse
Ausgabe: visualisierungen/higgsfield/referenzen/<modus>_<ansicht>.png und modelle/baufeld3_B3.blend/.glb"""
import bpy, bmesh, json, os, sys, math
from mathutils import Vector
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HF = os.path.join(ROOT, "visualisierungen", "higgsfield")
D = json.load(open(os.path.join(ROOT, "geometry", "variant_B3.json"))); V = D["variants"]["K"]
Y1, Y2 = V["depth_L1"], V["y2"]
MODE = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else (sys.argv[1] if len(sys.argv) > 1 else "mat")
ARGS = sys.argv[sys.argv.index("--") + 2:] if "--" in sys.argv else sys.argv[2:]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
MAT = {}
def mat(name, color, rough=0.6, metal=0.0, trans=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if trans: b.inputs["Transmission Weight"].default_value = trans
    MAT[name] = m; return m
def tex_brick(m, c1, c2, mortar, scale=1.0):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; t = nt.nodes.new("ShaderNodeTexBrick"); tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1, 1, 1); t.inputs["Color1"].default_value = (*c1, 1); t.inputs["Color2"].default_value = (*c2, 1); t.inputs["Mortar"].default_value = (*mortar, 1)
    t.inputs["Scale"].default_value = 4.0 * scale; t.inputs["Mortar Size"].default_value = 0.012; t.inputs["Brick Width"].default_value = 0.5; t.inputs["Row Height"].default_value = 0.25 * 0.5 / 0.5
    t.inputs["Bias"].default_value = 0.0; t.offset = 0.5
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], t.inputs["Vector"]); nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.4; nt.links.new(t.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
def tex_wood(m, c1, c2, scale=22.0):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; tc = nt.nodes.new("ShaderNodeTexCoord"); w = nt.nodes.new("ShaderNodeTexWave"); ramp = nt.nodes.new("ShaderNodeValToRGB"); n = nt.nodes.new("ShaderNodeTexNoise")
    w.wave_type = "BANDS"; w.bands_direction = "X"; w.inputs["Scale"].default_value = scale; w.inputs["Distortion"].default_value = 1.5; w.inputs["Detail"].default_value = 3
    ramp.color_ramp.elements[0].color = (*c1, 1); ramp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(tc.outputs["Object"], w.inputs["Vector"]); nt.links.new(w.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.25; nt.links.new(w.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
def tex_noise(m, c1, c2, scale=8.0, bump=0.1):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; tc = nt.nodes.new("ShaderNodeTexCoord"); n = nt.nodes.new("ShaderNodeTexNoise"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = 8; ramp.color_ramp.elements[0].color = (*c1, 1); ramp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"]); nt.links.new(n.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = bump; nt.links.new(n.outputs["Fac"], bm.inputs["Height"]); nt.links.new(bm.outputs["Normal"], b.inputs["Normal"])
clay = MODE == "clay"
def make_mats():
    if clay:
        for n, c in (("klinker", (0.36, 0.2, 0.17)), ("holz", (0.71, 0.55, 0.36)), ("beton", (0.74, 0.74, 0.73)), ("glas", (0.55, 0.72, 0.8)), ("rahmen", (0.1, 0.11, 0.13)), ("milch", (0.86, 0.91, 0.93)), ("asphalt", (0.28, 0.28, 0.29)), ("pflaster", (0.66, 0.65, 0.62)), ("deck", (0.62, 0.48, 0.32)), ("attika", (0.55, 0.56, 0.58)), ("dach", (0.45, 0.45, 0.47)), ("linie", (0.9, 0.9, 0.9)), ("tuer", (0.85, 0.88, 0.9)), ("holzfenster", (0.84, 0.74, 0.55))): mat(n, c, 0.9)
        return
    mat("klinker", (0.3, 0.12, 0.09), 0.85); tex_brick(MAT["klinker"], (0.26, 0.10, 0.075), (0.36, 0.15, 0.11), (0.45, 0.43, 0.40), 1.0)
    mat("holz", (0.5, 0.33, 0.2), 0.6); tex_wood(MAT["holz"], (0.42, 0.26, 0.14), (0.60, 0.40, 0.24), 26.0)
    mat("beton", (0.6, 0.6, 0.58), 0.8); tex_noise(MAT["beton"], (0.5, 0.5, 0.49), (0.66, 0.66, 0.64), 6.0, 0.05)
    mat("glas", (0.7, 0.85, 0.9), 0.05, 0, 1.0); MAT["glas"].node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.05
    mat("rahmen", (0.07, 0.075, 0.085), 0.45, 0.6)
    mat("milch", (0.82, 0.9, 0.9), 0.35, 0, 0.55)
    mat("asphalt", (0.16, 0.16, 0.17), 0.95); tex_noise(MAT["asphalt"], (0.12, 0.12, 0.13), (0.2, 0.2, 0.21), 60.0, 0.1)
    mat("pflaster", (0.55, 0.53, 0.5), 0.9); tex_brick(MAT["pflaster"], (0.55, 0.53, 0.5), (0.45, 0.43, 0.41), (0.3, 0.3, 0.3), 0.6)
    mat("deck", (0.45, 0.32, 0.2), 0.8); tex_wood(MAT["deck"], (0.38, 0.27, 0.17), (0.5, 0.36, 0.22), 18.0)
    mat("attika", (0.5, 0.5, 0.5), 0.5, 0.5); mat("dach", (0.25, 0.25, 0.26), 0.9); mat("linie", (0.92, 0.92, 0.9), 0.8); mat("tuer", (0.1, 0.1, 0.11), 0.4, 0.5); mat("holzfenster", (0.62, 0.45, 0.28), 0.55)
make_mats()
def X(x): return -x
objs = []
def box(x0, x1, y0, y1, z0, z1, m, name="b"):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    xa, xb = sorted((X(x0), X(x1))); o.location = ((xa + xb) / 2, (y0 + y1) / 2, (z0 + z1) / 2); o.scale = (xb - xa, y1 - y0, z1 - z0)
    o.data.materials.append(MAT[m]); objs.append(o); return o
def face(side, a0, a1, z0, z1, pos, m, depth=0.04):
    """Flächiges Bauteil auf der Fassade; side -y/+y/-x/+x; a = Koordinate entlang; pos = Fassadenebene; Tiefe nach außen"""
    if side == "-y": return box(a0, a1, pos - depth, pos, z0, z1, m)
    if side == "+y": return box(a0, a1, pos, pos + depth, z0, z1, m)
    if side == "-x": return box(pos - depth, pos, a0, a1, z0, z1, m)
    if side == "+x": return box(pos, pos + depth, a0, a1, z0, z1, m)
def window(side, a0, a1, z0, z1, pos, glass="glas", div=None, frame=0.07, fm="rahmen"):
    """Fenster/Tür: dunkler Rahmen vor der Wand (Tiefe 0,10), Glas dahinter, optional Pfosten (div = Anzahl Felder)"""
    d = 0.10; face(side, a0, a1, z0, z1, pos, glass, 0.02)
    face(side, a0, a1, z0, z0 + frame, pos, fm, d); face(side, a0, a1, z1 - frame, z1, pos, fm, d); face(side, a0, a0 + frame, z0, z1, pos, fm, d); face(side, a1 - frame, a1, z0, z1, pos, fm, d)
    if div:
        for i in range(1, div): a = a0 + (a1 - a0) * i / div; face(side, a - frame / 2, a + frame / 2, z0, z1, pos, fm, d * 0.8)
def build():
    # Gelände: neutrale Fläche, Platz (Pflaster) vor und seitlich, Asphalt im rückwärtigen Bereich (hypothetische Fläche H1, nicht bestätigt)
    box(-600, 600, -600, 0, -0.3, 0, "pflaster"); box(-600, 0, 0, 600, -0.3, 0, "pflaster"); box(32, 600, 0, 600, -0.3, 0, "pflaster"); box(0, 32, 18, 600, -0.3, 0, "pflaster"); box(0, 32, 18, 29, -0.29, 0.001, "asphalt")
    box(0, 32, 0, 18, 0, 3.5, "klinker", "EG"); box(0, 32, 0, 18, 3.5, 6.5, "klinker", "OG1"); box(4, 32, 18, Y1, 3.5, 6.5, "klinker", "OG1-Rueck")
    box(0.8, 31.2, 0.8, 17.2, 6.5, 9.6, "holz", "Staffel"); box(4.2, 31.2, 17.2, Y2, 6.5, 9.6, "holz", "Staffel-Rueck")
    for (x0, x1, y0, y1, z) in ((0, 32, 0, 18, 3.2), (4, 32, 18, Y1, 3.2), (0, 32, 0, 18, 6.2), (4, 32, 18, Y1, 6.2)): box(x0 - 0.04, x1 + 0.04, y0 - 0.04, y1 + 0.04, z, z + 0.3, "beton", "Deckenband")
    box(0.76, 31.24, 0.76, 17.24, 9.6, 9.9, "attika", "Attika"); box(4.16, 31.24, 17.2, Y2 + 0.04, 9.6, 9.9, "attika", "Attika-Rueck")
    box(0.8, 31.2, 0.8, Y2, 9.9, 9.92, "dach", "Dach")
    box(4, 32, 18, Y1, 6.5, 6.52, "deck", "Dachterrasse-Deck")
    box(4, 32, Y1 - 0.06, Y1, 6.5, 7.6, "milch", "Bruestung-R"); box(31.94, 32, Y2, Y1, 6.5, 7.6, "milch", "Bruestung-O"); box(4, 4.06, Y2, Y1, 6.5, 7.6, "milch", "Bruestung-W")
    # Platzseite
    window("-y", 4, 32, 0, 3.1, 0, "glas");
    import numpy as np
    for x in np.arange(5.4, 32, 1.4): face("-y", x - 0.03, x + 0.03, 0, 3.1, 0, "rahmen", 0.08)
    face("-y", 4, 32, 3.1, 3.2, 0, "rahmen", 0.08)
    for a, b in ((17, 19), (29.5, 31)): face("-y", a, b, 0, 2.4, 0, "tuer", 0.12)
    window("-y", 1.0, 2.5, 0, 2.4, 0, "glas")
    for b in V["balconies"]:
        x0, _, x1, _ = b["rect"]; box(x0, x1, -1.5, 0, 3.2, 3.5, "beton", "Balkon"); box(x0, x1, -1.5, -1.44, 3.5, 4.6, "milch"); box(x0, x0 + 0.06, -1.5, 0, 3.5, 4.6, "milch"); box(x1 - 0.06, x1, -1.5, 0, 3.5, 4.6, "milch")
    for i in range(5): x0 = 4 + 5.6 * i; window("-y", x0 + 0.9, x0 + 4.7, 3.9, 6.1, 0, "glas", 2)
    for r in V["rooms"]:
        if r["id"].startswith("WE-L2-V"): x0, x1 = r["rect"][0], r["rect"][2]; window("-y", x0 + 1.0, x1 - 1.0, 6.9, 9.0, 0.8, "glas", 2, fm="holzfenster")
    box(6, 30, -3.6, 0, 3.0, 3.1, "rahmen", "Vordach");
    # Rückseite (L1-Anbau y=Y1, Staffel-Anbau y=Y2, EG y=18)
    for r in V["rooms"]:
        if r["id"].startswith("WE-L1-H"): x0 = r["rect"][0]; window("+y", x0 + 1.6, x0 + 5.4, 3.9, 6.1, Y1, "glas", 2)
        if r["id"].startswith("WE-L2-H"): x0 = r["rect"][0]; window("+y", x0 + 1.6, x0 + 7.4, 6.6, 9.1, Y2, "glas", 2, fm="holzfenster")
    for a, b in ((5.0, 6.5), (15.0, 16.5), (1.0, 2.5)): window("+y", a, b, 0, 2.4, 18.0, "glas")
    # Seiten
    window("-x", 6.5, 7.5, 0.9, 3.0, 0, "glas"); window("-x", 6.5, 7.5, 3.9, 6.1, 0, "glas"); window("-x", 6.5, 7.5, 6.9, 9.1, 0.8, "glas", fm="holzfenster")
    window("+x", 11.5, 13.5, 4.4, 6.0, 32, "glas"); window("+x", 11.5, 13.5, 7.4, 9.0, 31.2, "glas", fm="holzfenster"); window("+x", 16.7, 17.9, 0, 2.4, 32, "glas")
    # Stellplatzmarkierung (11 Stellplätze 2,5 x 5,0 m, Fahrgasse 6 m – hypothetisch)
    for st in V["parking"]["stalls"]:
        x0, y0, x1, y1 = st
        for xa in (x0, x1 - 0.08): box(xa, xa + 0.08, y0, y1, 0, 0.012, "linie", "Stellplatz")
build()
# Export Modell (Quelle der Wahrheit)
os.makedirs(os.path.join(HF, "modelle"), exist_ok=True)
if MODE == "clay":
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HF, "modelle", "baufeld3_B3.blend")); bpy.ops.export_scene.gltf(filepath=os.path.join(HF, "modelle", "baufeld3_B3.glb"))
# Kameras: (Position, Ziel, Brennweite mm) im Modellkoordinatensystem (x West->Ost)
VIEWS = {"01_front": ((46, -34, 1.8), (19, 4, 4.4), 38), "03_rueck": ((-14, 52, 2.4), (17, 14, 4.6), 40), "04_west": ((-40, -4, 2.2), (4, 9, 4.6), 40), "05_ost": ((72, 24, 2.2), (30, 9, 4.6), 40),
         "06_luft": ((70, 58, 25), (14, 10, 3.0), 38), "08_terrasse": ((22, 33, 14.5), (17, 19.8, 7.2), 30)}
def setup_world(night=False):
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.sun_elevation = math.radians(8 if night else 38); sky.sun_rotation = math.radians(200); sky.sun_disc = False; sky.sun_intensity = 0.0
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.35 if night else 0.9
def night_flag(): return MODE == "night"
def render(view, out):
    p, t, lens = VIEWS[view]; cam = bpy.data.cameras.new("c"); cam.lens = lens; cam.sensor_width = 36; co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co)
    co.location = (X(p[0]), p[1], p[2]); d = Vector((X(t[0]), t[1], t[2])) - co.location; co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); sc.camera = co
    sc.render.resolution_x, sc.render.resolution_y = 2400, 1350
    if clay:
        sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 12; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 2
    else:
        sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 40; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6
    sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = -2.6
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 2.2 if not night_flag() else 0.0; sun.angle = math.radians(4); so = bpy.data.objects.new("sun", sun); sc.collection.objects.link(so)
    tgt = Vector((X(t[0]), t[1], t[2])); v = co.location - tgt; v.z = 0; v.normalize(); a = math.radians(38); vr = Vector((v.x * math.cos(a) - v.y * math.sin(a), v.x * math.sin(a) + v.y * math.cos(a), 0)); el = math.radians(40)
    pos = tgt + Vector((vr.x * math.cos(el), vr.y * math.cos(el), math.sin(el))) * 100; so.location = pos; so.rotation_euler = (tgt - pos).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = out; bpy.ops.render.render(write_still=True)
setup_world(MODE == "night")
if not clay:
    # Sonne zusätzlich als weiches Licht (Tageslicht)
    pass
os.makedirs(os.path.join(HF, "referenzen"), exist_ok=True)
for v in ARGS or []:
    if v in VIEWS: render(v, os.path.join(HF, "referenzen", f"{MODE}_{v}.png")); print("ok", v)
