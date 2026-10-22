#!/usr/bin/env python3
"""Create a portable HTML preview. Asset files are embedded; font files are not."""
from __future__ import annotations
import argparse
import base64
import mimetypes
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]/'docs'

def build_preview(*, offline_fonts: bool=False, include_pdfs: bool=True) -> str:
    soup=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
    def data_uri(path: Path) -> str:
        path=path.resolve()
        if ROOT not in path.parents or not path.is_file(): raise FileNotFoundError(path)
        mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
        return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
    images={path.relative_to(ROOT).as_posix():data_uri(path) for sub in ('images','videos') for path in (ROOT/'assets'/sub).rglob('*') if path.is_file() and path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.mp4'}}
    for link in soup.find_all('link',rel='stylesheet'):
        if urlsplit(link.get('href','')).path=='assets/css/styles.css':
            style=soup.new_tag('style');style.string=(ROOT/'assets/css/styles.css').read_text(encoding='utf-8');link.replace_with(style)
        elif offline_fonts: link.decompose()
    for el in soup.find_all(True):
        if el.get('href','').startswith('presentations.html?'):
            el['href']='https://sditr0414.github.io/'+el['href']
        for attr in ('src','data-image','data-video','data-src','poster','data-poster'):
            value=el.get(attr,'')
            if value.startswith(('assets/images/', 'assets/videos/')):
                asset=urlsplit(value).path
                if asset not in images:raise FileNotFoundError(asset)
                el[attr]=images[asset]
        if el.name=='img':el['loading']='eager'
        if el.name=='image' and el.get('href','').startswith('assets/images/'):  # photos inside inline SVG
            asset=urlsplit(el['href']).path
            if asset not in images:raise FileNotFoundError(asset)
            el['href']=images[asset]
        href=urlsplit(el.get('href','')).path
        if include_pdfs and href in ('assets/pdf/slides.pdf','assets/pdf/handout.pdf'):
            el['href']=data_uri(ROOT/href)
    app=(ROOT/'assets/js/app.js').read_text(encoding='utf-8')
    for name,uri in images.items():
        app=app.replace("'"+name+"'","'"+uri+"'").replace('"'+name+'"','"'+uri+'"')
    script=next(el for el in soup.find_all('script',src=True) if urlsplit(el['src']).path=='assets/js/app.js')
    replacement=soup.new_tag('script');replacement.string=app;script.replace_with(replacement)
    return str(soup)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    args.output.write_text(build_preview(),encoding='utf-8')
    print(args.output)
