import os
import math
import numpy as np

def create_showcase_obj():
    out_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\3D_OBJ_Exports"
    os.makedirs(out_dir, exist_ok=True)
    obj_path = os.path.join(out_dir, "Space_Elevator_Master_Showcase_Complete.obj")
    mtl_path = os.path.join(out_dir, "Space_Elevator_Master_Showcase_Complete.mtl")

    vertices = []
    normals = []
    faces = []

    def add_vertex(x, y, z):
        vertices.append((x, y, z))
        return len(vertices)

    def add_normal(nx, ny, nz):
        l = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
        normals.append((nx/l, ny/l, nz/l))
        return len(normals)

    def add_quad(v1, v2, v3, v4, n1, n2, n3, n4, mat):
        faces.append(([v1, v2, v3], [n1, n2, n3], mat))
        faces.append(([v1, v3, v4], [n1, n3, n4], mat))

    def add_cylinder(r, y_min, y_max, cx=0.0, cz=0.0, segments=36, mat="Marine_Steel"):
        top_v, bot_v, top_n, bot_n = [], [], [], []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            ca = math.cos(angle)
            sa = math.sin(angle)
            top_v.append(add_vertex(cx + r * ca, y_max, cz + r * sa))
            bot_v.append(add_vertex(cx + r * ca, y_min, cz + r * sa))
            top_n.append(add_normal(ca, 0.0, sa))
            bot_n.append(add_normal(ca, 0.0, sa))

        for i in range(segments):
            nxt = (i + 1) % segments
            add_quad(bot_v[i], top_v[i], top_v[nxt], bot_v[nxt],
                     bot_n[i], top_n[i], top_n[nxt], bot_n[nxt], mat)

    def add_box(min_x, max_x, min_y, max_y, min_z, max_z, mat="Marine_Steel"):
        p = [
            (min_x, min_y, min_z), (max_x, min_y, min_z),
            (max_x, max_y, min_z), (min_x, max_y, min_z),
            (min_x, min_y, max_z), (max_x, min_y, max_z),
            (max_x, max_y, max_z), (min_x, max_y, max_z)
        ]
        v = [add_vertex(pt[0], pt[1], pt[2]) for pt in p]
        nx_neg = add_normal(-1, 0, 0)
        nx_pos = add_normal(1, 0, 0)
        ny_neg = add_normal(0, -1, 0)
        ny_pos = add_normal(0, 1, 0)
        nz_neg = add_normal(0, 0, -1)
        nz_pos = add_normal(0, 0, 1)

        add_quad(v[0], v[3], v[2], v[1], nz_neg, nz_neg, nz_neg, nz_neg, mat)
        add_quad(v[4], v[5], v[6], v[7], nz_pos, nz_pos, nz_pos, nz_pos, mat)
        add_quad(v[0], v[4], v[7], v[3], nx_neg, nx_neg, nx_neg, nx_neg, mat)
        add_quad(v[1], v[2], v[6], v[5], nx_pos, nx_pos, nx_pos, nx_pos, mat)
        add_quad(v[0], v[1], v[5], v[4], ny_neg, ny_neg, ny_neg, ny_neg, mat)
        add_quad(v[3], v[7], v[6], v[2], ny_pos, ny_pos, ny_pos, ny_pos, mat)

    def add_torus(cx, cy, cz, r_major, r_minor_x, r_minor_y, seg_major=48, seg_minor=16, mat="Torus_Hab_White"):
        grid_v = []
        grid_n = []
        for i in range(seg_major):
            theta = 2.0 * math.pi * i / seg_major
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            ring_v = []
            ring_n = []
            for j in range(seg_minor):
                phi = 2.0 * math.pi * j / seg_minor
                cos_p = math.cos(phi)
                sin_p = math.sin(phi)
                r = r_major + r_minor_x * cos_p
                x = cx + r * cos_t
                y = cy + r_minor_y * sin_p
                z = cz + r * sin_t
                ring_v.append(add_vertex(x, y, z))
                ring_n.append(add_normal(cos_p * cos_t, sin_p, cos_p * sin_t))
            grid_v.append(ring_v)
            grid_n.append(ring_n)

        for i in range(seg_major):
            nxt_i = (i + 1) % seg_major
            for j in range(seg_minor):
                nxt_j = (j + 1) % seg_minor
                add_quad(grid_v[i][j], grid_v[nxt_i][j], grid_v[nxt_i][nxt_j], grid_v[i][nxt_j],
                         grid_n[i][j], grid_n[nxt_i][j], grid_n[nxt_i][nxt_j], grid_n[i][nxt_j], mat)

    def add_sphere(cx, cy, cz, radius, rings=16, sectors=24, mat="Biosphere_Glass"):
        grid_v = []
        grid_n = []
        for i in range(rings + 1):
            lat = math.pi * (-0.5 + float(i) / rings)
            sin_lat = math.sin(lat)
            cos_lat = math.cos(lat)
            ring_v = []
            ring_n = []
            for j in range(sectors + 1):
                lon = 2.0 * math.pi * float(j) / sectors
                sin_lon = math.sin(lon)
                cos_lon = math.cos(lon)
                nx = cos_lat * cos_lon
                ny = sin_lat
                nz = cos_lat * sin_lon
                ring_v.append(add_vertex(cx + radius * nx, cy + radius * ny, cz + radius * nz))
                ring_n.append(add_normal(nx, ny, nz))
            grid_v.append(ring_v)
            grid_n.append(ring_n)

        for i in range(rings):
            for j in range(sectors):
                add_quad(grid_v[i][j], grid_v[i+1][j], grid_v[i+1][j+1], grid_v[i][j+1],
                         grid_n[i][j], grid_n[i+1][j], grid_n[i+1][j+1], grid_n[i][j+1], mat)

    print("[1/4] Building Multi-Tier 3D Space Elevator Hierarchy...")

    # ==========================================
    # TIER 1: Marine Earth Port Platform (Y = 0m)
    # ==========================================
    # Pontoons
    add_box(-50.0, 50.0, -20.0, -10.0, -40.0, -24.0, mat="Marine_Steel")
    add_box(-50.0, 50.0, -20.0, -10.0,  24.0,  40.0, mat="Marine_Steel")
    # 4 Vertical Columns
    for col_x in [-32.0, 32.0]:
        for col_z in [-32.0, 32.0]:
            add_cylinder(7.0, -10.0, 18.0, cx=col_x, cz=col_z, mat="Marine_Steel")
    # Deck
    add_box(-42.0, 42.0, 18.0, 23.0, -42.0, 42.0, mat="Marine_Steel")
    # Gimbal Ring
    add_cylinder(13.0, 21.0, 24.5, mat="Gold_Gimbal")
    # Lightning Cowl
    add_cylinder(7.0, 23.0, 58.0, mat="Marine_Steel")

    # ==========================================
    # TIER 2: 20-Metric-Ton Climber (Y = +60m)
    # ==========================================
    climber_y = 60.0
    add_box(-1.6, 1.6, climber_y, climber_y + 5.0, -1.6, 1.6, mat="Composite_Chassis")
    # Radiator wings
    add_box(1.6, 5.1, climber_y + 0.4, climber_y + 4.6, -0.02, 0.02, mat="Silver_Radiator")
    add_box(-5.1, -1.6, climber_y + 0.4, climber_y + 4.6, -0.02, 0.02, mat="Silver_Radiator")
    # Cassegrain PV Dish at bottom
    add_sphere(0.0, climber_y - 1.0, 0.0, 3.0, rings=12, sectors=16, mat="Photovoltaic_Blue")

    # ==========================================
    # TIER 3: GEO Orbital Terminal (Y = +180m)
    # ==========================================
    geo_y = 180.0
    # Central Core
    add_cylinder(9.0, geo_y - 90.0, geo_y + 90.0, segments=36, mat="Titanium_Core")
    # Habitation Torus Ring (OD 208m)
    add_torus(0.0, geo_y, 0.0, 95.0, 9.0, 7.0, seg_major=48, seg_minor=16, mat="Torus_Hab_White")
    # 4 Spokes
    add_box(8.5, 86.0, geo_y - 2.0, geo_y + 2.0, -2.5, 2.5, mat="Composite_Chassis")
    add_box(-86.0, -8.5, geo_y - 2.0, geo_y + 2.0, -2.5, 2.5, mat="Composite_Chassis")
    add_box(-2.5, 2.5, geo_y - 2.0, geo_y + 2.0, 8.5, 86.0, mat="Composite_Chassis")
    add_box(-2.5, 2.5, geo_y - 2.0, geo_y + 2.0, -86.0, -8.5, mat="Composite_Chassis")
    # 4 Biosphere Spheres
    for cx, cz in [(50.0, 0.0), (-50.0, 0.0), (0.0, 50.0), (0.0, -50.0)]:
        add_sphere(cx, geo_y, cz, 13.0, rings=16, sectors=24, mat="Biosphere_Glass")
    # 6 Solar Wings at Y = geo_y + 75m
    for i in range(6):
        rad = math.radians(i * 60.0)
        cr = 53.5
        add_box(cr * math.cos(rad) - 7.0, cr * math.cos(rad) + 7.0,
                geo_y + 74.8, geo_y + 75.2,
                cr * math.sin(rad) - 7.0, cr * math.sin(rad) + 7.0, mat="Photovoltaic_Blue")
    # Spire
    add_cylinder(2.0, geo_y + 90.0, geo_y + 175.0, mat="Thermal_White")

    # ==========================================
    # TIER 4: Apex Counterweight Hub (Y = +320m)
    # ==========================================
    apex_y = 320.0
    add_box(-12.0, 12.0, apex_y - 7.5, apex_y + 7.5, -12.0, 12.0, mat="Titanium_Core")
    # Peet Sling Ramp
    add_box(8.0, 38.0, apex_y, apex_y + 3.0, -1.5, 1.5, mat="Gold_Gimbal")

    # Continuous Tether Line (passing through everything from Earth to Apex)
    add_box(-0.5, 0.5, -20.0, 340.0, -0.002, 0.002, mat="Graphene_Tether")

    # Write MTL
    mtl_content = """# Space Elevator Materials Library
newmtl Marine_Steel
Kd 0.15 0.22 0.30
Ks 0.50 0.50 0.50
Ns 40.0

newmtl Torus_Hab_White
Kd 0.94 0.96 0.98
Ks 0.40 0.40 0.40
Ns 50.0

newmtl Photovoltaic_Blue
Kd 0.08 0.18 0.55
Ks 0.95 0.95 0.98
Ns 95.0

newmtl Biosphere_Glass
Kd 0.55 0.80 0.92
Ks 0.95 0.95 0.95
Ns 120.0
d 0.45

newmtl Titanium_Core
Kd 0.68 0.70 0.74
Ks 0.70 0.70 0.72
Ns 60.0

newmtl Composite_Chassis
Kd 0.18 0.18 0.20
Ks 0.30 0.30 0.30
Ns 30.0

newmtl Gold_Gimbal
Kd 0.88 0.72 0.18
Ks 0.95 0.85 0.40
Ns 85.0

newmtl Silver_Radiator
Kd 0.85 0.88 0.90
Ks 0.90 0.90 0.90
Ns 70.0

newmtl Thermal_White
Kd 0.95 0.95 0.97
Ks 0.30 0.30 0.30
Ns 30.0

newmtl Graphene_Tether
Kd 0.18 0.22 0.28
Ks 0.65 0.65 0.70
Ns 50.0
"""
    with open(mtl_path, "w", encoding="utf-8") as f:
        f.write(mtl_content)

    with open(obj_path, "w", encoding="utf-8") as f:
        f.write("# Space Elevator Master Multi-Tier Architecture Showcase\n")
        f.write(f"mtllib {os.path.basename(mtl_path)}\n\n")
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for n in normals:
            f.write(f"vn {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n")
        curr_mat = None
        for f_v, f_n, mat in faces:
            if mat != curr_mat:
                curr_mat = mat
                f.write(f"usemtl {curr_mat}\n")
                f.write(f"g {curr_mat}\n")
            f_str = " ".join([f"{fv}//{fn}" for fv, fn in zip(f_v, f_n)])
            f.write(f"f {f_str}\n")

    print(f"[SUCCESS] Created Complete Multi-Tier OBJ ({os.path.getsize(obj_path):,} bytes)")

if __name__ == "__main__":
    create_showcase_obj()
