#!/usr/bin/env python3
"""Static QA: internal links + anchors, asset refs, duplicate metadata, JSON-LD, sitemap, a11y basics."""
import os, re, json, glob, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pages = sorted(glob.glob(os.path.join(ROOT, '*.html')))
errors, warns = [], []
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.assets=[]; s.ids=set(); s.title=''; s._t=False; s.meta={}; s.h1=0; s.imgs=[]; s.ld=[]; s._ld=False; s.canon=None; s.lang=None; s.hs=[]; s.labels=set(); s.inputs=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t=='html': s.lang=a.get('lang')
        if t=='a' and 'href' in a: s.links.append((a['href'],a))
        if t in('img','script','source','video') and ('src' in a): s.assets.append(a['src'])
        if t=='img' and 'srcset' in a: s.assets += [x.strip().split()[0] for x in a['srcset'].split(',')]
        if t=='video' and a.get('poster'): s.assets.append(a['poster'])
        if t=='link' and 'href' in a:
            s.assets.append(a['href']) if a.get('rel') not in ('canonical',) else None
            if a.get('rel')=='canonical': s.canon=a['href']
        if t=='use' and 'href' in a: s.assets.append(a['href'].split('#')[0])
        if t=='meta': s.meta[a.get('name') or a.get('property')]=a.get('content')
        if t=='img': s.imgs.append(a)
        if t=='title': s._t=True
        if t=='h1': s.h1+=1
        if t in('h1','h2','h3','h4'): s.hs.append(int(t[1]))
        if t=='script' and a.get('type')=='application/ld+json': s._ld=True; s.ld.append('')
        if t=='label' and 'for' in a: s.labels.add(a['for'])
        if t in('input','select','textarea'): s.inputs.append(a)
    def handle_endtag(s,t):
        if t=='title': s._t=False
        if t=='script': s._ld=False
    def handle_data(s,d):
        if s._t: s.title+=d
        if s._ld: s.ld[-1]+=d
info={}
for f in pages:
    p=P(); p.feed(open(f,encoding='utf-8').read()); info[os.path.basename(f)]=p
names=set(info)
for n,p in info.items():
    if p.lang!='en-ZA': errors.append(f'{n}: lang={p.lang}')
    if p.h1!=1: errors.append(f'{n}: {p.h1} h1 elements')
    prev=0
    for h in p.hs:
        if prev and h>prev+1: errors.append(f'{n}: heading jump h{prev}->h{h}')
        prev=h
    for a in p.imgs:
        if 'alt' not in a: errors.append(f'{n}: img missing alt {a.get("src")}')
        if 'width' not in a or 'height' not in a: errors.append(f'{n}: img missing dimensions {a.get("src")}')
    for i in p.inputs:
        if i.get('type') in('submit','hidden'): continue
        if i.get('id') not in p.labels: errors.append(f'{n}: input {i.get("id")} has no label')
    for raw,a in p.links:
        if raw.startswith(('mailto:','tel:')): 
            if raw in('mailto:','tel:'): errors.append(f'{n}: empty {raw}')
            continue
        u=urlparse(raw)
        if u.scheme in('http','https'):
            if a.get('target')=='_blank' and 'noopener' not in a.get('rel',''): errors.append(f'{n}: _blank without noopener {raw}')
            continue
        if raw in('#','') or raw.startswith('javascript'): errors.append(f'{n}: placeholder link {raw!r}'); continue
        path=u.path or n
        if path in('./','/'): path='index.html'
        if not path.endswith('.html'):
            if not os.path.exists(os.path.join(ROOT,unquote(path))): errors.append(f'{n}: broken file link {raw}')
            continue
        if path not in names: errors.append(f'{n}: broken link {raw}'); continue
        if u.fragment and u.fragment not in info[path].ids: errors.append(f'{n}: missing anchor {raw}')
    for a in p.assets:
        if a.startswith(('http','data:','/')) : 
            if a.startswith('/') and not os.path.exists(os.path.join(ROOT,a.lstrip('/'))): errors.append(f'{n}: missing root asset {a}')
            continue
        if not os.path.exists(os.path.join(ROOT,unquote(a))): errors.append(f'{n}: missing asset {a}')
    if n!='404.html' and p.canon!=('https://glsrefrigeration.co.za/' if n=='index.html' else f'https://glsrefrigeration.co.za/{n}'): errors.append(f'{n}: canonical {p.canon}')
    for k in('description','og:title','og:description','og:url','og:image','twitter:card','twitter:image'):
        if not p.meta.get(k): errors.append(f'{n}: missing meta {k}')
    if len(p.meta.get('description',''))>160: warns.append(f'{n}: description {len(p.meta["description"])} chars')
    if not p.ld: errors.append(f'{n}: no JSON-LD')
    for blob in p.ld:
        try:
            j=json.loads(blob); ids=[x.get('@id') for x in j['@graph']]
            if len(ids)!=len(set(ids)): errors.append(f'{n}: duplicate @id')
            refs=set(re.findall(r'"@id":\s*"([^"]+)"',blob))
            for r in refs:
                if r not in ids and 'cor3hausproduction' not in r: errors.append(f'{n}: dangling @id {r}')
            for node in j['@graph']:
                if node['@type']=='HVACBusiness':
                    if node['telephone']!='+27736541480' or node['address']['streetAddress']!='2 Churchill Avenue, Primrose': errors.append(f'{n}: business facts wrong')
                    if 'geo' in node or 'aggregateRating' in node or 'openingHoursSpecification' in node or 'priceRange' in node: errors.append(f'{n}: unverified attribute present')
        except Exception as e: errors.append(f'{n}: JSON-LD invalid {e}')
    txt=open(os.path.join(ROOT,n),encoding='utf-8').read()
    if n!='404.html' and 'Website designed and developed by <a href="https://cor3hausproduction.com/" target="_blank" rel="noopener noreferrer">COR3 Haus Production</a>' not in txt: errors.append(f'{n}: COR3 attribution missing')
    for bad in ('073 654 1480','071 934 2182'): pass
    for old in ('0619342182','061 934 2182','082 920 8903','0829208903','Bertrams','Bezuidenhout','Judith','www.glsrefrigeration','JAY K','jay_k','j24y'):
        if old in txt: errors.append(f'{n}: stale value {old!r}')
for k in('title',):
    seen={}
    for n,p in info.items(): seen.setdefault(p.title.strip(),[]).append(n)
    for t,ns in seen.items():
        if len(ns)>1: errors.append(f'duplicate title {ns}')
seen={}
for n,p in info.items(): seen.setdefault(p.meta.get('description'),[]).append(n)
for d,ns in seen.items():
    if len(ns)>1: errors.append(f'duplicate description {ns}')
sm=open(os.path.join(ROOT,'sitemap.xml')).read()
for loc in re.findall(r'<loc>([^<]+)</loc>',sm):
    f=urlparse(loc).path.strip('/') or 'index.html'
    if f not in names: errors.append(f'sitemap entry without page: {loc}')
    if not loc.startswith('https://glsrefrigeration.co.za'): errors.append(f'sitemap host {loc}')
for n in names-{'404.html'}:
    loc='https://glsrefrigeration.co.za/'+('' if n=='index.html' else n)
    if loc not in sm: errors.append(f'page missing from sitemap: {n}')
# unused assets
used=set()
for f in pages+[os.path.join(ROOT,'assets/css/main.css'),os.path.join(ROOT,'assets/js/main.js'),os.path.join(ROOT,'site.webmanifest')]:
    t=open(f,encoding='utf-8').read(); used.update(re.findall(r'assets/[\w./-]+|[\w-]+\.(?:png|ico|webp|jpg|woff2|svg)',t))
allassets=[os.path.relpath(x,ROOT) for x in glob.glob(os.path.join(ROOT,'assets/**/*.*'),recursive=True)]
unused=[a for a in allassets if os.path.basename(a) not in {os.path.basename(u) for u in used} and 'LICENSE' not in a]
print('pages:',len(pages),'| errors:',len(errors),'| warnings:',len(warns))
for e in errors: print('ERROR',e)
for w in warns: print('WARN',w)
print('unreferenced assets:',unused or 'none')
sys.exit(1 if errors else 0)
