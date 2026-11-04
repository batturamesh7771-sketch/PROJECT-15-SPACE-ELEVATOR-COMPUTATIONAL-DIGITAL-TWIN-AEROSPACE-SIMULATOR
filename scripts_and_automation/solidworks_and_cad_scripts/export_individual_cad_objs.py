import os
import math

models_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\models"
os.makedirs(models_dir, exist_ok=True)

class ObjBuilder:
    def __init__(self, name, mtl_name):
        self.name = name
        self.mtl_name = mtl_name
        self.vertices = []
        self.normals = []
        self.faces = []

    def add_vertex(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices)

    def add_normal(self, nx, ny, nz):
        l = math.hypot(nx, ny, nz) or 1.0
        self.normals.append((nx/l, ny/l, nz/l))
        return len(self.normals)

    def add_quad(self, v1, v2, v3, v4, n1, n2, n3, n4, mat):
        self.faces.append(([v1, v2, v3], [n1, n2, n3], mat))
        self.faces.append(([v1, v3, v4], [n1, n3, n4], mat))

    def add_tri(self, v1, v2, v3, n1, n2, n3, mat):
        self.faces.append(([v1, v2, v3], [n1, n2, n3], mat))

    def add_cylinder(self, r, y_min, y_max, cx=0.0, cz=0.0, segments=36, mat="Default"):
        top_v, bot_v, top_n, bot_n = [], [], [], []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            ca, sa = math.cos(angle), math.sin(angle)
            top_v.append(self.add_vertex(cx + r * ca, y_max, cz + r * sa))
            bot_v.append(self.add_vertex(cx + r * ca, y_min, cz + r * sa))
            top_n.append(self.add_normal(ca, 0.0, sa))
            bot_n.append(self.add_normal(ca, 0.0, sa))

        for i in range(segments):
            nxt = (i + 1) % segments
            self.add_quad(bot_v[i], top_v[i], top_v[nxt], bot_v[nxt],
                          bot_n[i], top_n[i], top_n[nxt], bot_n[nxt], mat)

    def add_box(self, min_x, max_x, min_y, max_y, min_z, max_z, mat="Default"):
        p = [
            (min_x, min_y, min_z), (max_x, min_y, min_z),
            (max_x, max_y, min_z), (min_x, max_y, min_z),
            (min_x, min_y, max_z), (max_x, min_y, max_z),
            (max_x, max_y, max_z), (min_x, max_y, max_z)
        ]
        v = [self.add_vertex(pt[0], pt[1], pt[2]) for pt in p]
        nx_neg = self.add_normal(-1, 0, 0)
        nx_pos = self.add_normal(1, 0, 0)
        ny_neg = self.add_normal(0, -1, 0)
        ny_pos = self.add_normal(0, 1, 0)
        nz_neg = self.add_normal(0, 0, -1)
        nz_pos = self.add_normal(0, 0, 1)

        self.add_quad(v[0], v[3], v[2], v[1], nz_neg, nz_neg, nz_neg, nz_neg, mat)
        self.add_quad(v[4], v[5], v[6], v[7], nz_pos, nz_pos, nz_pos, nz_pos, mat)
        self.add_quad(v[0], v[4], v[7], v[3], nx_neg, nx_neg, nx_neg, nx_neg, mat)
        self.add_quad(v[1], v[2], v[6], v[5], nx_pos, nx_pos, nx_pos, nx_pos, mat)
        self.add_quad(v[0], v[1], v[5], v[4], ny_neg, ny_neg, ny_neg, ny_neg, mat)
        self.add_quad(v[3], v[7], v[6], v[2], ny_pos, ny_pos, ny_pos, ny_pos, mat)

    def add_oriented_box(self, center_x, center_z, angle_rad, length, width, height, y_center, mat="Default"):
        half_l = length * 0.5
        half_w = width * 0.5
        half_h = height * 0.5
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        px = -sin_a
        pz = cos_a

        pts_2d = [
            (-half_l, -half_w), (half_l, -half_w), (half_l, half_w), (-half_l, half_w)
        ]
        v_bot = []
        v_top = []
        for lx, lz in pts_2d:
            gx = center_x + (lx * cos_a - lz * px)
            gz = center_z + (lx * sin_a - lz * pz)
            v_bot.append(self.add_vertex(gx, y_center - half_h, gz))
            v_top.append(self.add_vertex(gx, y_center + half_h, gz))

        ny_up = self.add_normal(0, 1, 0)
        ny_dn = self.add_normal(0, -1, 0)
        self.add_quad(v_top[0], v_top[1], v_top[2], v_top[3], ny_up, ny_up, ny_up, ny_up, mat)
        self.add_quad(v_bot[3], v_bot[2], v_bot[1], v_bot[0], ny_dn, ny_dn, ny_dn, ny_dn, mat)
        for i in range(4):
            nxt = (i + 1) % 4
            dx = pts_2d[nxt][0] - pts_2d[i][0]
            dz = pts_2d[nxt][1] - pts_2d[i][1]
            snx = (dx * cos_a - dz * px)
            snz = (dx * sin_a - dz * pz)
            sid_n = self.add_normal(-snz, 0, snx)
            self.add_quad(v_bot[i], v_top[i], v_top[nxt], v_bot[nxt], sid_n, sid_n, sid_n, sid_n, mat)

    def add_sphere(self, cx, cy, cz, radius, rings=20, sectors=30, mat="Default"):
        grid_v = []
        grid_n = []
        for i in range(rings + 1):
            lat = math.pi * (-0.5 + float(i) / rings)
            sin_lat, cos_lat = math.sin(lat), math.cos(lat)
            ring_v, ring_n = [], []
            for j in range(sectors + 1):
                lon = 2.0 * math.pi * float(j) / sectors
                sin_lon, cos_lon = math.sin(lon), math.cos(lon)
                nx = cos_lat * cos_lon
                ny = sin_lat
                nz = cos_lat * sin_lon
                ring_v.append(self.add_vertex(cx + radius * nx, cy + radius * ny, cz + radius * nz))
                ring_n.append(self.add_normal(nx, ny, nz))
            grid_v.append(ring_v)
            grid_n.append(ring_n)

        for i in range(rings):
            for j in range(sectors):
                self.add_quad(grid_v[i][j], grid_v[i+1][j], grid_v[i+1][j+1], grid_v[i][j+1],
                              grid_n[i][j], grid_n[i+1][j], grid_n[i+1][j+1], grid_n[i][j+1], mat)

    def add_torus(self, cx, cy, cz, r_major, r_minor_x, r_minor_y, seg_major=64, seg_minor=20, mat="Default"):
        grid_v = []
        grid_n = []
        for i in range(seg_major):
            theta = 2.0 * math.pi * i / seg_major
            cos_t, sin_t = math.cos(theta), math.sin(theta)
            ring_v, ring_n = [], []
            for j in range(seg_minor):
                phi = 2.0 * math.pi * j / seg_minor
                cos_p, sin_p = math.cos(phi), math.sin(phi)
                r = r_major + r_minor_x * cos_p
                x = cx + r * cos_t
                y = cy + r_minor_y * sin_p
                z = cz + r * sin_t
                ring_v.append(self.add_vertex(x, y, z))
                ring_n.append(self.add_normal(cos_p * cos_t, sin_p, cos_p * sin_t))
            grid_v.append(ring_v)
            grid_n.append(ring_n)

        for i in range(seg_major):
            nxt_i = (i + 1) % seg_major
            for j in range(seg_minor):
                nxt_j = (j + 1) % seg_minor
                self.add_quad(grid_v[i][j], grid_v[nxt_i][j], grid_v[nxt_i][nxt_j], grid_v[i][nxt_j],
                              grid_n[i][j], grid_n[nxt_i][j], grid_n[nxt_i][nxt_j], grid_n[i][nxt_j], mat)

    def save(self, mtl_content):
        obj_file = os.path.join(models_dir, f"{self.name}.obj")
        mtl_file = os.path.join(models_dir, f"{self.mtl_name}.mtl")

        with open(mtl_file, "w", encoding="utf-8") as f:
            f.write(mtl_content)

        with open(obj_file, "w", encoding="utf-8") as f:
            f.write(f"# Wavefront OBJ Export for {self.name}\n")
            f.write(f"mtllib {self.mtl_name}.mtl\n\n")
            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for n in self.normals:
                f.write(f"vn {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n")

            current_mat = None
            for face_v, face_n, mat in self.faces:
                if mat != current_mat:
                    current_mat = mat
                    f.write(f"usemtl {current_mat}\n")
                    f.write(f"g {current_mat}\n")
                f_str = " ".join([f"{fv}//{fn}" for fv, fn in zip(face_v, face_n)])
                f.write(f"f {f_str}\n")

        print(f"Exported: {self.name}.obj ({os.path.getsize(obj_file):,} bytes)")

# =============================================================================
# 1. EARTH PORT PLATFORM (100 m Scale Marine Platform)
# =============================================================================
ep = ObjBuilder("Earth_Port_Platform", "Earth_Port_Platform")
# Twin lower buoyancy pontoons: length = 100m, width = 16m, height = 10m, center-to-center = 64m
ep.add_box(-50.0, 50.0, -5.0, 5.0, -40.0, -24.0, mat="Marine_Epoxy_Steel")
ep.add_box(-50.0, 50.0, -5.0, 5.0,  24.0,  40.0, mat="Marine_Epoxy_Steel")
# 4 Vertical stability columns: dia = 14m, height = 28m
for cx in [-32.0, 32.0]:
    for cz in [-32.0, 32.0]:
        ep.add_cylinder(7.0, 5.0, 33.0, cx=cx, cz=cz, mat="Marine_Epoxy_Steel")
# Upper main structural deck: 84m x 84m x 5m
ep.add_box(-42.0, 42.0, 33.0, 38.0, -42.0, 42.0, mat="Deck_Industrial_Gold")
# Moonpool & Gimbal Ring
ep.add_cylinder(13.0, 36.0, 39.5, mat="Safety_Gold")
# Wind & Lightning Arrestor Tower (35m conical cowl)
ep.add_cylinder(6.5, 38.0, 73.0, segments=24, mat="Marine_White")

ep_mtl = """
newmtl Marine_Epoxy_Steel
Kd 0.14 0.22 0.30
Ks 0.50 0.55 0.60
Ns 45.0

newmtl Deck_Industrial_Gold
Kd 0.85 0.65 0.15
Ks 0.70 0.60 0.20
Ns 40.0

newmtl Safety_Gold
Kd 0.84 0.65 0.12
Ks 0.90 0.80 0.30
Ns 80.0

newmtl Marine_White
Kd 0.80 0.82 0.85
Ks 0.30 0.30 0.30
Ns 25.0
"""
ep.save(ep_mtl)

# =============================================================================
# 2. TETHER CLIMBER (6 m Scale 20-Metric-Ton Climber, centered at origin)
# =============================================================================
cl = ObjBuilder("Tether_Climber_20T", "Tether_Climber_20T")
# Hexagonal Composite Chassis: 3.2m flat-to-flat, 5.0m height
cl.add_cylinder(1.7, -2.5, 2.5, segments=6, mat="CFRP_Chassis")
# Central cable passage slot
cl.add_box(-0.65, 0.65, -2.5, 2.5, -0.15, 0.15, mat="CFRP_Chassis")
# 6 Pinch Rollers & Hydraulic Actuators (at Y = -1.5, 0.0, +1.5)
for y_elev in [-1.5, 0.0, 1.5]:
    # Front Roller
    cl.add_cylinder(0.20, y_elev - 0.55, y_elev + 0.55, cx=0.0, cz=0.25, segments=16, mat="DLC_Roller")
    cl.add_box(-0.7, 0.7, y_elev - 0.25, y_elev + 0.25, 0.35, 0.55, mat="Anodized_Red_Yoke")
    # Rear Roller
    cl.add_cylinder(0.20, y_elev - 0.55, y_elev + 0.55, cx=0.0, cz=-0.25, segments=16, mat="DLC_Roller")
    cl.add_box(-0.7, 0.7, y_elev - 0.25, y_elev + 0.25, -0.55, -0.35, mat="Anodized_Red_Yoke")

# 2 Thermal Radiator Wings (Starboard X=+1.65m, Port X=-1.65m, Span 3.5m, Height 4.2m)
cl.add_box(1.65, 5.15, -2.1, 2.1, -0.02, 0.02, mat="Silver_Radiator")
cl.add_box(-5.15, -1.65, -2.1, 2.1, -0.02, 0.02, mat="Silver_Radiator")

# Inverted Cassegrain Laser PV Receiver Dish at base (Dia = 6m)
cl.add_sphere(0.0, -3.2, 0.0, 3.0, rings=16, sectors=24, mat="GaAs_Photovoltaic")

cl_mtl = """
newmtl CFRP_Chassis
Kd 0.12 0.12 0.14
Ks 0.40 0.40 0.40
Ns 35.0

newmtl DLC_Roller
Kd 0.75 0.55 0.20
Ks 0.85 0.70 0.30
Ns 70.0

newmtl Anodized_Red_Yoke
Kd 0.75 0.15 0.15
Ks 0.85 0.40 0.40
Ns 80.0

newmtl Silver_Radiator
Kd 0.88 0.90 0.92
Ks 0.95 0.95 0.95
Ns 90.0

newmtl GaAs_Photovoltaic
Kd 0.15 0.10 0.35
Ks 0.95 0.90 0.98
Ns 110.0
"""
cl.save(cl_mtl)

# =============================================================================
# 3. GEO ORBITAL TERMINAL STATION (208 m Scale, centered at origin)
# =============================================================================
geo = ObjBuilder("GEO_Orbital_Station", "GEO_Orbital_Station")
# 180m Central Transit Core (OD 18m, ID 10m)
geo.add_cylinder(9.0, -90.0, 90.0, segments=48, mat="Titanium_Core")
# 6 Longitudinal Stiffener Ribs
for i in range(6):
    rad = math.radians(i * 60.0)
    rc = 9.75
    geo.add_oriented_box(rc * math.cos(rad), rc * math.sin(rad), rad, 1.5, 1.2, 160.0, 0.0, mat="Titanium_Core")

# Pressurized Torus Hab Ring: OD 208m, Major R = 95m, capsule cross-section 18m x 14m
geo.add_torus(0.0, 0.0, 0.0, 95.0, 9.0, 7.0, seg_major=72, seg_minor=24, mat="Torus_Hab_White")
# Circumferential Whipple Bumper Ribs
geo.add_torus(0.0, 4.5, 0.0, 95.0, 9.5, 1.0, seg_major=72, seg_minor=12, mat="Titanium_Core")
geo.add_torus(0.0, -4.5, 0.0, 95.0, 9.5, 1.0, seg_major=72, seg_minor=12, mat="Titanium_Core")

# 4 Orthogonal Transit Spoke Corridors (Width 5m, Height 4m, R=8.5m to 86m)
geo.add_box(8.5, 86.0, -2.0, 2.0, -2.5, 2.5, mat="Composite_Slate")
geo.add_box(-86.0, -8.5, -2.0, 2.0, -2.5, 2.5, mat="Composite_Slate")
geo.add_box(-2.5, 2.5, -2.0, 2.0, 8.5, 86.0, mat="Composite_Slate")
geo.add_box(-2.5, 2.5, -2.0, 2.0, -86.0, -8.5, mat="Composite_Slate")
geo.add_box(-8.5, 8.5, -2.5, 2.5, -8.5, 8.5, mat="Composite_Slate")

# 4 Geodesic Biosphere Spheres (Diameter = 26m, Radius = 13m, centered at R=50m)
for cx, cz in [(50.0, 0.0), (-50.0, 0.0), (0.0, 50.0), (0.0, -50.0)]:
    geo.add_sphere(cx, 0.0, cz, 13.0, rings=20, sectors=32, mat="Biosphere_Glass")
    # Equatorial exo-skeleton spaceframe
    for deg in range(0, 360, 20):
        rad1, rad2 = math.radians(deg), math.radians(deg + 20)
        p1x, p1z = cx + 13.5 * math.cos(rad1), cz + 13.5 * math.sin(rad1)
        p2x, p2z = cx + 13.5 * math.cos(rad2), cz + 13.5 * math.sin(rad2)
        midx, midz = (p1x + p2x) * 0.5, (p1z + p2z) * 0.5
        d = math.hypot(p2x - p1x, p2z - p1z)
        ang = math.atan2(p2z - p1z, p2x - p1x)
        geo.add_oriented_box(midx, midz, ang, d, 0.8, 0.8, 0.0, mat="Gold_Truss")

# 6-Wing Mega Solar Photovoltaic Array (Wingspan 190m, Y = +75m)
geo.add_cylinder(11.0, 73.5, 76.5, segments=36, mat="Composite_Slate")
for i in range(6):
    rad = math.radians(i * 60.0)
    center_r = 53.5
    cx, cz = center_r * math.cos(rad), center_r * math.sin(rad)
    geo.add_oriented_box(cx, cz, rad, 83.0, 16.0, 0.35, 75.0, mat="Photovoltaic_Blue")
    geo.add_oriented_box(cx, cz, rad, 85.0, 1.2, 0.8, 75.0, mat="Titanium_Core")

# Axial Communications Spire (Y = +90m to +175m)
geo.add_cylinder(2.0, 90.0, 175.0, segments=24, mat="Thermal_White")
for y_pos, d_rad in [(120.0, 4.0), (140.0, 3.5), (160.0, 3.0)]:
    geo.add_sphere(4.0, y_pos, 0.0, d_rad, rings=12, sectors=16, mat="Gold_Truss")

geo_mtl = """
newmtl Torus_Hab_White
Kd 0.94 0.96 0.98
Ks 0.50 0.50 0.50
Ns 50.0

newmtl Photovoltaic_Blue
Kd 0.06 0.14 0.45
Ks 0.95 0.95 0.98
Ns 100.0

newmtl Biosphere_Glass
Kd 0.55 0.80 0.92
Ks 0.95 0.95 0.95
Ns 120.0
d 0.45

newmtl Titanium_Core
Kd 0.68 0.70 0.74
Ks 0.70 0.70 0.72
Ns 60.0

newmtl Composite_Slate
Kd 0.35 0.37 0.40
Ks 0.30 0.30 0.30
Ns 25.0

newmtl Gold_Truss
Kd 0.88 0.72 0.18
Ks 0.95 0.85 0.40
Ns 85.0

newmtl Thermal_White
Kd 0.95 0.95 0.97
Ks 0.30 0.30 0.30
Ns 30.0
"""
geo.save(geo_mtl)

# =============================================================================
# 4. APEX COUNTERWEIGHT HUB (50 m Scale, centered at origin)
# =============================================================================
ap = ObjBuilder("Apex_Counterweight_Hub", "Apex_Counterweight_Hub")
ap.add_box(-12.0, 12.0, -7.5, 7.5, -12.0, 12.0, mat="Ballast_Titanium")
ap.add_box(8.0, 38.0, 0.0, 3.0, -1.5, 1.5, mat="Accelerator_Orange")
for i in range(4):
    rad = math.radians(i * 90.0)
    ap.add_oriented_box(20.0 * math.cos(rad), 20.0 * math.sin(rad), rad, 16.0, 6.0, 0.2, 0.0, mat="Photovoltaic_Blue")

ap_mtl = """
newmtl Ballast_Titanium
Kd 0.28 0.30 0.32
Ks 0.50 0.50 0.50
Ns 40.0

newmtl Accelerator_Orange
Kd 0.88 0.44 0.08
Ks 0.80 0.60 0.30
Ns 60.0

newmtl Photovoltaic_Blue
Kd 0.06 0.14 0.45
Ks 0.95 0.95 0.98
Ns 100.0
"""
ap.save(ap_mtl)
print("\nALL 4 CAD 3D OBJs SUCCESSFULLY GENERATED IN WebGL_Simulator/models/!")
