"""Encode approved reference frames; private config and raw sources are not published."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image

def run():
 ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True);ap.add_argument('--media-output',type=Path,required=True);a=ap.parse_args()
 cfg=json.loads(a.config.read_text(encoding='utf-8-sig'));a.media_output.mkdir(parents=True,exist_ok=True);results=[]
 for entry in cfg['assets']:
  folder=Path(cfg['outputRoot'])/entry['id'];files=sorted((folder/'clean-frames').glob('*.png'))
  if len(files)!=48:raise ValueError('Expected exactly48 approved camera frames')
  frames=[Image.open(p).convert('RGB') for p in files]
  if any(im.size!=(480,480) for im in frames):raise ValueError('Unexpected frame dimensions')
  # One palette from all angles avoids frame-by-frame palette flicker.
  montage=Image.new('RGB',(120*8,120*6),'white')
  for i,im in enumerate(frames):montage.paste(im.resize((120,120),Image.Resampling.LANCZOS),((i%8)*120,(i//8)*120))
  palette=montage.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  quantized=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
  target=a.media_output/(entry['id']+'-360.gif')
  quantized[0].save(target,save_all=True,append_images=quantized[1:],duration=100,loop=0,disposal=2,optimize=False)
  still=a.media_output/(entry['id']+'.png');shutil.copyfile(folder/'clean-still.png',still)
  thumb=Image.open(still);thumb.thumbnail((160,160),Image.Resampling.LANCZOS)
  thumb.save(a.media_output/(entry['id']+'-thumb.png'))
  with Image.open(target) as check:
   if check.n_frames!=48 or check.info.get('loop')!=0:raise ValueError('GIF frame/loop mismatch')
   for i,q in enumerate(quantized):
    check.seek(i)
    if check.info.get('duration')!=100 or check.convert('RGB').tobytes()!=q.convert('RGB').tobytes():raise ValueError('Decoded GIF differs from selected quantized frame')
  results.append({'id':entry['id'],'frameCount':48,'frameDelayMs':100,'durationMs':4800,'loop':0,'palette':'global256colors from all48angles; no dithering',
   'media':[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in [still,target,a.media_output/(entry['id']+'-thumb.png')]]})
 print(json.dumps(results,indent=2))
if __name__=='__main__':run()
