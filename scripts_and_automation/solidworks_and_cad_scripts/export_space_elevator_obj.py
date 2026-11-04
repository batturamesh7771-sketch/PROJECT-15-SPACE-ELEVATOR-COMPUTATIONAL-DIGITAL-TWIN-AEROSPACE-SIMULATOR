import os
import math
import numpy as np

def create_space_elevator_obj():
    out_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\3D_OBJ_Exports"
    os.makedirs(out_dir, exist_ok=True)
    obj_path = os.path.join(out_dir, "Space_Elevator_GEO_Orbital_Station.obj")
    mtl_path = os.path.join(out_dir, "Space_Elevator_GEO_Orbital_Station.mtl")

    vertices = []
    normals = []
    texcoords = []
    faces = [] # (v_indices, n_indices, material)

    # ---------------------------------------------------------
    # Helper functions to build 3D mesh primitives
    # ---------------------------------------------------------
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

    def add_tri(v1, v2, v3, n1, n2, n3, mat):
        faces.append(([v1, v2, v3], [n1, n2, n3], mat))

    # Cylinder along Y axis
    def add_cylinder(r, y_min, y_max, segments=48, mat="Titanium_Core"):
        top_v = []
        bot_v = []
        top_n = []
        bot_n = []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            ca = math.cos(angle)
            sa = math.sin(angle)
            top_v.append(add_vertex(r * ca, y_max, r * sa))
            bot_v.append(add_vertex(r * ca, y_min, r * sa))
            top_n.append(add_normal(ca, 0.0, sa))
            bot_n.append(add_normal(ca, 0.0, sa))

        for i in range(segments):
            next_i = (i + 1) % segments
            # Side quads
            add_quad(bot_v[i], top_v[i], top_v[next_i], bot_v[next_i],
                     bot_n[i], top_n[i], top_n[next_i], bot_n[next_i], mat)

    # Hollow Cylinder (Tube)
    def add_tube(r_in, r_out, y_min, y_max, segments=48, mat="Titanium_Core"):
        add_cylinder(r_out, y_min, y_max, segments, mat)

    # Torus centered on Y axis
    def add_torus(r_major, r_minor_x, r_minor_y, seg_major=72, seg_minor=24, mat="Torus_Hab_White"):
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
                x = r * cos_t
                y = r_minor_y * sin_p
                z = r * sin_t

                # Normal
                nx = cos_p * cos_t
                ny = sin_p
                nz = cos_p * sin_t

                ring_v.append(add_vertex(x, y, z))
                ring_n.append(add_normal(nx, ny, nz))
            grid_v.append(ring_v)
            grid_n.append(ring_n)

        for i in range(seg_major):
            next_i = (i + 1) % seg_major
            for j in range(seg_minor):
                next_j = (j + 1) % seg_minor
                add_quad(grid_v[i][j], grid_v[next_i][j], grid_v[next_i][next_j], grid_v[i][next_j],
                         grid_n[i][j], grid_n[next_i][j], grid_n[next_i][next_j], grid_n[i][next_j], mat)

    # UV Sphere
    def add_sphere(cx, cy, cz, radius, rings=24, sectors=36, mat="Biosphere_Glass"):
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

                x = cx + radius * nx
                y = cy + radius * ny
                z = cz + radius * nz

                ring_v.append(add_vertex(x, y, z))
                ring_n.append(add_normal(nx, ny, nz))
            grid_v.append(ring_v)
            grid_n.append(ring_n)

        for i in range(rings):
            for j in range(sectors):
                add_quad(grid_v[i][j], grid_v[i+1][j], grid_v[i+1][j+1], grid_v[i][j+1],
                         grid_n[i][j], grid_n[i+1][j], grid_n[i+1][j+1], grid_n[i][j+1], mat)

    # Box (oriented bounding slab)
    def add_box(min_x, max_x, min_y, max_y, min_z, max_z, mat="Composite_Corridor"):
        p = [
            (min_x, min_y, min_z), (max_x, min_y, min_z),
            (max_x, max_y, min_z), (min_x, max_y, min_z),
            (min_x, min_y, max_z), (max_x, min_y, max_z),
            (max_x, max_y, max_z), (min_x, max_y, max_z)
        ]
        v = [add_vertex(pt[0], pt[1], pt[2]) for pt in p]
        
        # Normals for 6 faces
        nx_neg = add_normal(-1, 0, 0)
        nx_pos = add_normal(1, 0, 0)
        ny_neg = add_normal(0, -1, 0)
        ny_pos = add_normal(0, 1, 0)
        nz_neg = add_normal(0, 0, -1)
        nz_pos = add_normal(0, 0, 1)

        # -Z face
        add_quad(v[0], v[3], v[2], v[1], nz_neg, nz_neg, nz_neg, nz_neg, mat)
        # +Z face
        add_quad(v[4], v[5], v[6], v[7], nz_pos, nz_pos, nz_pos, nz_pos, mat)
        # -X face
        add_quad(v[0], v[4], v[7], v[3], nx_neg, nx_neg, nx_neg, nx_neg, mat)
        # +X face
        add_quad(v[1], v[2], v[6], v[5], nx_pos, nx_pos, nx_pos, nx_pos, mat)
        # -Y face
        add_quad(v[0], v[1], v[5], v[4], ny_neg, ny_neg, ny_neg, ny_neg, mat)
        # +Y face
        add_quad(v[3], v[7], v[6], v[2], ny_pos, ny_pos, ny_pos, ny_pos, mat)

    # Oriented Flat Box for Solar Wings
    def add_oriented_box(center_x, center_z, angle_rad, length, width, height, y_elev, mat="Photovoltaic_Blue"):
        half_l = length * 0.5
        half_w = width * 0.5
        half_h = height * 0.5
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        px = -sin_a
        pz = cos_a

        # Local corners in 2D
        pts_2d = [
            (-half_l, -half_w), (half_l, -half_w), (half_l, half_w), (-half_l, half_w)
        ]
        v_bot = []
        v_top = []
        for lx, lz in pts_2d:
            gx = center_x + (lx * cos_a - lz * px)
            gz = center_z + (lx * sin_a - lz * pz)
            v_bot.append(add_vertex(gx, y_elev - half_h, gz))
            v_top.append(add_vertex(gx, y_elev + half_h, gz))

        ny_up = add_normal(0, 1, 0)
        ny_dn = add_normal(0, -1, 0)
        # Top & Bottom
        add_quad(v_top[0], v_top[1], v_top[2], v_top[3], ny_up, ny_up, ny_up, ny_up, mat)
        add_quad(v_bot[3], v_bot[2], v_bot[1], v_bot[0], ny_dn, ny_dn, ny_dn, ny_dn, mat)
        # Sides
        for i in range(4):
            nxt = (i + 1) % 4
            # Normal perpendicular to side edge
            dx = pts_2d[nxt][0] - pts_2d[i][0]
            dz = pts_2d[nxt][1] - pts_2d[i][1]
            snx = (dx * cos_a - dz * px)
            snz = (dx * sin_a - dz * pz)
            sid_n = add_normal(-snz, 0, snx)
            add_quad(v_bot[i], v_top[i], v_top[nxt], v_bot[nxt], sid_n, sid_n, sid_n, sid_n, mat)

    print("[1/5] Synthesizing 3D Geometry for Space Elevator Station...")

    # 1. Central Transit Core (180m Backbone Tower: OD=18m, ID=10m)
    add_cylinder(9.0, -90.0, 90.0, segments=48, mat="Titanium_Core")
    # 6 Longitudinal Stiffener Ribs
    for i in range(6):
        deg = i * 60.0
        rad = math.radians(deg)
        rc = 9.75
        add_oriented_box(rc * math.cos(rad), rc * math.sin(rad), rad, 1.5, 1.2, 160.0, 0.0, mat="Titanium_Core")

    # 4 Maglev Climber Docking Collars
    add_tube(9.0, 10.5, 23.0, 27.0, segments=36, mat="Gold_Foil")
    add_tube(9.0, 10.5, -27.0, -23.0, segments=36, mat="Gold_Foil")

    # 2. Pressurized Habitation Torus Ring (208m outer diameter, R_major=95m, R_x=9m, R_y=7m)
    add_torus(95.0, 9.0, 7.0, seg_major=72, seg_minor=24, mat="Torus_Hab_White")
    # Circumferential Whipple Shield Ribs
    add_torus(95.0, 9.6, 1.0, seg_major=72, seg_minor=12, mat="Thermal_White")
    add_torus(95.0, 9.6, -1.0, seg_major=72, seg_minor=12, mat="Thermal_White")

    # 3. 4 Orthogonal Transit Spoke Corridors (Width=5m, Height=4m, R=8.5m to 86m)
    add_box(8.5, 86.0, -2.0, 2.0, -2.5, 2.5, mat="Composite_Corridor")
    add_box(-86.0, -8.5, -2.0, 2.0, -2.5, 2.5, mat="Composite_Corridor")
    add_box(-2.5, 2.5, -2.0, 2.0, 8.5, 86.0, mat="Composite_Corridor")
    add_box(-2.5, 2.5, -2.0, 2.0, -86.0, -8.5, mat="Composite_Corridor")
    # Central corridor junction hub
    add_box(-8.5, 8.5, -2.5, 2.5, -8.5, 8.5, mat="Composite_Corridor")

    # 4. 4 Geodesic Biosphere Spheres (Diameter=26m, R=13m, centered at R=50m)
    for cx, cz in [(50.0, 0.0), (-50.0, 0.0), (0.0, 50.0), (0.0, -50.0)]:
        add_sphere(cx, 0.0, cz, 13.0, rings=20, sectors=32, mat="Biosphere_Glass")
        # Equatorial Spaceframe Ring
        for deg in range(0, 360, 15):
            rad1 = math.radians(deg)
            rad2 = math.radians(deg + 15)
            # Add thin circumferential truss segments
            p1x = cx + 13.5 * math.cos(rad1)
            p1z = cz + 13.5 * math.sin(rad1)
            p2x = cx + 13.5 * math.cos(rad2)
            p2z = cz + 13.5 * math.sin(rad2)
            midx = (p1x + p2x) * 0.5
            midz = (p1z + p2z) * 0.5
            d = math.hypot(p2x - p1x, p2z - p1z)
            ang = math.atan2(p2z - p1z, p2x - p1x)
            add_oriented_box(midx, midz, ang, d, 0.8, 0.8, 0.0, mat="Gold_Foil")

    # 5. 6-Wing Mega Solar Photovoltaic Array (Wingspan 190m, Y = +75m)
    add_cylinder(11.0, 73.5, 76.5, segments=36, mat="Composite_Corridor")
    for i in range(6):
        deg = i * 60.0
        rad = math.radians(deg)
        # Solar wing: Length 83m (R: 12m to 95m), Width 16m, Thickness 0.35m
        center_r = (12.0 + 95.0) * 0.5
        cx = center_r * math.cos(rad)
        cz = center_r * math.sin(rad)
        add_oriented_box(cx, cz, rad, 83.0, 16.0, 0.35, 75.0, mat="Photovoltaic_Blue")
        # Structural support boom
        add_oriented_box(cx, cz, rad, 85.0, 1.2, 0.8, 75.0, mat="Titanium_Core")

    # 6. Communications Spire and RCS Mast (Y = +90m to +175m)
    # Tapered Spire Cone
    spire_segs = 32
    spire_base_v = []
    spire_base_n = []
    spire_tip_v = []
    spire_tip_n = []
    for i in range(spire_segs):
        ang = 2.0 * math.pi * i / spire_segs
        ca = math.cos(ang)
        sa = math.sin(ang)
        spire_base_v.append(add_vertex(5.0 * ca, 90.0, 5.0 * sa))
        spire_base_n.append(add_normal(ca, 0.05, sa))
        spire_tip_v.append(add_vertex(1.1 * ca, 175.0, 1.1 * sa))
        spire_tip_n.append(add_normal(ca, 0.05, sa))

    for i in range(spire_segs):
        nxt = (i + 1) % spire_segs
        add_quad(spire_base_v[i], spire_tip_v[i], spire_tip_v[nxt], spire_base_v[nxt],
                 spire_base_n[i], spire_tip_n[i], spire_tip_n[nxt], spire_base_n[nxt], "Thermal_White")

    # 3 High-Gain Parabolic Communications Dishes at Y = 120m, 140m, 160m
    for y_pos, d_rad in [(120.0, 4.0), (140.0, 3.5), (160.0, 3.0)]:
        add_sphere(5.0, y_pos, 0.0, d_rad, rings=12, sectors=16, mat="Gold_Foil")

    # 4 Radial Cold-Gas RCS Thruster Outriggers at Y = 130m
    add_box(-18.0, 18.0, 129.4, 130.6, -0.6, 0.6, mat="Composite_Corridor")
    add_box(-0.6, 0.6, 129.4, 130.6, -18.0, 18.0, mat="Composite_Corridor")

    # 7. Continuous 400m Graphene Elevator Tether Ribbon (Y: -200m to +200m)
    add_box(-0.5, 0.5, -200.0, 200.0, -0.002, 0.002, mat="Graphene_Tether")

    print(f"[2/5] Generated {len(vertices):,} vertices, {len(normals):,} normals, {len(faces):,} polygonal faces.")

    # ---------------------------------------------------------
    # Write Wavefront Material Library (.mtl)
    # ---------------------------------------------------------
    print("[3/5] Writing Material Library (.mtl)...")
    mtl_content = """# Space Elevator Materials Library
newmtl Torus_Hab_White
Ka 0.25 0.25 0.25
Kd 0.92 0.94 0.96
Ks 0.40 0.40 0.40
Ns 45.0
d 1.0

newmtl Photovoltaic_Blue
Ka 0.10 0.15 0.35
Kd 0.08 0.18 0.55
Ks 0.95 0.95 0.98
Ns 95.0
d 1.0

newmtl Biosphere_Glass
Ka 0.20 0.35 0.45
Kd 0.55 0.80 0.92
Ks 0.95 0.95 0.95
Ns 120.0
d 0.45

newmtl Titanium_Core
Ka 0.20 0.20 0.22
Kd 0.68 0.70 0.74
Ks 0.70 0.70 0.72
Ns 60.0
d 1.0

newmtl Composite_Corridor
Ka 0.15 0.15 0.16
Kd 0.35 0.37 0.40
Ks 0.30 0.30 0.30
Ns 25.0
d 1.0

newmtl Gold_Foil
Ka 0.30 0.22 0.05
Kd 0.88 0.72 0.18
Ks 0.95 0.85 0.40
Ns 85.0
d 1.0

newmtl Thermal_White
Ka 0.30 0.30 0.30
Kd 0.95 0.95 0.97
Ks 0.30 0.30 0.30
Ns 30.0
d 1.0

newmtl Graphene_Tether
Ka 0.10 0.12 0.15
Kd 0.18 0.22 0.28
Ks 0.65 0.65 0.70
Ns 50.0
d 1.0
"""
    with open(mtl_path, "w", encoding="utf-8") as f:
        f.write(mtl_content)

    # ---------------------------------------------------------
    # Write Wavefront 3D Object (.obj)
    # ---------------------------------------------------------
    print("[4/5] Writing Wavefront 3D Object (.obj)...")
    with open(obj_path, "w", encoding="utf-8") as f:
        f.write("# Space Elevator GEO Orbital Station (Node-01)\n")
        f.write("# High-Fidelity 3D Wavefront OBJ Export\n")
        f.write(f"mtllib {os.path.basename(mtl_path)}\n\n")

        # Vertices
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

        # Normals
        for n in normals:
            f.write(f"vn {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n")

        # Faces grouped by material
        current_mat = None
        for face_v, face_n, mat in faces:
            if mat != current_mat:
                current_mat = mat
                f.write(f"usemtl {current_mat}\n")
                f.write(f"g {current_mat}\n")
            
            # 1-based indexing
            f_str = " ".join([f"{fv}//{fn}" for fv, fn in zip(face_v, face_n)])
            f.write(f"f {f_str}\n")

    file_size = os.path.getsize(obj_path)
    mtl_size = os.path.getsize(mtl_path)
    print(f"[5/5] SUCCESS! Created 3D OBJ file ({file_size:,} bytes) and MTL ({mtl_size:,} bytes)")
    print(f"      OBJ: {obj_path}")
    print(f"      MTL: {mtl_path}")

if __name__ == "__main__":
    create_space_elevator_obj()
