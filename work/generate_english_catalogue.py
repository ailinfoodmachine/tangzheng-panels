import io, json, math, re
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'dist/assets'
PRODUCTS=ASSETS/'products'
OUT=ASSETS/'TANGZHENG-English-Catalogue.pdf'
PHONE='+86 155 8886 9611'; EMAIL='15588869611@163.com'; WA='https://wa.me/8615588869611'; SITE='https://tangzhengpanels.com'
GREEN=HexColor('#164a42'); TEAL=HexColor('#1d766b'); GOLD=HexColor('#e7b05d'); INK=HexColor('#102a29'); MUTED=HexColor('#667472'); PAPER=HexColor('#f7f3e9')
W,H=landscape(A4)

src=(ROOT/'src/render.js').read_text()
items=json.loads(re.search(r'const fullCatalog=(\[[\s\S]*?\]);',src).group(1))
seen=set(); items=[x for x in items if not (x['code'] in seen or seen.add(x['code']))]

qr_img=Image.open(ASSETS/'contact-qr.png').convert('RGB')
qr_buf=io.BytesIO();qr_img.save(qr_buf,format='PNG');qr_buf.seek(0);QR=ImageReader(qr_buf)

def fit_text(c,text,x,y,maxw,size=10,font='Helvetica',leading=None,color=INK):
    leading=leading or size*1.25;c.setFillColor(color);c.setFont(font,size)
    words=text.split();lines=[];line=''
    for word in words:
        candidate=(line+' '+word).strip()
        if c.stringWidth(candidate,font,size)<=maxw: line=candidate
        else:
            if line:lines.append(line)
            line=word
    if line:lines.append(line)
    for ln in lines:c.drawString(x,y,ln);y-=leading
    return y

def footer(c,page):
    c.setStrokeColor(HexColor('#d7ded8'));c.line(34,31,W-34,31)
    c.setFillColor(MUTED);c.setFont('Helvetica',7.5)
    c.drawString(34,18,f'TANGZHENG  |  {PHONE}  |  {EMAIL}  |  {SITE}')
    c.drawRightString(W-78,18,f'{page:02d}')
    c.drawImage(QR,W-68,5,54,54,mask='auto')
    c.setFont('Helvetica-Bold',5.8);c.setFillColor(GREEN);c.drawCentredString(W-41,3,'WHATSAPP')

def header(c,title,subtitle=None):
    c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(GREEN);c.roundRect(34,H-72,W-68,38,8,fill=1,stroke=0)
    c.setFillColor(white);c.setFont('Helvetica-Bold',20);c.drawString(50,H-59,title)
    if subtitle:c.setFont('Helvetica',9);c.drawRightString(W-50,H-57,subtitle)

def draw_image_fit(c,path,x,y,w,h):
    im=Image.open(path).convert('RGB');im.thumbnail((1000,650),Image.Resampling.LANCZOS)
    iw,ih=im.size;scale=min(w/iw,h/ih);nw,nh=iw*scale,ih*scale
    buf=io.BytesIO();im.save(buf,format='JPEG',quality=84,optimize=True);buf.seek(0)
    c.drawImage(ImageReader(buf),x+(w-nw)/2,y+(h-nh)/2,nw,nh,mask='auto')

def cover(c):
    c.setFillColor(INK);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(TEAL);c.circle(W-70,H-40,240,fill=1,stroke=0)
    c.setFillColor(GOLD);c.circle(W-40,20,155,fill=1,stroke=0)
    c.setFillColor(white);c.setFont('Helvetica-Bold',18);c.drawString(55,H-70,'TANGZHENG')
    c.setFont('Helvetica-Bold',38);c.drawString(55,H-160,'INSULATED DECORATIVE')
    c.drawString(55,H-208,'METAL WALL PANELS')
    c.setFont('Helvetica',15);c.drawString(57,H-242,'English product catalogue · 152 finish models')
    draw_image_fit(c,PRODUCTS/'05-sbg-003.jpg',55,118,310,150)
    draw_image_fit(c,PRODUCTS/'06-am-058.jpg',382,118,210,150)
    draw_image_fit(c,PRODUCTS/'07-mv-005.jpg',609,118,175,150)
    c.setFillColor(white);c.setFont('Helvetica-Bold',13);c.drawString(55,82,'Project enquiries and physical sample requests')
    c.setFont('Helvetica',11);c.drawString(55,60,f'{PHONE}  ·  {EMAIL}')
    c.drawImage(QR,W-142,30,86,86,mask='auto');c.setFont('Helvetica-Bold',8);c.drawCentredString(W-99,19,'SCAN FOR WHATSAPP')

def info_page(c,page):
    header(c,'PRODUCT SYSTEM OVERVIEW','English edition')
    c.setFillColor(INK);c.setFont('Helvetica-Bold',26);c.drawString(45,H-120,'Three-layer decorative wall panel')
    y=H-160
    blocks=[('1  DECORATIVE METAL SURFACE','Coated Al-Zn alloy steel sheet, or aluminium sheet as specified for the selected product.'),('2  RIGID INSULATION CORE','Rigid polyurethane core in the catalogue construction. Confirm the exact core and project requirements before ordering.'),('3  INNER BACKING LAYER','Aluminium foil or glass-fibre fabric backing, depending on the confirmed product construction.')]
    for title,body in blocks:
        c.setFillColor([GOLD,TEAL,GREEN][len(blocks)%3]);c.roundRect(45,y-46,310,58,8,fill=1,stroke=0)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',12);c.drawString(60,y-5,title)
        fit_text(c,body,60,y-23,275,8.5,color=INK);y-=82;blocks=blocks
    c.setFillColor(white);c.roundRect(395,H-360,390,240,12,fill=1,stroke=0)
    c.setFillColor(GREEN);c.setFont('Helvetica-Bold',18);c.drawString(420,H-155,'CATALOGUE REFERENCE SPECIFICATION')
    rows=[('Panel size','3800 × 380 × 16 mm'),('Packing size','3850 × 380 × 16 mm'),('Catalogue weight','3.7 kg/m²'),('Packing quantity','8 panels / package')]
    yy=H-195
    for a,b in rows:
        c.setFillColor(MUTED);c.setFont('Helvetica',10);c.drawString(420,yy,a)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',11);c.drawRightString(755,yy,b);c.setStrokeColor(HexColor('#dfe4df'));c.line(420,yy-9,755,yy-9);yy-=42
    fit_text(c,'These figures reproduce the supplied catalogue. Confirm current dimensions, construction, tolerances, packing and all test documents in the written quotation for the selected model.',420,H-385,335,9,color=MUTED)
    footer(c,page)

def features_page(c,page):
    header(c,'WHY BUYERS CHOOSE THIS PANEL FORMAT','Project-specific verification remains essential')
    cards=[('THERMAL INSULATION','An integrated insulation core can support exterior wall thermal design when the complete assembly is properly specified.'),('FAST INSTALLATION','Large, lightweight panels can reduce wet trades and simplify wall covering work on suitable substrates.'),('LIGHTWEIGHT FORMAT','Catalogue weight is 3.7 kg/m². Structural support and fixings must still be designed for the project.'),('WEATHER DETAILING','Joints, corners, openings, flashings and sealants must be planned as part of the complete wall system.'),('DURABLE FINISH OPTIONS','Brick, stone, wood, marble, corrugated and plain appearances provide a broad material palette.'),('RENOVATION FLEXIBILITY','Panels may be considered for new walls and exterior renovation after the existing wall has been assessed.')]
    for i,(title,body) in enumerate(cards):
        col=i%3;row=i//3;x=45+col*255;y=H-145-row*185
        c.setFillColor(white);c.roundRect(x,y-135,225,145,12,fill=1,stroke=0)
        c.setFillColor([GOLD,TEAL,GREEN][col]);c.circle(x+25,y-18,13,fill=1,stroke=0)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',12);c.drawString(x+48,y-23,title)
        fit_text(c,body,x+20,y-54,185,9,color=MUTED)
    footer(c,page)

def accessories_page(c,page):
    header(c,'DECORATIVE TRIMS & ACCESSORIES','Confirm compatible profiles for the selected panel')
    rows=[('Outside corner cap','YM-10590A','Spray-moulded aluminium alloy','Exterior corner base A'),('Inside corner base / cap','YM-10710A','Aluminium alloy','Internal and external corner cover'),('Door / window trim','YM-20313E','Spray-moulded aluminium alloy','External corner pedestal F'),('External corner trim','YM-20313C / YM-20314','Spray-moulded aluminium alloy','Multi-function decorative trim'),('Starter','YM-2968','Spray-moulded aluminium alloy','Starter profile'),('Invisible starter','YM-10590','Aluminium alloy','Built-in starter'),('Middle seam base','YM-10590A / PVC-20054','Spray-moulded aluminium alloy','Panel connection base A'),('Middle seam cap','BH-20051A','Panel material + aluminium alloy','Panel connection buckle A'),('Cover and base set','YM-2969 / YM-2970','Aluminium alloy','Fastening cover and base'),('F profile','YM-2966','Spray-moulded aluminium alloy','Window, door and corner trim'),('Large / small positive corner','BH-20050','Panel material + galvanised light steel','Matching positive-corner parts'),('Asphalt tile trim','BH-20050','Panel material + galvanised light steel','Roof-edge waterproof decoration')]
    c.setFillColor(GREEN);c.rect(45,H-115,750,25,fill=1,stroke=0)
    for x,t in zip([55,230,355,555],['ACCESSORY','MODEL','MATERIAL','PURPOSE']):c.setFillColor(white);c.setFont('Helvetica-Bold',8);c.drawString(x,H-107,t)
    yy=H-137
    for i,row in enumerate(rows):
        if i%2==0:c.setFillColor(white);c.rect(45,yy-20,750,28,fill=1,stroke=0)
        for x,t in zip([55,230,355,555],row):c.setFillColor(INK if i%2==0 else MUTED);c.setFont('Helvetica-Bold' if x==55 else 'Helvetica',7.4);c.drawString(x,yy,t[:38])
        yy-=31
    footer(c,page)

def product_page(c,page,title,subset,part=None):
    heading=title+(f' · {part}' if part else '')
    header(c,heading.upper(),'Finish images from the supplied catalogue')
    n=len(subset);cols=5 if n>12 else 4;rows=math.ceil(n/cols)
    gap=10;x0=44;y_top=H-95;bottom=65;cellw=(W-88-gap*(cols-1))/cols;cellh=(y_top-bottom-gap*(rows-1))/rows
    for i,item in enumerate(subset):
        col=i%cols;row=i//cols;x=x0+col*(cellw+gap);y=y_top-(row+1)*cellh-row*gap
        c.setFillColor(white);c.roundRect(x,y,cellw,cellh,7,fill=1,stroke=0)
        img_h=cellh-27;draw_image_fit(c,PRODUCTS/item['image'],x+4,y+23,cellw-8,img_h-5)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',8.5);c.drawString(x+7,y+9,item['code'])
        c.setFillColor(MUTED);c.setFont('Helvetica',6.5);c.drawRightString(x+cellw-7,y+9,'Physical sample recommended')
    footer(c,page)

def project_page(c,page):
    header(c,'PROJECT & ORDERING CHECKLIST','Use the exact model code in every enquiry')
    c.setFillColor(INK);c.setFont('Helvetica-Bold',27);c.drawString(45,H-125,'Information needed for an accurate discussion')
    checklist=['Project country, city and building use','New construction or renovation','Wall dimensions, drawings and approximate quantity','Selected finish model codes and physical sample request','Required thermal, fire, structural and weather documents','Openings, corners, parapets, base details and accessories','Delivery destination and target schedule']
    yy=H-175
    for i,t in enumerate(checklist,1):
        c.setFillColor(GOLD if i%2 else TEAL);c.circle(60,yy+3,12,fill=1,stroke=0);c.setFillColor(INK);c.setFont('Helvetica-Bold',9);c.drawCentredString(60,yy,str(i));c.setFont('Helvetica',12);c.drawString(85,yy-2,t);yy-=46
    c.setFillColor(GREEN);c.roundRect(500,H-420,280,300,15,fill=1,stroke=0)
    c.setFillColor(white);c.setFont('Helvetica-Bold',20);c.drawString(530,H-165,'CONTACT TANGZHENG')
    c.setFont('Helvetica',12);c.drawString(530,H-205,PHONE);c.drawString(530,H-235,EMAIL);c.drawString(530,H-265,SITE)
    c.drawImage(QR,575,H-390,120,120,mask='auto');c.setFont('Helvetica-Bold',9);c.drawCentredString(635,H-405,'WHATSAPP · SCAN TO ENQUIRE')
    footer(c,page)

c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1);page=1
cover(c);c.showPage();page+=1
info_page(c,page);c.showPage();page+=1
features_page(c,page);c.showPage();page+=1
accessories_page(c,page);c.showPage();page+=1
groups=[]
for item in items:
    name=item['group'].split(' / ')[0]
    if name not in [g[0] for g in groups]:groups.append((name,[]))
    next(g[1] for g in groups if g[0]==name).append(item)
for name,group in groups:
    chunks=[group[i:i+15] for i in range(0,len(group),15)]
    for j,chunk in enumerate(chunks,1):
        product_page(c,page,name,chunk,f'PART {j}' if len(chunks)>1 else None);c.showPage();page+=1
project_page(c,page);c.showPage();c.save()
print(f'created {OUT} with {page} pages and {len(items)} products')
