"""Compile the portable page. Python standard library only; no network required."""
from pathlib import Path
import argparse,json,os,re,runpy,sys
ROOT=Path(__file__).resolve().parent

def build(output=None,config=None):
    output=Path(output).resolve() if output else ROOT/'dist'/'India_Trip_Generator.html'
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
    output.parent.mkdir(parents=True,exist_ok=True)
    old=os.environ.get('TRIP_DATA_OUTPUT');os.environ['TRIP_DATA_OUTPUT']=str(output.parent/'data.json')
    sys.path.insert(0,str(ROOT))
    try:runpy.run_path(str(ROOT/'build_data.py'))
    finally:
        if old is None:os.environ.pop('TRIP_DATA_OUTPUT',None)
        else:os.environ['TRIP_DATA_OUTPUT']=old
    engine=(ROOT/'engine.js').read_text()
    pieces={'__DATA__':(output.parent/'data.json').read_text().replace('</','<\\/'),'__ENGINE__':engine,'__ENGINE_STRING__':json.dumps(engine).replace('</','<\\/'),'__CARTOGRAPHY__':(ROOT/'cartography.js').read_text(),'__PRESENTATION__':(ROOT/'presentation.js').read_text(),'__APP__':(ROOT/'app.js').read_text(),'__THEME_CSS__':(ROOT/'theme.css').read_text(),'__BUILD_CONFIG__':json.dumps({'mapboxToken':token}).replace('<','\\u003c')}
    html=(ROOT/'shell.html').read_text()
    for key,value in pieces.items():html=html.replace(key,value)
    if any(key in html for key in pieces):raise ValueError('An unresolved build placeholder remains.')
    output.write_text(html)
    print(f'Compiled {output.name}: {output.stat().st_size:,} bytes → {output.parent}')
    return output
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);parser.add_argument('--config',type=Path)
    args=parser.parse_args();build(args.output,args.config)
