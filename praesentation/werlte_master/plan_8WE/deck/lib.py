import copy
from pptx.util import Emu
def eur(v,d=0,sign=False):
    s=f"{abs(v):,.{d}f}".replace(",","X").replace(".",",").replace("X",".")
    pre="−" if v<0 else ("+" if sign else "")
    return f"{pre}{s} €"
def num(v,d=0):
    return f"{v:,.{d}f}".replace(",","X").replace(".",",").replace("X",".")
def pct(v,d=1): return f"{v*100:.{d}f} %".replace(".",",")
def f2(v): return f"{v:.2f}".replace(".",",")
def setp(p,text):
    runs=p.runs
    if runs:
        runs[0].text=text
        for r in runs[1:]: r._r.getparent().remove(r._r)
    else: p.add_run().text=text
def T(shape,*texts):
    """Absätze setzen; Formatierung des jeweiligen Absatzes bleibt erhalten."""
    if len(texts)==1 and isinstance(texts[0],(list,tuple)): texts=texts[0]
    texts=[x for t in texts for x in (t.split("\n") if isinstance(t,str) else [t])] if False else list(texts)
    tf=shape.text_frame; ps=list(tf.paragraphs)
    while len(ps)<len(texts):
        new=copy.deepcopy(ps[-1]._p); ps[-1]._p.addnext(new); ps=list(tf.paragraphs)
    while len(ps)>len(texts):
        ps[-1]._p.getparent().remove(ps[-1]._p); ps=list(tf.paragraphs)
    for p,t in zip(ps,texts): setp(p,t)
def cell(c,text,ref=None):
    p=c.text_frame.paragraphs[0]
    if not p.runs and ref is not None:
        r=p.add_run(); r.text=text
        rp=ref._r.find("{http://schemas.openxmlformats.org/drawingml/2006/main}rPr")
        if rp is not None:
            old=r._r.find("{http://schemas.openxmlformats.org/drawingml/2006/main}rPr")
            if old is not None: r._r.remove(old)
            r._r.insert(0,copy.deepcopy(rp))
        for extra in c.text_frame.paragraphs[1:]: extra._p.getparent().remove(extra._p)
        return
    setp(p,text)
    for extra in c.text_frame.paragraphs[1:]: extra._p.getparent().remove(extra._p)
def table_set(shape,rows,remove=(),ncols=None,widths=None):
    tbl=shape.table._tbl
    if ncols:
        grid=tbl.tblGrid; gcs=list(grid)
        for g in gcs[1:]: grid.remove(g)
        for _ in range(ncols-1): grid.append(copy.deepcopy(gcs[0]))
        for k,g in enumerate(grid): g.set("w",str(int(widths[k]*914400)))
        for tr in tbl.tr_lst:
            tcs=list(tr.tc_lst); first=copy.deepcopy(tcs[0]); other=copy.deepcopy(tcs[1] if len(tcs)>1 else tcs[0])
            for tc in tcs: tr.remove(tc)
            tr.append(copy.deepcopy(first))
            for _ in range(ncols-1): tr.append(copy.deepcopy(other))
    for i in sorted(remove,reverse=True): tbl.remove(tbl.tr_lst[i])
    while len(tbl.tr_lst)<len(rows):
        n=len(tbl.tr_lst); src=tbl.tr_lst[n-2 if n>2 else n-1]; tbl.tr_lst[n-2 if n>2 else n-1].addnext(copy.deepcopy(src))
    while len(tbl.tr_lst)>len(rows):
        tbl.remove(tbl.tr_lst[len(tbl.tr_lst)-2])
    t=shape.table
    for r,row in zip(t.rows,rows):
        assert len(r.cells)==len(row),(len(r.cells),row)
        ref=None
        for c in r.cells:
            if c.text_frame.paragraphs[0].runs: ref=c.text_frame.paragraphs[0].runs[-1]; break
        for c,v in zip(r.cells,row): cell(c,v,ref)
def dup(prs,src):
    new=prs.slides.add_slide(src.slide_layout)
    for shp in list(new.shapes): shp._element.getparent().remove(shp._element)
    for el in list(src.shapes._spTree)[2:]:
        assert not any(k in el.tag for k in ("}pic",)), "pic"
        new.shapes._spTree.append(copy.deepcopy(el))
    return new
def reorder(prs,order):
    lst=prs.slides._sldIdLst
    ids={sl.part:el for sl,el in zip(prs.slides,list(lst))}
    for el in list(lst): lst.remove(el)
    for sl in order: lst.append(ids[sl.part])
def delshape(sh): sh._element.getparent().remove(sh._element)
