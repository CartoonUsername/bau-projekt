"""Verbindliches 3D-Modell Baufeld 3 (B3/K), Version 3 – gebaut aus scripts/modell_b3.py (gleiche Quelle wie die Planprüfung), Renderings mit Blender/Cycles.
Szene: x' = -x (Spiegelung, damit eine Kamera von der Platzseite mit Blick +y den Kern x=0 rechts zeigt – Plan als Karte gelesen, wie Blatt 25). Himmelsrichtung unbekannt (C-13).
Aufruf: python3 blender_modell_v3.py <modus> <ansicht...>
  modus  ortho  : flache Ortho-Ansichten (Geometrie-Dokumentation, Maßstab wie Blatt 25)
         tag    : Tageslicht, Materialien    nacht : blaue Stunde, gleiche Kamera
         einfach: neutrales Tonmodell (Farbcode wie Blatt 25)
  ansicht: 01_front 03_rueck 04_west 05_ost 06_luft 08_terrasse   (Kameras stehen in VIEWS, Lichtrichtung je Ansicht)
Ausgabe: visualisierungen/higgsfield/renderings/... (siehe OUT)"""
import bpy, bmesh, os, sys, math, json
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modell_b3 as MB, texturen_b3 as TX
ROOT = MB.ROOT; HF = os.path.join(ROOT, "visualisierungen", "higgsfield")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
VARIANTE = "vorschlag" if "--vorschlag" in argv else "plangetreu"
argv = [a for a in argv if a != "--vorschlag"]
MODE = argv[0]; VIEWS_TO_DO = argv[1:]
RENDER_ROOT = os.path.join(HF, "renderings", "v4")   # Modellversion v4 (nach Korrekturen vom 23.10.2026); ältere Renderings bleiben unberührt
PFX = "vorschlag_" if VARIANTE == "vorschlag" else ""
TEXDIR = os.path.join(HF, "modelle", "texturen")
if MODE in ("tag", "nacht") and not os.path.exists(os.path.join(TEXDIR, "klinker.png")): TX.make(TEXDIR)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
M = {}
def newmat(name, color=(0.5, 0.5, 0.5), rough=0.6, metal=0.0, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit[:3], 1); b.inputs["Emission Strength"].default_value = emit[3]
    M[name] = m; return m
def imgtex(m, name, scale_override=None, rough=0.8, bump=0.25):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); t = nt.nodes.new("ShaderNodeTexImage")
    w, h = TX.TILE[name]; mp.inputs["Scale"].default_value = (1 / w, 1 / w, 1 / h)
    t.image = bpy.data.images.load(os.path.join(TEXDIR, name + ".png")); t.projection = "BOX"; t.projection_blend = 0.0; t.interpolation = "Smart"
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], t.inputs["Vector"]); nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = bump; bm.inputs["Distance"].default_value = 0.01; nt.links.new(t.outputs["Color"], bm.inputs["Height"]); nt.links.new(bm.outputs["Normal"], b.inputs["Normal"]); b.inputs["Roughness"].default_value = rough
FLAT = MODE in ("ortho", "einfach")
if FLAT:   # Farbcode wie Blatt 25
    def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    for n, c in (("klinker", "#C9ADA3"), ("laerche", "#DCC7A4"), ("beton", "#D9DADC"), ("attika", "#8E9399"), ("milch", "#EAF1F3"), ("glas", "#C9DCE6"), ("stahl", "#2B3036"), ("holz", "#E6D9BE"), ("tuer", "#FFFFFF"), ("deck", "#A9ADB3"), ("dach", "#6B7280"), ("boden", "#EEEEEE"), ("asphalt", "#999999"), ("linie", "#FFFFFF"), ("vordach", "#4A4F57")):
        newmat(n, hexc(c), 1.0, 0.0, (*hexc(c), 1.0)).diffuse_color = (*hexc(c), 1.0)   # Farbe bleibt exakt
else:
    newmat("klinker"); imgtex(M["klinker"], "klinker", rough=0.85, bump=0.35)
    newmat("laerche"); imgtex(M["laerche"], "holz", rough=0.55, bump=0.3)
    newmat("beton"); imgtex(M["beton"], "beton", rough=0.85, bump=0.05)
    newmat("attika", (0.34, 0.35, 0.37), 0.5, 0.4); newmat("dach", (0.22, 0.22, 0.23), 0.9)
    newmat("glas", (0.02, 0.035, 0.045), 0.03, 0.0); M["glas"].node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.5
    newmat("milch", (0.55, 0.72, 0.70), 0.28); M["milch"].node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 0.8; M["milch"].node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.45
    newmat("stahl", (0.04, 0.042, 0.048), 0.45, 0.7); newmat("holz", (0.56, 0.42, 0.26), 0.55); newmat("tuer", (0.04, 0.042, 0.048), 0.45, 0.7)
    newmat("deck", (0.5, 0.5, 0.5), 0.85); imgtex(M["deck"], "beton", rough=0.85, bump=0.03); newmat("boden"); imgtex(M["boden"], "pflaster", rough=0.9, bump=0.2); newmat("asphalt"); imgtex(M["asphalt"], "asphalt", rough=0.95, bump=0.1)
    newmat("linie", (0.9, 0.9, 0.88), 0.8); newmat("vordach", (0.05, 0.05, 0.055), 0.45, 0.7); newmat("gelaende", (0.42, 0.42, 0.40), 0.95)
    # beleuchtete Fenster (nur Nacht): Gastro warm, einzelne Wohnungsfenster dezent
    newmat("glas_gastro", (0.02, 0.02, 0.02), 0.1, 0.0, (1.0, 0.62, 0.30, 3.2 if MODE == "nacht" else 0.0)); newmat("glas_wohnen", (0.02, 0.02, 0.02), 0.1, 0.0, (1.0, 0.72, 0.45, 1.3 if MODE == "nacht" else 0.0))
    for k in ("glas_gastro", "glas_wohnen"): M[k].node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.5
    if MODE != "nacht":
        for k in ("glas_gastro", "glas_wohnen"): M[k] = M["glas"]
NIGHT_LIT = {"OG1-Fenster-1", "OG1-Fenster-3", "OG1-Fenster-4", "Staffel-WE-L2-V2", "OG1-hinten-WE-L1-H2", "Staffel-hinten-WE-L2-H1", "Ost-OG1"}
def X(x): return -x
OBJS = []
def mesh_box(name, mat, x, y, z, grow=0.0):
    x0, x1 = x; y0, y1 = y; z0, z1 = z; x0 -= grow; y0 -= grow; z0 -= grow; x1 += grow; y1 += grow; z1 += grow
    bm = bmesh.new(); vs = [bm.verts.new((X(a), b, c)) for a in (x0, x1) for b in (y0, y1) for c in (z0, z1)]
    bmesh.ops.convex_hull(bm, input=vs); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(M[mat]); OBJS.append(o); return o
def panel(side, a, z, pos, depth, name, mat):
    """dünnes Bauteil auf einer Fassade; depth = Ausladung nach außen (negativ: nach innen)"""
    d0, d1 = (pos - depth, pos) if side in ("-y", "-x") else (pos, pos + depth)
    if depth < 0: d0, d1 = (pos, pos - depth) if side in ("-y", "-x") else (pos + depth, pos)
    if side in ("-y", "+y"): return mesh_box(name, mat, a, (d0, d1), z)
    return mesh_box(name, mat, (d0, d1), a, z)
def build():
    ground = "boden" if not FLAT else "boden"
    mesh_box("Gelaende", "boden", (-700, 700), (-700, 700), (-0.4, 0.0))
    mesh_box("Asphalt", "asphalt", (0, 32), (18, 29), (-0.02, 0.006))
    for st in MB.stalls():
        x0, y0, x1, y1 = st
        for xa in (x0, x1 - 0.08): mesh_box("Stellplatzlinie", "linie", (xa, xa + 0.08), (y0, y1), (0, 0.012))
    for b in MB.boxes(): mesh_box(b["name"], "klinker" if b["mat"] == "klinker" else "laerche", b["x"], b["y"], b["z"])
    for b in MB.bands(): mesh_box(b["name"], "beton", b["x"], b["y"], b["z"], grow=0.004)
    for b in MB.attika(): mesh_box(b["name"], "attika", b["x"], b["y"], b["z"], grow=0.002)
    mesh_box("Dach", "dach", (0.8, 31.2), (0.8, MB.Y2), (9.9, 9.93))
    t = MB.roof_terrace(); mesh_box("Dachterrasse-Deck", "deck", t["x"], t["y"], (6.5, 6.53))
    P = 0.06
    mesh_box("Bruestung-hinten", "milch", (t["x"][0], t["x"][1]), (MB.Y1 - P, MB.Y1), (6.5, 7.6)); mesh_box("Bruestung-Ost", "milch", (t["x"][1] - P, t["x"][1]), (t["y"][0], MB.Y1), (6.5, 7.6)); mesh_box("Bruestung-West", "milch", (t["x"][0], t["x"][0] + P), (t["y"][0], MB.Y1), (6.5, 7.6))
    for bal in MB.balconies():
        x, y = bal["x"], bal["y"]; mesh_box("Balkonplatte", "beton", x, y, (3.2, 3.5)); mesh_box("Balkon-vorn", "milch", x, (y[0], y[0] + P), (3.5, 4.6)); mesh_box("Balkon-W", "milch", (x[0], x[0] + P), y, (3.5, 4.6)); mesh_box("Balkon-O", "milch", (x[1] - P, x[1]), y, (3.5, 4.6))
    v = MB.vordach(); mesh_box("Vordach", "vordach", v["x"], v["y"], v["z"])
    # Abluftstutzen: Dachaustritt offen (C-22), wird nicht gebaut; der Schacht liegt im Gebäude (MB.shaft())
    rt = MB.rahmenteilung()
    for xr in ([] if FLAT else rt["x"]): panel("-y", (xr - 0.035, xr + 0.035), (0.0, 3.1), 0.0, 0.08, "Rahmenteilung-konzeptionell", "rahmen" if "rahmen" in M else "stahl")
    for o in MB.openings(VARIANTE):
        side, (a0, a1), (z0, z1), pos = o["side"], o["a"], o["z"], o["pos"]; fr = "holz" if o["frame"] == "holz" else "stahl"; w = 0.07 if o["kind"] == "glas" else 0.1
        gm = "glas"
        if not FLAT and MODE == "nacht": gm = "glas_gastro" if o["tag"] in ("EG-Verglasung", "Doppeltür Gastro", "Tür Gastro Ost") else ("glas_wohnen" if o["tag"] in NIGHT_LIT else "glas")
        if FLAT: gm = "glas" if o["kind"] == "glas" else "tuer"; fr = "stahl" if o["frame"] == "stahl" else "holz"
        if FLAT and o["tag"] == "EG-Verglasung": panel(side, (a0, a1), (z0, z1), pos, 0.02, "EG-Verglasung", "glas"); continue
        if FLAT and o["kind"] == "tuer" and o["tag"] != "Ost-Tür-EG": panel(side, (a0, a1), (z0, z1), pos, 0.05, o["tag"], "tuer"); continue
        if FLAT and o["tag"] == "Ost-Tür-EG": panel(side, (a0, a1), (z0, z1), pos, 0.05, o["tag"], "stahl"); continue
        if FLAT and o["tag"] in ("EG-hinten",): panel(side, (a0, a1), (z0, z1), pos, 0.05, o["tag"], "stahl"); panel(side, (a0 + 0.12, a1 - 0.12), (z0 + 0.12, z1 - 0.12), pos, 0.06, o["tag"] + "-glas", "glas"); continue
        panel(side, (a0, a1), (z0, z1), pos, 0.02, o["tag"] + "-Glas", gm)
        d = 0.09; panel(side, (a0, a1), (z0, z0 + w), pos, d, o["tag"] + "-u", fr); panel(side, (a0, a1), (z1 - w, z1), pos, d, o["tag"] + "-o", fr); panel(side, (a0, a0 + w), (z0, z1), pos, d, o["tag"] + "-l", fr); panel(side, (a1 - w, a1), (z0, z1), pos, d, o["tag"] + "-r", fr)
        n = o["div"]
        for i in range(1, n): a = a0 + (a1 - a0) * i / n; panel(side, (a - w / 2, a + w / 2), (z0, z1), pos, d * 0.8, o["tag"] + "-p", fr)
        if o["kind"] == "tuer": panel(side, (a0, a1), (z0 + 1.0, z0 + 1.0 + w), pos, d * 0.8, o["tag"] + "-q", fr)
build()
os.makedirs(os.path.join(HF, "modelle"), exist_ok=True)
if MODE == "einfach" and not VIEWS_TO_DO: pass
# Kameras (Modellkoordinaten): Position, Ziel, Brennweite (Kleinbild 36 mm), Sonnenrichtung (Azimut Grad im Modell, Höhe Grad)
VIEWS = {"01_front": dict(p=(46, -34, 1.8), t=(19, 4, 4.4), lens=38, sun=(-35, 38)), "03_rueck": dict(p=(-14, 52, 2.4), t=(17, 14, 4.6), lens=36, sun=(-60, 40)), "04_west": dict(p=(-40, -4, 2.2), t=(4, 9, 4.6), lens=36, sun=(-70, 40)),
         "05_ost": dict(p=(72, 24, 2.2), t=(30, 9, 4.6), lens=36, sun=(-65, 40)), "06_luft": dict(p=(70, 58, 25), t=(14, 10, 3.0), lens=36, sun=(-50, 45)), "08_terrasse": dict(p=(22, 33, 14.5), t=(17, 19.8, 7.2), lens=30, sun=(-50, 45))}
def world_sky(night, sunvec):
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes["Background"]; sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
    sky.sun_disc = False; sky.sun_direction = sunvec; sky.air_density = 1.0
    if night:   # Abendhimmel: Verlauf von warmem Horizont zu dunklem Blau (Sky-Textur ist unter dem Horizont nicht brauchbar)
        tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); mr = nt.nodes.new("ShaderNodeMapRange"); ramp = nt.nodes.new("ShaderNodeValToRGB")
        mr.inputs["From Min"].default_value = 0.0; mr.inputs["From Max"].default_value = 0.7; ramp.color_ramp.elements[0].color = (0.30, 0.34, 0.50, 1); ramp.color_ramp.elements[1].color = (0.015, 0.03, 0.09, 1)
        nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"]); nt.links.new(sep.outputs["Z"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.9
    else: nt.links.new(sky.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0
def setup_light(view, night):
    az, el = view["sun"]
    if night: el = -4.0
    # Sonnenvektor in Szenenkoordinaten (x' gespiegelt); Azimut relativ zur Blickrichtung der Kamera
    p, t = view["p"], view["t"]; d = Vector((X(t[0]) - X(p[0]), t[1] - p[1], 0)); d.normalize(); a = math.radians(az); sh = Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), 0)) * -1
    e = math.radians(el); vec = Vector((sh.x * math.cos(e), sh.y * math.cos(e), math.sin(e))); vec.normalize()
    world_sky(night, vec)
    if not night:
        s = bpy.data.lights.new("sun", "SUN"); s.energy = 4.5; s.angle = math.radians(1.2); so = bpy.data.objects.new("sun", s); sc.collection.objects.link(so); so.rotation_euler = (-vec).to_track_quat("-Z", "Y").to_euler() if False else Vector(vec).to_track_quat("Z", "Y").to_euler()
def camera(view):
    cam = bpy.data.cameras.new("c"); cam.lens = view["lens"]; cam.sensor_width = 36; co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); p, t = view["p"], view["t"]
    co.location = (X(p[0]), p[1], p[2]); co.rotation_euler = (Vector((X(t[0]), t[1], t[2])) - co.location).to_track_quat("-Z", "Y").to_euler(); sc.camera = co; return co
# Ortho-Prüfansichten im Maßstab von Blatt 25 (47,244 px je m = 11,811 px/mm x 4 mm/m)
PXM = 11.811 * 4.0
ORTHO = {"front": dict(side=-1), "rear": dict(), "west": dict(), "east": dict()}
def ortho(view, out, region):
    """region = (a0, a1, z0, z1) in Metern (a wie elev3: front 32-x, rear x, west y, east 21-y)"""
    a0, a1, z0, z1 = region; wpx, hpx = int(round((a1 - a0) * PXM)), int(round((z1 - z0) * PXM)); ca, cz = (a0 + a1) / 2, (z0 + z1) / 2
    cam = bpy.data.cameras.new("o"); cam.type = "ORTHO"; cam.ortho_scale = (a1 - a0); co = bpy.data.objects.new("o", cam); sc.collection.objects.link(co); sc.camera = co
    if view == "front": co.location = (-(32 - ca), -100, cz); co.rotation_euler = (math.radians(90), 0, 0)
    if view == "rear": co.location = (-ca, 100, cz); co.rotation_euler = (math.radians(90), 0, math.radians(180))
    if view == "west": co.location = (100, ca, cz); co.rotation_euler = (math.radians(90), 0, math.radians(90))
    if view == "east": co.location = (-100, MB.Y1 - ca, cz); co.rotation_euler = (math.radians(90), 0, math.radians(-90))
    sc.render.resolution_x, sc.render.resolution_y = wpx, hpx; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4; sc.cycles.use_denoising = False; sc.cycles.max_bounces = 0; sc.cycles.filter_width = 0.8
    sc.view_settings.view_transform = "Standard"; sc.render.filepath = out; bpy.ops.render.render(write_still=True)
if MODE == "ortho":
    outd = os.path.join(RENDER_ROOT, "00_geometrie_ortho"); os.makedirs(outd, exist_ok=True)
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    for v, reg in (("front", (-1, 33, -0.3, 10.5)), ("rear", (-1, 33, -0.3, 10.5)), ("west", (-1, 22, -0.3, 10.5)), ("east", (-1, 22, -0.3, 10.5))):
        if VIEWS_TO_DO and v not in VIEWS_TO_DO: continue
        ortho(v, os.path.join(outd, f"{PFX}ortho_{v}.png"), reg); print("ok", v)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HF, "modelle", f"baufeld3_B3_{MB.MODEL_VERSION}{'_vorschlag' if VARIANTE == 'vorschlag' else ''}.blend")); sys.exit(0)
outd = os.path.join(RENDER_ROOT, {"einfach": "00_geometrie_neutral", "tag": "tag", "nacht": "nacht"}[MODE]); os.makedirs(outd, exist_ok=True)
for name in VIEWS_TO_DO:
    for o in [o for o in bpy.data.objects if o.type in ("LIGHT", "CAMERA")]: bpy.data.objects.remove(o)
    v = VIEWS[name]; camera(v); sc.render.resolution_x, sc.render.resolution_y = 2400, 1350
    if FLAT:
        sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 8; sc.cycles.use_denoising = False; sc.cycles.max_bounces = 0
        w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.93, 0.95, 0.98, 1); sc.view_settings.view_transform = "Standard"
    else:
        sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 56; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 4; sc.cycles.transmission_bounces = 4
        setup_light(v, MODE == "nacht"); sc.view_settings.view_transform = "AgX"; sc.view_settings.exposure = -0.4 if MODE == "tag" else 0.2
        try: sc.view_settings.look = "AgX - Medium High Contrast"
        except Exception as e: print("look", e)
    sc.render.filepath = os.path.join(outd, f"{PFX}{MODE}_{name}.png"); bpy.ops.render.render(write_still=True); print("ok", name, flush=True)
    json.dump(dict(view=name, camera=v["p"], target=v["t"], lens_mm=v["lens"], sensor_mm=36, sun_azimut_rel=v["sun"][0], sun_hoehe=v["sun"][1], modus=MODE, variante=VARIANTE, modellversion=MB.MODEL_VERSION), open(os.path.join(outd, f"{PFX}{MODE}_{name}.camera.json"), "w"))
