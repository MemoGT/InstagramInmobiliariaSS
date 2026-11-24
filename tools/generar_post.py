#!/usr/bin/env python3
"""Generador de posts de Inmobiliaria SS (1080x1350, 4:5).

Uso:
  python3 generar_post.py spec.json

spec.json (ejemplo):
{
  "foto": "/ruta/foto.jpg",          # opcional; si falta, fondo azul liso
  "etiqueta": "PARA COMPRADORES",
  "titulo": "Comprar bien empieza por tu presupuesto",
  "items": ["Punto 1", "Punto 2", "Punto 3"],   # opcional (lista numerada)
  "texto": "Texto de apoyo",                      # opcional (si no hay items)
  "boton": "Escríbenos por WhatsApp",             # opcional
  "cierre": "Frase final dorada",                 # opcional (con items)
  "salida": "post.jpg"
}
Fuentes: Caladea Bold (títulos), Inter (texto). Pie: INMOBILIARIA SS | WhatsApp 3287-5430.
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1350
NAVY=(14,28,48); GOLD=(201,162,89); CREAM=(246,241,231)
SER="/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf"
INT="/usr/share/fonts/opentype/inter/Inter-Regular.otf"
INB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F=lambda p,s: ImageFont.truetype(p,s)

def wrap(d,t,font,maxw):
    out=[];cur=""
    for w in t.split():
        x=(cur+" "+w).strip()
        if d.textlength(x,font=font)<=maxw: cur=x
        else: out.append(cur);cur=w
    out.append(cur);return out

def block(d,text,font,y,fill,gap=1.25,x=110,maxw=W-220):
    for l in wrap(d,text,font,maxw):
        d.text((x,y),l,font=font,fill=fill);y+=int(font.size*gap)
    return y

def fondo(foto,blur=6,tint=0.7):
    if not foto:
        return Image.new("RGB",(W,H),NAVY)
    ph=Image.open(foto).convert("RGB")
    s=W/ph.width; ph=ph.resize((W,int(ph.height*s)))
    if ph.height>=H:
        top=(ph.height-H)//2; ph=ph.crop((0,top,W,top+H))
    else: ph=ph.resize((W,H))
    ph=ImageEnhance.Contrast(ph.filter(ImageFilter.GaussianBlur(blur))).enhance(1.1)
    mask=Image.new("L",(W,H),0);md=ImageDraw.Draw(mask)
    for y in range(H):
        t=abs(y/H-0.5)*2
        md.line([(0,y),(W,y)],fill=min(int(255*(tint+(0.97-tint)*t**2)),255))
    return Image.composite(Image.new("RGB",(W,H),NAVY),ph,mask)

def generar(spec):
    im=fondo(spec.get("foto")); d=ImageDraw.Draw(im)
    d.rectangle([60,60,W-60,H-60],outline=GOLD,width=3)
    # etiqueta
    fnt=F(INB,28); et=spec["etiqueta"]; tw=d.textlength(et,font=fnt)
    d.rounded_rectangle([110,116,110+tw+48,176],radius=30,outline=GOLD,width=3)
    d.text((134,132),et,font=fnt,fill=GOLD)
    items=spec.get("items")
    tam=68 if items else 80
    y=block(d,spec["titulo"],F(SER,tam),290,CREAM,1.2)
    if items:
        y+=45
        for i,t in enumerate(items,1):
            d.ellipse([110,y,190,y+80],outline=GOLD,width=4,fill=NAVY)
            d.text((150,y+40),str(i),font=F(INB,40),fill=GOLD,anchor="mm")
            yy=block(d,t,F(INB,38),y+8,CREAM,1.3,x=225,maxw=W-335)
            y=max(y+108,yy+30)
        if spec.get("cierre"): block(d,spec["cierre"],F(INT,38),y+20,GOLD)
    else:
        d.line([(110,y+30),(310,y+30)],fill=GOLD,width=5)
        if spec.get("texto"):
            y=block(d,spec["texto"],F(INT,40),y+80,CREAM,1.4)
        if spec.get("boton"):
            d.rounded_rectangle([110,y+60,W-110,y+190],radius=14,fill=GOLD)
            d.text((W//2,y+125),spec["boton"],font=F(INB,40),fill=NAVY,anchor="mm")
    # pie
    d.line([(110,H-170),(W-110,H-170)],fill=GOLD,width=2)
    d.text((110,H-140),"INMOBILIARIA SS",font=F(INB,30),fill=GOLD)
    d.text((W-110,H-140),"WhatsApp 3287-5430",font=F(INB,30),fill=CREAM,anchor="ra")
    im.save(spec.get("salida","post.jpg"),quality=95)

if __name__=="__main__":
    generar(json.load(open(sys.argv[1],encoding="utf-8")))
