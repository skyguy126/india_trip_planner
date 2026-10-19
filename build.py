"""Compile the portable page and Express/Helmet hosting artifacts.

Python standard library only; no network required.
"""
from pathlib import Path
import argparse,json,os,re,runpy,sys
ROOT=Path(__file__).resolve().parent

THEME_BOOTSTRAP='try{document.documentElement.dataset.theme=localStorage.getItem("india-trip-theme-v2")||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")}catch(e){document.documentElement.dataset.theme="light"}'
PORTABLE_SCRIPTS_RE=re.compile(
    r'<script type="application/json" id="build-config">__BUILD_CONFIG__</script>\s*'
    r'<script id="trip-data" type="application/json">__DATA__</script>\s*'
    r'<script>__ENGINE__</script>\s*'
    r'<script>const ENGINE_SOURCE=__ENGINE_STRING__;</script>\s*'
    r'<script>__PRESENTATION__</script>\s*'
    r'<script>__CARTOGRAPHY__</script>\s*'
    r'<script>__APP__</script>',
    re.M,
)
HOST_SCRIPTS=(
    '<script type="application/json" id="build-config" nonce="<%= nonce %>">'
    '<%- JSON.stringify({ mapboxToken }) %></script>\n'
    '<script src="/js/india_trip_planner.js" nonce="<%= nonce %>"></script>'
)

def load_token(config):
    default_config=ROOT/'config'/'mapbox.public.json'
    config=Path(config).resolve() if config else default_config
    settings={}
    if config.exists():settings=json.loads(config.read_text())
    elif config!=default_config:raise FileNotFoundError(f'Config not found: {config}')
    local=ROOT/'config'/'mapbox.local.json'
    if local.exists() and config==default_config:settings.update(json.loads(local.read_text()))
    token=os.environ.get('MAPBOX_TOKEN') or settings.get('mapboxToken','')
    if not isinstance(token,str) or not re.fullmatch(r'pk\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',token):
        raise ValueError('Set a valid public pk. Mapbox token via MAPBOX_TOKEN, config/mapbox.local.json, or config/mapbox.public.json (copy from config/mapbox.example.json).')
    return token,config,default_config

def assemble_data(output_parent):
    old=os.environ.get('TRIP_DATA_OUTPUT');os.environ['TRIP_DATA_OUTPUT']=str(output_parent/'data.json')
    sys.path.insert(0,str(ROOT))
    try:runpy.run_path(str(ROOT/'build_data.py'))
    finally:
        if old is None:os.environ.pop('TRIP_DATA_OUTPUT',None)
        else:os.environ['TRIP_DATA_OUTPUT']=old
    return (output_parent/'data.json').read_text()

def fill_shell(shell,pieces):
    html=shell
    for key,value in pieces.items():html=html.replace(key,value)
    if any(key in html for key in pieces):raise ValueError('An unresolved build placeholder remains.')
    return html

def build_hosting_bundle(data_text,engine,presentation,cartography,app):
    """Dual-purpose JS: TripEngine + worker handler, or full planner on the main thread."""
    # app.js opens with 'use strict'; — keep that as the first statement of the main-thread branch.
    app_body=re.sub(r"^'use strict';\s*",'',app.lstrip(),count=1)
    return '\n'.join([
        '/* India Trip Generator — engine + planner bundle (worker-safe). */',
        engine.rstrip(),
        "if(typeof WorkerGlobalScope!=='undefined'&&self instanceof WorkerGlobalScope){",
        'onmessage=e=>{try{postMessage({result:TripEngine.solve(e.data.data,e.data.ids,e.data.settings)})}catch(error){postMessage({error:error.message})}};',
        '}else{',
        "'use strict';",
        f'window.INDIA_TRIP_DATA={data_text};',
        presentation.rstrip(),
        cartography.rstrip(),
        app_body.rstrip(),
        '}',
        '',
    ])

def build_hosting_ejs(shell,theme_css):
    ejs=shell.replace('__THEME_CSS__',theme_css)
    ejs=ejs.replace(
        f'<script>{THEME_BOOTSTRAP}</script>',
        f'<script nonce="<%= nonce %>">{THEME_BOOTSTRAP}</script>',
        1,
    )
    ejs=ejs.replace('<style>', '<style nonce="<%= nonce %>">', 1)
    if not PORTABLE_SCRIPTS_RE.search(ejs):
        raise ValueError('Portable script block not found while building hosting EJS.')
    ejs=PORTABLE_SCRIPTS_RE.sub(HOST_SCRIPTS,ejs,count=1)
    # Hosting shell must not retain portable embed placeholders.
    leftovers=[k for k in ('__DATA__','__ENGINE__','__ENGINE_STRING__','__CARTOGRAPHY__','__PRESENTATION__','__APP__','__BUILD_CONFIG__','__THEME_CSS__') if k in ejs]
    if leftovers:raise ValueError(f'Unresolved hosting placeholders: {", ".join(leftovers)}')
    if re.search(r'\sstyle="',ejs):raise ValueError('Hosting EJS must not use static style="" attributes (CSP).')
    # Match tags even when EJS delimiters contain ">" (e.g. <%= nonce %>).
    for m in re.finditer(r'<(script|style)\b',ejs,re.I):
        tag=m.group(1).lower()
        # Scan forward to the real tag end: a ">" that is not inside <%= … %> / <%- … %>.
        i=m.end()
        while i<len(ejs):
            if ejs.startswith('<%',i):
                end=ejs.find('%>',i+2)
                if end<0:raise ValueError(f'Unclosed EJS in <{tag}> tag')
                i=end+2
                continue
            if ejs[i]=='>':
                attrs=ejs[m.end():i]
                break
            i+=1
        else:
            raise ValueError(f'Unclosed <{tag}> tag in hosting EJS')
        if 'nonce="<%= nonce %>"' not in attrs:
            raise ValueError(f'Hosting {tag} tag missing nonce="<%= nonce %>": <{tag}{attrs}>')
    if 'id="build-config"' not in ejs or '<%- JSON.stringify({ mapboxToken }) %>' not in ejs:
        raise ValueError('Hosting EJS must inject Mapbox token via build-config JSON script.')
    if 'src="/js/india_trip_planner.js"' not in ejs:
        raise ValueError('Hosting EJS must load /js/india_trip_planner.js once.')
    return ejs

def build(output=None,config=None):
    output=Path(output).resolve() if output else ROOT/'dist'/'India_Trip_Generator.html'
    token,_,_=load_token(config)
    output.parent.mkdir(parents=True,exist_ok=True)
    data_text=assemble_data(output.parent)
    data_for_html=data_text.replace('</','<\\/')
    engine=(ROOT/'engine.js').read_text()
    presentation=(ROOT/'presentation.js').read_text()
    cartography=(ROOT/'cartography.js').read_text()
    app=(ROOT/'app.js').read_text()
    theme=(ROOT/'theme.css').read_text()
    shell=(ROOT/'shell.html').read_text()

    # Portable single-file page (token embedded at build time).
    portable_pieces={
        '__DATA__':data_for_html,
        '__ENGINE__':engine,
        '__ENGINE_STRING__':json.dumps(engine).replace('</','<\\/'),
        '__CARTOGRAPHY__':cartography,
        '__PRESENTATION__':presentation,
        '__APP__':app,
        '__THEME_CSS__':theme,
        '__BUILD_CONFIG__':json.dumps({'mapboxToken':token}).replace('<','\\u003c'),
    }
    html=fill_shell(shell,portable_pieces)
    output.write_text(html)
    print(f'Compiled {output.name}: {output.stat().st_size:,} bytes → {output.parent}')

    # Express + Helmet hosting artifacts: EJS shell + dual-purpose JS bundle only.
    views_dir=output.parent/'views'
    public_js=output.parent/'public'/'js'
    views_dir.mkdir(parents=True,exist_ok=True)
    public_js.mkdir(parents=True,exist_ok=True)
    # Remove legacy monolithic hosting EJS if present.
    legacy=output.parent/'india_trip_planner.ejs'
    if legacy.exists():legacy.unlink()

    ejs=build_hosting_ejs(shell,theme)
    ejs_path=views_dir/'india_trip_planner.ejs'
    ejs_path.write_text(ejs)

    bundle=build_hosting_bundle(data_text,engine,presentation,cartography,app)
    js_path=public_js/'india_trip_planner.js'
    js_path.write_text(bundle)

    if token in ejs or token in bundle:
        raise ValueError('Mapbox token must not appear in hosting EJS or JS bundle.')

    host_files=sorted(p for p in (output.parent/'views').rglob('*') if p.is_file())
    host_files+=sorted(p for p in (output.parent/'public').rglob('*') if p.is_file())
    expected={ejs_path.resolve(),js_path.resolve()}
    actual={p.resolve() for p in host_files}
    if actual!=expected:
        raise ValueError(f'Hosting deploy tree must contain exactly the two artifacts; found: {sorted(str(p.relative_to(output.parent)) for p in actual)}')

    print(f'Compiled {ejs_path.relative_to(output.parent)}: {ejs_path.stat().st_size:,} bytes')
    print(f'Compiled {js_path.relative_to(output.parent)}: {js_path.stat().st_size:,} bytes')
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);parser.add_argument('--config',type=Path)
    args=parser.parse_args();build(args.output,args.config)
