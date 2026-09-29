import numpy as np, trimesh, math
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals
from PIL import Image, ImageDraw, ImageFont
import os
OUT="/home/claude/content/models"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s):
    try: return ImageFont.truetype(FONT,s)
    except: return ImageFont.load_default()

def mat(color, metal=0.0, rough=0.6, emissive=None, alpha=None):
    c=[int(x*255) if x<=1 else int(x) for x in color[:3]]
    a=255 if alpha is None else int(alpha*255)
    m=PBRMaterial(baseColorFactor=c+[a], metallicFactor=metal, roughnessFactor=rough,
                  doubleSided=True)
    if emissive is not None:
        m.emissiveFactor=list(emissive)
    if alpha is not None: m.alphaMode="BLEND"
    return m

def paint(mesh, m):
    mesh.visual=TextureVisuals(material=m); return mesh

def box(ext,pos,m):
    b=trimesh.creation.box(extents=ext); b.apply_translation(pos); return paint(b,m)

def cyl(r,h,pos,m,axis='y',sections=32):
    c=trimesh.creation.cylinder(radius=r,height=h,sections=sections)
    if axis=='y': c.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0]))
    elif axis=='x': c.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
    c.apply_translation(pos); return paint(c,m)

def sph(r,pos,m,scale=(1,1,1),sub=3):
    s=trimesh.creation.icosphere(subdivisions=sub,radius=r)
    s.apply_scale(scale); s.apply_translation(pos); return paint(s,m)

def cone(r,h,pos,m,sections=24):
    c=trimesh.creation.cone(radius=r,height=h,sections=sections)
    c.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0]))
    c.apply_translation(pos); return paint(c,m)

def save(name, meshes):
    sc=trimesh.Scene()
    for i,m in enumerate(meshes): sc.add_geometry(m,geom_name=f"{name}_{i}")
    path=f"{OUT}/{name}.glb"; sc.export(path); print(name, os.path.getsize(path)//1024,"KB")

RED=(0.80,0.08,0.06); BLACK=(0.08,0.08,0.09); BLUE=(0.10,0.30,0.75); SILVER=(0.75,0.77,0.80)
YEL=(1.0,0.78,0.05)

# ---------- Fire extinguishers ----------
def extinguisher(name, band_color, horn=False, nozzle_color=BLACK):
    red=mat(RED,0.3,0.35); band=mat(band_color,0.1,0.5); sil=mat(SILVER,0.9,0.3); blk=mat(BLACK,0.1,0.7)
    ms=[]
    R=0.075; H=0.42
    ms.append(cyl(R,H,[0,H/2,0],red))
    ms.append(sph(R,[0,H,0],red,(1,0.55,1)))
    ms.append(sph(R,[0,0.0,0],red,(1,0.25,1)))
    ms.append(cyl(R+0.002,0.05,[0,0.24,0],band))
    ms.append(cyl(0.03,0.05,[0,H+0.06,0],sil))          # neck
    ms.append(cyl(0.035,0.02,[0,H+0.10,0],blk))         # valve cap
    ms.append(box([0.16,0.018,0.03],[0.02,H+0.13,0],blk))  # top lever
    ms.append(box([0.12,0.015,0.03],[0.03,H+0.09,0],blk))  # lower handle
    ms.append(cyl(0.028,0.012,[0.05,H+0.045,-0.06],sil,axis='z')) # gauge
    ms.append(cyl(0.02,0.012,[0.05,H+0.045,-0.067],mat((0.95,0.95,0.95)),axis='z'))
    # hose
    ang=np.linspace(0,math.pi*0.95,16)
    for a in ang:
        ms.append(sph(0.009,[0.06+0.055*math.sin(a),H+0.02-0.13*(a/math.pi)-0.02*math.sin(a), 0.075*math.cos(a)*0+0.075],blk,sub=1))
    ms.append(cyl(0.013 if not horn else 0.02, 0.06 if not horn else 0.16,
                  [0.115,H-0.12,0.075] if not horn else [0.12,H-0.16,0.085],
                  mat(nozzle_color,0.1,0.6) if not horn else blk))
    save(name,ms)
extinguisher("extinguisher_water",BLUE,False,SILVER)
extinguisher("extinguisher_co2",BLACK,True)
extinguisher("extinguisher_powder",(0.15,0.35,0.85),False)
# fix band colors semantics: water = red body, silver-blue band; CO2 = black band + horn; powder = blue band

# ---------- Fire / flames ----------
def flames():
    ms=[]
    layers=[((1.0,0.25,0.02),(1.0,0.2,0.0),0.28,0.75,1.0),
            ((1.0,0.55,0.05),(1.0,0.45,0.0),0.20,0.60,0.9),
            ((1.0,0.90,0.30),(1.0,0.8,0.1),0.11,0.42,0.85)]
    rng=np.random.default_rng(3)
    for col,em,r,h,a in layers:
        for i in range(7):
            ang=rng.uniform(0,2*math.pi); d=rng.uniform(0,r*0.8) if col[1]<0.9 else rng.uniform(0,r*0.3)
            hh=h*rng.uniform(0.6,1.15); rr=r*rng.uniform(0.5,0.9)
            c=cone(rr,hh,[d*math.cos(ang),0,d*math.sin(ang)],mat(col,0,0.9,emissive=em,alpha=a))
            ms.append(c)
    ms.append(cyl(0.34,0.03,[0,0.005,0],mat((0.1,0.06,0.04),0,1.0),sections=32))  # scorched base
    save("fire_flames",ms)
flames()

# ---------- Exit sign ----------
def exit_sign():
    W,H=1024,384
    im=Image.new("RGB",(W,H),(0,140,60)); d=ImageDraw.Draw(im)
    d.rectangle([10,10,W-10,H-10],outline=(255,255,255),width=10)
    d.text((W*0.62,H/2),"EXIT",font=font(210),fill=(255,255,255),anchor="mm")
    # running man pictogram (simplified)
    cx,cy=200,H/2
    d.ellipse([cx-20,cy-115,cx+20,cy-75],fill="white")
    d.line([cx-5,cy-70,cx-20,cy+10],fill="white",width=24)
    d.line([cx-15,cy+5,cx-60,cy+50],fill="white",width=20); d.line([cx-60,cy+50,cx-90,cy+40],fill="white",width=18)
    d.line([cx-15,cy+5,cx+30,cy+40],fill="white",width=20); d.line([cx+30,cy+40,cx+35,cy+95],fill="white",width=18)
    d.line([cx-5,cy-55,cx+50,cy-35],fill="white",width=16); d.line([cx-5,cy-55,cx-55,cy-40],fill="white",width=16)
    d.polygon([(330,cy),(400,cy-50),(400,cy-20),(450,cy-20),(450,cy+20),(400,cy+20),(400,cy+50)],fill="white")
    tex=f"{OUT}/_exit_tex.png"; im.save(tex)
    body=box([0.5,0.19,0.04],[0,0,0],mat((0.05,0.35,0.15),0.1,0.6))
    body.apply_translation([0,0.095,0])
    # textured front quad
    w,h=0.48,0.18; z=0.0205
    v=np.array([[-w/2,0.005,z],[w/2,0.005,z],[w/2,0.005+h,z],[-w/2,0.005+h,z]])
    q=trimesh.Trimesh(v,[[0,1,2],[0,2,3]],process=False)
    uv=np.array([[0,0],[1,0],[1,1],[0,1]])
    m=PBRMaterial(baseColorTexture=Image.open(tex),emissiveTexture=Image.open(tex),emissiveFactor=[1,1,1],doubleSided=True)
    q.visual=TextureVisuals(uv=uv,material=m)
    # back face too so it reads from both sides
    v2=v.copy(); v2[:,2]=-z
    q2=trimesh.Trimesh(v2,[[0,2,1],[0,3,2]],process=False); q2.visual=TextureVisuals(uv=uv,material=m)
    save("exit_sign",[body,q,q2]); os.remove(tex)
exit_sign()

# ---------- Gas monitor ----------
def gas_monitor():
    W,H=256,320
    im=Image.new("RGB",(W,H),(20,45,25)); d=ImageDraw.Draw(im)
    d.text((W/2,50),"CH4",font=font(44),fill=(120,255,140),anchor="mm")
    d.text((W/2,130),"0.0",font=font(84),fill=(120,255,140),anchor="mm")
    d.text((W/2,200),"% LEL",font=font(40),fill=(120,255,140),anchor="mm")
    d.text((W/2,265),"O2 20.9  CO 0",font=font(30),fill=(120,255,140),anchor="mm")
    tex=f"{OUT}/_gm.png"; im.save(tex)
    yel=mat(YEL,0.0,0.5); blk=mat(BLACK,0.0,0.7); sil=mat(SILVER,0.8,0.35)
    ms=[box([0.07,0.13,0.032],[0,0.065,0],yel),
        box([0.074,0.012,0.036],[0,0.006,0],blk),box([0.074,0.02,0.036],[0,0.122,0],blk),
        cyl(0.007,0.05,[0.025,0.155,0],blk),                     # antenna/sensor
        box([0.05,0.018,0.02],[0,0.146,0.0],blk),
        box([0.018,0.05,0.008],[0,0.065,-0.019],sil)]            # back clip
    # sensor grille dots
    for i in range(3): ms.append(cyl(0.006,0.004,[-0.02+0.02*i,0.128,0.019],mat((0.3,0.3,0.3)),axis='z',sections=12))
    w,h=0.05,0.06; z=0.0165
    v=np.array([[-w/2,0.06,z],[w/2,0.06,z],[w/2,0.06+h,z],[-w/2,0.06+h,z]])
    q=trimesh.Trimesh(v,[[0,1,2],[0,2,3]],process=False)
    q.visual=TextureVisuals(uv=np.array([[0,0],[1,0],[1,1],[0,1]]),
        material=PBRMaterial(baseColorTexture=Image.open(tex),emissiveTexture=Image.open(tex),emissiveFactor=[1,1,1]))
    ms.append(q)
    for i,c in enumerate([(0.9,0.1,0.1),(0.2,0.8,0.2)]):
        ms.append(cyl(0.008,0.004,[-0.016+0.032*i,0.038,0.0175],mat(c,0,0.5),axis='z',sections=16))
    save("gas_monitor",ms); os.remove(tex)
gas_monitor()

# ---------- Gas cloud ----------
def gas_cloud():
    rng=np.random.default_rng(7); ms=[]
    for i in range(14):
        p=rng.normal(0,0.35,3)*[1,0.6,1]; r=rng.uniform(0.25,0.5)
        g=rng.uniform(0.55,0.85)
        ms.append(sph(r,p+[0,0.5,0],mat((0.55*g,0.9*g,0.2),0,1.0,emissive=(0.05,0.12,0.02),alpha=rng.uniform(0.18,0.32)),
                      scale=(1,rng.uniform(0.7,1.0),1),sub=2))
    save("gas_cloud",ms)
gas_cloud()

# ---------- PPE ----------
def hard_hat():
    yel=mat(YEL,0.0,0.4); blk=mat(BLACK,0.0,0.8)
    dome=trimesh.creation.icosphere(subdivisions=4,radius=0.12)
    dome=dome.slice_plane([0,0,0],[0,1,0],cap=False)
    dome.apply_scale([1,0.95,1.12]); dome.apply_translation([0,0.02,0]); paint(dome,yel)
    ms=[dome]
    ms.append(cyl(0.128,0.012,[0,0.02,0],yel,sections=48))
    brim=box([0.16,0.008,0.08],[0,0.024,0.15],yel); ms.append(brim)
    for x in (-0.03,0,0.03): ms.append(box([0.014,0.02,0.24],[x,0.13,0.0],yel)) if x==0 else None
    ms.append(box([0.03,0.02,0.25],[0,0.135,0.0],yel))
    ms.append(cyl(0.11,0.02,[0,0.028,0],blk,sections=48))
    ms.append(box([0.06,0.03,0.006],[0,0.075,0.139],mat((0.95,0.95,0.95))))
    save("ppe_hard_hat",ms)
hard_hat()

def boots():
    blk=mat((0.10,0.09,0.08),0.0,0.7); sole=mat((0.35,0.25,0.12),0.0,0.9); steel=mat(SILVER,0.8,0.4)
    ms=[]
    for s in (-1,1):
        x=0.07*s
        ms.append(box([0.09,0.03,0.30],[x,0.015,0.03],sole))
        ms.append(box([0.088,0.03,0.09],[x,0.045,0.08],blk))  # toe
        ms.append(sph(0.045,[x,0.06,0.10],blk,(1,0.75,1.4)))
        ms.append(box([0.085,0.05,0.16],[x,0.06,0.02],blk))
        ms.append(cyl(0.048,0.20,[x,0.16,-0.03],blk,sections=24))
        ms.append(box([0.06,0.014,0.03],[x,0.20,0.03],mat((0.7,0.7,0.7))))  # tongue-lace strip
        ms.append(cyl(0.052,0.02,[x,0.265,-0.03],mat((0.2,0.2,0.2)),sections=24))
        ms.append(box([0.09,0.03,0.06],[x,0.015,-0.13],mat((0.25,0.18,0.1))))  # heel
        ms.append(box([0.05,0.012,0.02],[x,0.09,0.11],steel))  # steel toe hint
    save("ppe_safety_boots",ms)
boots()

def vest():
    org=mat((1.0,0.42,0.03),0.0,0.7); ref=mat((0.85,0.87,0.9),0.9,0.25)
    ms=[]
    ms.append(box([0.17,0.55,0.03],[-0.12,0.35,0.11],org))   # front left
    ms.append(box([0.17,0.55,0.03],[0.12,0.35,0.11],org))    # front right
    ms.append(box([0.40,0.55,0.03],[0,0.35,-0.11],org))      # back
    for s in (-1,1):
        ms.append(box([0.09,0.06,0.20],[0.155*s,0.63,0.0],org))  # shoulders  (straps)
        ms.append(box([0.03,0.55,0.20],[0.205*s,0.35,0.0],org))  # sides
    for y in (0.24,0.42):
        ms.append(box([0.17,0.045,0.033],[-0.12,y,0.113],ref)); ms.append(box([0.17,0.045,0.033],[0.12,y,0.113],ref))
        ms.append(box([0.40,0.045,0.033],[0,y,-0.113],ref))
    for s in (-1,1):
        ms.append(box([0.035,0.55,0.034],[0.135*s,0.35,0.113],ref))
        ms.append(box([0.035,0.34,0.034],[0.09*s,0.35,-0.113],ref)) if False else None
    ms.append(box([0.006,0.55,0.034],[0,0.35,0.116],mat((0.5,0.5,0.5),0.6,0.4)))  # zipper
    save("ppe_hivis_vest",[m for m in ms if m is not None])
vest()
