"""Generate readable display pages; never rewrite raw catalogue/provenance/media."""
import argparse,json
from pathlib import Path
from presentation_public import generated
ROOT=Path(__file__).resolve().parent

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    data=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8-sig'))
    outputs=generated(data)
    for rel,text in outputs.items():
        target=ROOT/rel
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8')!=text:raise ValueError('Stale presentation '+rel)
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8',newline='\n')
    print('PASS: '+str(len(data['assets']))+' immutable parent records; '+str(len(outputs))+' readable presentation outputs; no processing')
if __name__=='__main__':run()
