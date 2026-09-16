from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree
import re,sys
src,dst=sys.argv[1:]
A='http://schemas.openxmlformats.org/drawingml/2006/main'
ns={'a':A}
count=0
with ZipFile(src) as z, ZipFile(dst,'w',ZIP_DEFLATED) as o:
 for name in z.namelist():
  raw=z.read(name)
  if re.fullmatch(r'ppt/slides/slide\d+\.xml',name):
   d=etree.fromstring(raw)
   for p in d.findall('.//a:p',ns):
    text=''.join(p.xpath('.//a:t/text()',namespaces=ns))
    if re.search('[\u0590-\u05ff]',text):
     pp=p.find('a:pPr',ns)
     if pp is None:
      pp=etree.Element('{'+A+'}pPr');p.insert(0,pp)
     pp.set('rtl','1')
     for r in p.findall('.//a:rPr',ns)+p.findall('.//a:defRPr',ns):r.set('lang','he-IL')
     count+=1
   raw=etree.tostring(d,xml_declaration=True,encoding='UTF-8',standalone=True)
  if name.startswith('ppt/theme/') and name.endswith('.xml'):
   d=etree.fromstring(raw)
   for kind in ('hlink','folHlink'):
    for c in d.findall('.//a:clrScheme/a:'+kind+'/*',ns):
     c.set('val','4EE5FF')
   raw=etree.tostring(d,xml_declaration=True,encoding='UTF-8',standalone=True)
  o.writestr(name,raw)
print('RTL paragraphs',count)
