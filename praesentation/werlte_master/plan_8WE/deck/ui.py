from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.oxml.ns import qn
import copy
from lxml import etree
def C(h): return RGBColor.from_string(h)
INK,GREEN,GOLD,TERRA,GREY,LIGHT,LINE,POS,NEG,WHITE="3A3530","6E7B5E","C08A5B","B5654A","7A726A","EBE1D3","D8CCBC","5E7F4E","A8442F","FFFFFF"
CREAM="F6F1E9"; SAGE="DCE0CF"; BLUSH="EFD8CC"
HF,BF="Cambria","Calibri"
class Deck:
    def __init__(s):
        s.prs=Presentation(); s.prs.slide_width=Inches(13.333); s.prs.slide_height=Inches(7.5); s.n=0
    def blank(s,bg=CREAM):
        sl=s.prs.slides.add_slide(s.prs.slide_layouts[6]); s.n+=1
        f=sl.background.fill; f.solid(); f.fore_color.rgb=C(bg); return sl
def tx(sl,x,y,w,h,paras,size=14,color=INK,bold=False,font=BF,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4,line=1.05):
    tb=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(0); tf.margin_top=tf.margin_bottom=Inches(0); tf.vertical_anchor=anchor
    if isinstance(paras,str): paras=[paras]
    for i,p in enumerate(paras):
        o=dict(t=p) if isinstance(p,str) else dict(p)
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        para.alignment=o.get("align",align); para.space_after=Pt(o.get("space",space)); para.line_spacing=line
        runs=o["t"] if isinstance(o["t"],list) else [(o["t"],{})]
        for rt,ro in runs:
            r=para.add_run(); r.text=rt; f=r.font; f.name=ro.get("font",o.get("font",font)); f.size=Pt(ro.get("size",o.get("size",size)))
            f.bold=ro.get("bold",o.get("bold",bold)); f.color.rgb=C(ro.get("color",o.get("color",color)))
    return tb
def rect(sl,x,y,w,h,fill=LIGHT,line=None,shape=MSO_SHAPE.RECTANGLE):
    r=sl.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h)); r.shadow.inherit=False
    if fill: r.fill.solid(); r.fill.fore_color.rgb=C(fill)
    else: r.fill.background()
    if line: r.line.color.rgb=C(line); r.line.width=Pt(0.75)
    else: r.line.fill.background()
    return r
def page(d,section,title,source=None,bg=CREAM):
    sl=d.blank(bg)
    rect(sl,11.4,-1.5,3.2,3.2,SAGE,shape=MSO_SHAPE.OVAL); rect(sl,-0.9,6.1,2.0,2.0,BLUSH,shape=MSO_SHAPE.OVAL)
    tx(sl,0.7,0.42,9,0.3,section.upper(),size=11,color=GOLD,bold=True)
    tx(sl,0.7,0.72,10.8,1.1,title,size=28,color=INK,font=HF,line=0.95)
    ln=sl.shapes.add_connector(1,Inches(0.7),Inches(7.0),Inches(12.63),Inches(7.0)); ln.line.color.rgb=C(LINE); ln.line.width=Pt(0.5)
    tx(sl,0.7,7.1,8,0.25,"Neue Mitte Werlte · Baufeld 3 · Stand November 2026 · Entwurf, alle Werte Annahmen",size=9,color=GREY)
    tx(sl,11.6,7.1,1.03,0.25,str(d.n),size=9,color=GREY,align=PP_ALIGN.RIGHT)
    if source: tx(sl,0.7,6.68,11.9,0.25,source,size=9,color=GREY)
    return sl
def kpi(sl,x,y,w,value,label,color=GREEN,vs=34):
    rect(sl,x,y,0.05,1.05,color)
    tx(sl,x+0.2,y-0.02,w-0.2,0.6,value,size=vs,color=color,font=HF,bold=False)
    tx(sl,x+0.2,y+0.62,w-0.2,0.5,label,size=12,color=GREY)
def _border(cell,color=LINE,w=6350,sides=("b",)):
    tcPr=cell._tc.get_or_add_tcPr()
    for s in ("L","R","T","B"):
        tag=qn("a:ln"+s)
        for e in tcPr.findall(tag): tcPr.remove(e)
        ln=etree.SubElement(tcPr,tag)
        if s.lower() in sides:
            ln.set("w",str(w)); sf=etree.SubElement(ln,qn("a:solidFill")); c=etree.SubElement(sf,qn("a:srgbClr")); c.set("val",color)
        else: ln.set("w","0"); etree.SubElement(ln,qn("a:noFill"))
def table(sl,x,y,w,rows,widths,size=12,rh=0.36,align=None,hl=(),bold=(),neg=(),pos=(),head=True,total=()):
    nr,nc=len(rows),len(rows[0]); gf=sl.shapes.add_table(nr,nc,Inches(x),Inches(y),Inches(w),Inches(rh*nr)); t=gf.table
    tblPr=t._tbl.tblPr; tblPr.set("firstRow","0"); tblPr.set("bandRow","0")
    st=tblPr.find(qn("a:tableStyleId"))
    if st is not None: st.text="{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    sc=w/sum(widths)
    for i,wd in enumerate(widths): t.columns[i].width=Inches(wd*sc)
    align=align or ["l"]+["r"]*(nc-1)
    for r in range(nr):
        t.rows[r].height=Inches(rh)
        for c in range(nc):
            ce=t.cell(r,c); ce.margin_left=ce.margin_right=Inches(0.08); ce.margin_top=ce.margin_bottom=Inches(0.02); ce.vertical_anchor=MSO_ANCHOR.MIDDLE
            tf=ce.text_frame; tf.word_wrap=True; p=tf.paragraphs[0]; p.alignment={"l":PP_ALIGN.LEFT,"r":PP_ALIGN.RIGHT,"c":PP_ALIGN.CENTER}[align[c]]
            run=p.add_run(); run.text=str(rows[r][c]); f=run.font; f.name=BF; f.size=Pt(size)
            ishead=head and r==0
            f.bold=ishead or r in bold or r in total
            f.color.rgb=C(TERRA if ishead else (NEG if r in neg else (POS if r in pos else INK)))
            if ishead: ce.fill.background()
            elif r in hl or r in total: ce.fill.solid(); ce.fill.fore_color.rgb=C(LIGHT)
            else: ce.fill.background()
            _border(ce,INK if (ishead or r in total) else LINE,12700 if (ishead or r in total) else 6350,("b",) if not (r in total) else ("t","b"))
    return gf
def img(sl,path,x,y,w,h):
    from PIL import Image
    iw,ih=Image.open(path).size; pic=sl.shapes.add_picture(path,Inches(x),Inches(y)); 
    ar=w/h; iar=iw/ih
    if iar>ar: c=(1-ar/iar)/2; pic.crop_left=c; pic.crop_right=c
    else: c=(1-iar/ar)/2; pic.crop_top=c; pic.crop_bottom=c
    pic.left,pic.top,pic.width,pic.height=Inches(x),Inches(y),Inches(w),Inches(h); return pic
def dot(sl,x,y,color,d=0.16): 
    o=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(y),Inches(d),Inches(d)); o.fill.solid(); o.fill.fore_color.rgb=C(color); o.line.fill.background(); o.shadow.inherit=False
def style_chart(ch,size=11,legend=False):
    ch.font.size=Pt(size); ch.font.name=BF; ch.has_legend=legend; ch.has_title=False
    if legend: ch.legend.position=XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(size)
def hide_axis_lines(ax,grid=False):
    ax.format.line.fill.background(); ax.has_major_gridlines=grid
    if grid: ax.major_gridlines.format.line.color.rgb=C(LINE); ax.major_gridlines.format.line.width=Pt(0.5)
