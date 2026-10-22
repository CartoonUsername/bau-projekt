"""Gastro-Innenraum aus dem Modell (Grundriss Blatt 21, Layout 'normal'): Gastraum x 4–32, y 0–10, Höhe 3,2 m; Bar x 5–15 / y 8,6–10; 12 Barhocker; Tische 1,2 x 0,8 m mit Stühlen 0,45 m; Fluchtwegfelder und Türen x 17–19 / 29,5–31.
Nicht im Plan und deshalb NICHT dargestellt: Pfeiler/Stützen, Glas-Stahl-Trennung, Bänke. Materialien laut Gestaltungsvorgabe (Olivgrün, Cognac, Bordeaux, Eiche, dunkle geriffelte Barfront, Messing, Mikrozement).
Aufruf: python3 blender_interior.py einfach|tag  -> visualisierungen/higgsfield/renderings/<..>/<modus>_07_gastro.png"""
import bpy, bmesh, os, sys, math
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modell_b3 as MB, texturen_b3 as TX
ROOT = MB.ROOT; HF = os.path.join(ROOT, "visualisierungen", "higgsfield"); TEXDIR = os.path.join(HF, "modelle", "texturen")
FURN = MB.D["furnishing"]["normal"]
MODE = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else (sys.argv[1] if len(sys.argv) > 1 else "tag"); FLAT = MODE == "einfach"
if not os.path.exists(os.path.join(TEXDIR, "klinker.png")): TX.make(TEXDIR)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; M = {}
def mat(name, color, rough=0.6, metal=0.0, emit=None, sheen=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if sheen: b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Sheen Roughness"].default_value = 0.4
    if emit: b.inputs["Emission Color"].default_value = (*emit[:3], 1); b.inputs["Emission Strength"].default_value = emit[3]
    M[name] = m; return m
def imgtex(m, name, bump=0.1, rough=0.6):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); t = nt.nodes.new("ShaderNodeTexImage"); w, h = TX.TILE[name]
    mp.inputs["Scale"].default_value = (1 / w, 1 / w, 1 / h); t.image = bpy.data.images.load(os.path.join(TEXDIR, name + ".png")); t.projection = "BOX"
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], t.inputs["Vector"]); nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = bump; bm.inputs["Distance"].default_value = 0.005; nt.links.new(t.outputs["Color"], bm.inputs["Height"]); nt.links.new(bm.outputs["Normal"], b.inputs["Normal"])
if FLAT:
    for n, c in (("boden", (0.55, 0.40, 0.27)), ("decke", (0.93, 0.92, 0.88)), ("oliv", (0.42, 0.45, 0.30)), ("stahl", (0.1, 0.11, 0.13)), ("eiche", (0.72, 0.58, 0.4)), ("bar", (0.2, 0.14, 0.1)), ("cognac", (0.55, 0.28, 0.14)), ("bordeaux", (0.35, 0.1, 0.12)), ("messing", (0.7, 0.55, 0.25)), ("lampe", (1, 0.9, 0.7)), ("aussen", (0.6, 0.6, 0.58))):
        m = mat(n, c, 1.0, 0.0, (*c, 1.0)); m.diffuse_color = (*c, 1)
else:
    mat("boden", (0.4, 0.4, 0.4), 0.35); imgtex(M["boden"], "mikrozement", 0.05, 0.35); mat("decke", (0.9, 0.88, 0.82), 0.9); mat("oliv", (0.16, 0.21, 0.11), 0.65); mat("stahl", (0.04, 0.042, 0.048), 0.4, 0.7)
    mat("eiche", (0.5, 0.35, 0.2), 0.45); imgtex(M["eiche"], "eiche", 0.05, 0.45); mat("bar", (0.04, 0.035, 0.03), 0.35); mat("cognac", (0.45, 0.2, 0.08), 0.8, 0.0, None, 0.6); mat("bordeaux", (0.22, 0.03, 0.06), 0.8, 0.0, None, 0.6)
    mat("messing", (0.7, 0.5, 0.2), 0.3, 1.0); mat("lampe", (1.0, 0.72, 0.4), 0.5, 0.0, (1.0, 0.7, 0.38, 25.0)); mat("aussen", (0.5, 0.48, 0.45), 0.9); imgtex(M["aussen"], "pflaster", 0.1, 0.9); mat("creme", (0.85, 0.8, 0.7), 0.9)
def X(x): return -x
def box(x, y, z, m, name="b"):
    x0, x1 = x; y0, y1 = y; z0, z1 = z; bm = bmesh.new(); vs = [bm.verts.new((X(a), b, c)) for a in (x0, x1) for b in (y0, y1) for c in (z0, z1)]; bmesh.ops.convex_hull(bm, input=vs); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(M[m]); return o
def cyl(x, y, z0, z1, r, m, name="c"):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=28, radius1=r, radius2=r, depth=z1 - z0); bmesh.ops.translate(bm, verts=bm.verts, vec=(X(x), y, (z0 + z1) / 2)); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(M[m]); return o
x0, x1, y0, y1, H = 4.0, 32.0, 0.0, 10.0, 3.2
box((x0, x1), (y0, y1), (-0.1, 0), "boden"); box((x0, x1), (y0, y1), (H, H + 0.15), "decke")
box((x0 - 0.15, x0), (y0, y1), (0, H), "oliv"); box((x1, x1 + 0.15), (y0, y1), (0, H), "oliv"); box((x0, x1), (y1, y1 + 0.15), (0, H), "oliv")
for k in range(int(28 / 1.4)):   # Paneelfugen: schmale dunkle Leisten alle 1,4 m an der Rückwand
    box((x0 + 1.4 * k - 0.02, x0 + 1.4 * k + 0.02), (y1 - 0.02, y1), (0.0, H), "stahl", "Fuge")
# Platzseite: Glasfront (nur Pfosten sichtbar, Scheibe weggelassen), Pfostenraster 1,4 m ab x 4, Sturzband 3,1–3,2 m
box((x0, x1), (y0 - 0.08, y0 + 0.04), (3.1, H), "stahl", "Sturz"); box((x0, x1), (y0 - 0.08, y0 + 0.04), (-0.02, 0.06), "stahl", "Sockel")
for k in range(21): box((x0 + 1.4 * k - 0.03, x0 + 1.4 * k + 0.03), (y0 - 0.08, y0 + 0.04), (0, 3.1), "stahl", "Pfosten")
for a, b in ((17, 19), (29.5, 31)):
    box((a, b), (y0 - 0.1, y0 + 0.06), (2.4, 2.46), "stahl", "Tuersturz"); box((a, a + 0.06), (y0 - 0.1, y0 + 0.06), (0, 2.4), "stahl", "Tuerrahmen"); box((b - 0.06, b), (y0 - 0.1, y0 + 0.06), (0, 2.4), "stahl", "Tuerrahmen")
# Außenwelt (Platz) vor der Fassade, nur neutral
box((-80, 120), (-80, -0.05), (-0.3, -0.02), "aussen", "Platz")
# Bar
box((5, 15), (9.0, 10), (0, 1.05), "bar", "Bar"); box((4.95, 15.05), (8.9, 10), (1.05, 1.1), "eiche", "Barplatte")
for i in range(int(10 / 0.12)): box((5 + i * 0.12, 5 + i * 0.12 + 0.06), (8.85, 9.0), (0.05, 1.0), "bar", "Riffel")
box((5, 15), (8.85, 8.9), (0.95, 1.0), "messing", "Fussleiste"); box((5.5, 14.5), (9.85, 10.0), (1.3, 2.5), "bar", "Regal")
for i in range(10):
    for j in range(3): box((5.7 + i * 0.9, 6.3 + i * 0.9), (9.7, 9.85), (1.45 + 0.35 * j, 1.47 + 0.35 * j), "messing", "Regalbrett")
for sx, sy in FURN["stools"]: cyl(sx, sy, 0, 0.72, 0.02, "stahl", "Stiel"); cyl(sx, sy, 0.72, 0.8, 0.2, "bordeaux", "Sitz")
for t in FURN["tables"]:
    tx, ty = t["x"], t["y"]; box((tx, tx + 1.2), (ty, ty + 0.8), (0.72, 0.76), "eiche", "Tisch"); box((tx + 0.55, tx + 0.65), (ty + 0.35, ty + 0.45), (0, 0.72), "stahl", "Fuss"); box((tx + 0.3, tx + 0.9), (ty + 0.25, ty + 0.55), (0, 0.02), "stahl", "Platte")
    for cx in (tx + 0.15, tx + 0.6):
        for cy, back in ((ty - 0.45, "n"), (ty + 0.8, "s")):
            box((cx, cx + 0.45), (cy, cy + 0.45), (0.42, 0.48), "cognac", "Sitz"); by = (cy + 0.4, cy + 0.45) if back == "n" else (cy, cy + 0.05); box((cx, cx + 0.45), by, (0.48, 0.9), "cognac", "Lehne")
            for dx in (0.02, 0.4):
                for dy in (0.02, 0.4): box((cx + dx, cx + dx + 0.03), (cy + dy, cy + dy + 0.03), (0, 0.42), "stahl", "Bein")
    cx, cy = tx + 0.6, ty + 0.4; box((cx - 0.005, cx + 0.005), (cy - 0.005, cy + 0.005), (1.9, H), "messing", "Kabel"); cyl(cx, cy, 1.78, 1.95, 0.15, "lampe", "Leuchte")
# Kamera und Licht
cam = bpy.data.cameras.new("c"); cam.lens = 20; cam.sensor_width = 36; co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); co.location = (X(30.5), 1.5, 1.5)
co.rotation_euler = (Vector((X(11.0), 8.0, 1.15)) - co.location).to_track_quat("-Z", "Y").to_euler(); sc.camera = co
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
if FLAT: w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.93, 0.95, 0.98, 1)
else:
    nt = w.node_tree; sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.sun_disc = False; sky.sun_direction = Vector((0.3, -0.6, 0.35)).normalized(); nt.links.new(sky.outputs["Color"], nt.nodes["Background"].inputs["Color"]); nt.nodes["Background"].inputs["Strength"].default_value = 1.0
    s = bpy.data.lights.new("sun", "SUN"); s.energy = 2.0; s.angle = math.radians(3); so = bpy.data.objects.new("sun", s); sc.collection.objects.link(so); so.rotation_euler = Vector((0.3, -0.6, 0.35)).normalized().to_track_quat("Z", "Y").to_euler()
    a = bpy.data.lights.new("fill", "AREA"); a.energy = 500; a.size = 24; a.size_y = 9; ao = bpy.data.objects.new("fill", a); sc.collection.objects.link(ao); ao.location = (X(18), 5, H - 0.05)
sc.render.resolution_x, sc.render.resolution_y = 2400, 1350; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.use_denoising = not FLAT
if FLAT: sc.cycles.samples = 8; sc.cycles.max_bounces = 0; sc.view_settings.view_transform = "Standard"
else: sc.cycles.samples = 64; sc.cycles.max_bounces = 6; sc.view_settings.view_transform = "AgX"; sc.view_settings.exposure = 0.3
outd = os.path.join(HF, "renderings", "07_gastro_innenraum"); os.makedirs(outd, exist_ok=True); sc.render.filepath = os.path.join(outd, f"{MODE}_07_gastro.png"); bpy.ops.render.render(write_still=True); print("ok gastro")
