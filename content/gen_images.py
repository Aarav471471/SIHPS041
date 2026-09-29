from PIL import Image, ImageDraw, ImageFont
import math, os
IMG="/home/claude/content/images"; ICON=IMG+"/appicon"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def F(s): return ImageFont.truetype(B,s)

def draw_icon(S, bg=True):
    k=4; W=S*k
    im=Image.new("RGBA",(W,W),(0,0,0,0)); d=ImageDraw.Draw(im)
    if bg:
        # vertical gradient background
        for y in range(W):
            t=y/W; d.line([(0,y),(W,y)],fill=(int(20+10*t),int(40+30*t),int(90+50*t),255))
    s=W/1024
    # shield
    cx=W/2
    pts=[(cx-300*s,230*s),(cx,150*s),(cx+300*s,230*s),(cx+280*s,560*s),(cx,880*s),(cx-280*s,560*s)]
    d.polygon(pts,fill=(255,255,255,255))
    inner=[(cx-255*s,255*s),(cx,185*s),(cx+255*s,255*s),(cx+238*s,548*s),(cx,832*s),(cx-238*s,548*s)]
    d.polygon(inner,fill=(255,178,0,255))
    # hard hat
    d.pieslice([cx-170*s,300*s,cx+170*s,640*s],180,360,fill=(30,30,30,255))
    d.rectangle([cx-215*s,470*s,cx+215*s,500*s],fill=(30,30,30,255))
    d.rectangle([cx-30*s,300*s,cx+30*s,470*s],fill=(255,178,0,255))
    # flame
    fx,fy=cx,760*s
    d.polygon([(fx,fy-215*s),(fx+95*s,fy-70*s),(fx+70*s,fy+30*s),(fx,fy+60*s),(fx-70*s,fy+30*s),(fx-95*s,fy-70*s)],fill=(220,40,20,255))
    d.polygon([(fx,fy-100*s),(fx+45*s,fy-20*s),(fx+30*s,fy+30*s),(fx,fy+45*s),(fx-30*s,fy+30*s),(fx-45*s,fy-20*s)],fill=(255,220,60,255))
    return im.resize((S,S),Image.LANCZOS)

draw_icon(1024).save(f"{IMG}/app_icon_1024.png")
draw_icon(512).save(f"{IMG}/app_icon_512_playstore.png")
for name,px in [("mipmap-mdpi",48),("mipmap-hdpi",72),("mipmap-xhdpi",96),("mipmap-xxhdpi",144),("mipmap-xxxhdpi",192)]:
    os.makedirs(f"{ICON}/{name}",exist_ok=True)
    ic=draw_icon(px)
    ic.save(f"{ICON}/{name}/ic_launcher.png")
    # round variant
    m=Image.new("L",(px,px),0); ImageDraw.Draw(m).ellipse([0,0,px-1,px-1],fill=255)
    r=Image.new("RGBA",(px,px),(0,0,0,0)); r.paste(ic,(0,0),m); r.save(f"{ICON}/{name}/ic_launcher_round.png")
# adaptive icon layers (432px, safe zone in centre 66%)
fg=Image.new("RGBA",(432,432),(0,0,0,0)); g=draw_icon(285,bg=False); fg.paste(g,(73,73),g); fg.save(f"{ICON}/ic_launcher_foreground_432.png")
Image.new("RGBA",(432,432),(25,50,110,255)).save(f"{ICON}/ic_launcher_background_432.png")

# ---- Placeholder logos (NOT official emblems) ----
def badge(path,title,sub,color,W=900,H=300,mono=None):
    k=2; im=Image.new("RGBA",(W*k,H*k),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([20*k,20*k,280*k,280*k],fill=color,outline=(255,255,255,255),width=6*k)
    d.ellipse([50*k,50*k,250*k,250*k],outline=(255,255,255,255),width=4*k)
    d.text((150*k,150*k),mono,font=F(80*k),fill=(255,255,255,255),anchor="mm")
    d.text((320*k,120*k),title,font=F(64*k),fill=(20,30,60,255),anchor="lm")
    d.text((320*k,195*k),sub,font=F(34*k),fill=(90,100,120,255),anchor="lm")
    im.resize((W,H),Image.LANCZOS).save(path)
badge(f"{IMG}/logo_govt_jharkhand_PLACEHOLDER.png","Government of Jharkhand","Placeholder - replace with official emblem",(20,110,60,255),mono="JH")
badge(f"{IMG}/logo_dgms_PLACEHOLDER.png","DGMS","Directorate General of Mines Safety (placeholder)",(30,60,140,255),mono="DG")
