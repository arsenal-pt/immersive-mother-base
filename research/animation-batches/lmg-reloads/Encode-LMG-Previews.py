"""Encode genuine clean animation renders into titled catalogue GIFs; no motion is generated."""
import argparse,hashlib,json,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def media_info(path,root):return {'path':path.relative_to(root).as_posix(),'bytes':path.stat().st_size,'sha256':sha(path)}
def title_for(row):
 name=row['shortIdentifier'];role=row['role'];family=row['sequenceFamily'];phase=row['phase'];kind=row['phaseKind']
 if role=='lmg_ready_reload_candidate':return 'LMG reload candidate - '+('kneeling' if '_q_' in name else 'standing'),'NPC ready/reload family | held LMG absent'
 if role=='npc_combo_receiver_candidate':return 'NPC combo receiver - '+family+' phase '+str(phase),'NPC hit receiver candidate'
 if role=='snake_combo_initiator_candidate':
  if name.endswith('_f1_st'):return 'Snake CQC combo - front phase 1 start','Snake transition candidate'
  if name.endswith('_f1_ed'):return 'Snake CQC combo - front phase 1 end','Snake transition candidate'
  if family in ['front','back']:return 'Snake CQC combo - '+family+' phase '+str(phase),'Snake attacker candidate'
  return 'Snake CQC - left start/miss transition','Snake transition candidate'
 actor='player' if row['sourceRole']=='player' else 'enemy'
 part='ending' if name.endswith('_ed') else 'phase 2' if name.endswith('pnh2') else 'phase 1'
 return 'Special/zombie punch - '+actor+' '+part,'Special/zombie actor; ordinary soldier attack unproved'

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for argument in ['renders','media-output','clean-gif-output','contact-output','font','tool-dir']:p.add_argument('--'+argument,type=Path,required=True)
 p.add_argument('--expected-count',type=int,required=True)
 a=p.parse_args();batch=json.loads((a.renders/'batch-receipt.json').read_text());assert 1<=len(batch['clips'])==a.expected_count<=25,'Expected explicitly bounded source clip count'
 for path in [a.media_output,a.clean_gif_output,a.contact_output]:assert not path.exists(),'Use fresh output directories';path.mkdir(parents=True)
 font=lambda size:ImageFont.truetype(str(a.font),size)
 entries=[];contact_thumbs=[]
 for selected in batch['clips']:
  source=a.renders/selected['id'];receipt_path=source/'render-receipt.json';assert sha(receipt_path)==selected['renderReceiptSha256'];row=json.loads(receipt_path.read_text());title,role=title_for(row)
  for item in row['cleanPngs']:assert sha(source/item['path'])==item['sha256'],'Clean render changed'
  frames=row['sourceFramesSampled'];count=row['rawFrameCount'];fps=row['chosenSourceFramesPerSecond'];step=row['sampleStep'];images=[Image.open(source/('frame-'+str(f).zfill(4)+'.png')).convert('RGB') for f in frames]
  durations=[(round(min(count,f+step)/fps*100)-round(f/fps*100))*10 for f in frames];assert all(d>0 for d in durations)
  width,height=images[0].size;captions=[]
  for im in images:
   out=Image.new('RGB',(width,height+134),'#111a27');out.paste(im,(0,0));draw=ImageDraw.Draw(out)
   for y,text,size,color in [(height+6,title,20,'#ffffff'),(height+35,row['shortIdentifier'],18,'#d7e7ff'),(height+64,role,13,'#d1d8e3'),(height+86,'Stock Ocelot reference model | untextured offline retarget',14,'#d1d8e3'),(height+110,str(fps)+' source frames/s chosen; '+str(round(fps/step))+' fps GIF; native rate unverified',13,'#b6c1d0')]:
    assert draw.textbbox((0,0),text,font=font(size))[2]<=width-32,'Caption does not fit: '+text
    draw.text((16,y),text,font=font(size),fill=color)
   captions.append(out)
  clean=a.clean_gif_output/(row['id']+'-clean.gif');titled=a.media_output/(row['id']+'.gif');thumbnail=a.media_output/(row['id']+'.png')
  for output,ims in [(clean,images),(titled,captions)]:
   quantized=[im.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE) for im in ims]
   quantized[0].save(output,save_all=True,append_images=quantized[1:],duration=durations,loop=0,optimize=True,disposal=1)
   with Image.open(output) as pixels:
    assert pixels.n_frames==len(quantized),'Unexpected frame merging'
    for index,expected in enumerate(quantized):
     pixels.seek(index);assert pixels.convert('RGB').tobytes()==expected.convert('RGB').tobytes(),'Delta encoding changed composited frame pixels'

  captions[len(captions)//3].save(thumbnail)
  with Image.open(titled) as check:
   assert check.n_frames==len(frames) and check.size==(width,height+134)
   actual=[]
   for index in range(check.n_frames):check.seek(index);check.load();actual.append(check.info.get('duration'))
   assert actual==durations,'Encoded GIF timing differs'
  contact=Image.new('RGB',(width*3,height+134),'#111a27')
  for i,index in enumerate([0,len(captions)//3,2*len(captions)//3]):contact.paste(captions[index],(i*width,0))
  contact.save(a.contact_output/(row['id']+'-contact.png'));contact_thumbs.append(captions[len(captions)//3].resize((320,round((height+134)*320/width))))
  entries.append({'id':row['id'],'title':title,'shortIdentifier':row['shortIdentifier'],'sourceName':row['name'],'sourceArchive':row['sourceArchive'],'sourceArchiveSha256':row['sourceArchiveSha256'],'hashId':row['hashId'],'sourceGaniSha256':row['originalGaniSha256'],'sourceRole':row['sourceRole'],'role':row['role'],'sequenceFamily':row['sequenceFamily'],'phase':row['phase'],'phaseKind':row['phaseKind'],'rawFrameCount':count,'decodedTrackCount':row['decodedTrackCount'],'headerIndex':row['headerIndex'],'sourceFramesSampled':frames,'endpointFrameSavedPrivately':count,'chosenSourceFramesPerSecond':fps,'gifFrameDurationsMilliseconds':durations,'gifDurationMilliseconds':sum(durations),'nativeFrameRate':None,'rawLayoutFrameRateField':row['rawLayoutFrameRateField'],'rawLayoutRateMeaning':'Unverified enum/value; not assumed to be frames per second','referenceCharacter':'Stock Ocelot oce0_main0_def','visualStatus':'actual decoded motion rendered on offline stock reference character','nativeGameplayProof':False,'pairedAlignmentProof':False,'ordinarySoldierAttackProof':False,'cameraFixedForFullClip':True,'camera':row['camera'],'worldBounds':row['worldBounds'],'titledGif':media_info(titled,a.media_output),'thumbnail':media_info(thumbnail,a.media_output),'privateCleanGifSha256':sha(clean),'privateRenderReceiptSha256':sha(receipt_path),'cleanPngFrameCount':len(row['cleanPngs']),'maximumPerVertexWeightSumError':max(x['maxPerVertexWeightSumError'] for x in row['weightAudit'])})
  print('ENCODED '+row['id'],flush=True)
 reference=json.loads((a.renders/batch['clips'][0]['id']/'render-receipt.json').read_text())
 manifest={'schemaVersion':1,'date':'2026-10-15','scope':'Selected LMG ready/reload offline decoded MTAR previews; titled GIFs/thumbnails only, no game animation or model payloads','tooling':{'blender':batch['blender'],'mctrollinReferenceRevision':batch['communityRevision'],'referenceRevisionStatus':'Cited source pin from catalog; actual installed Python file hashes recorded separately, not an assertion for arbitrary caller tool directories','installedCommunityPythonFiles':[{'path':p.relative_to(a.tool_dir).as_posix(),'sha256':sha(p)} for p in sorted(a.tool_dir.rglob('*.py'))],'referenceRigSha256':batch['referenceRigSha256'],'trackMapSha256':batch['trackMapSha256'],'boneMapSha256':batch['boneMapSha256'],'rendererScriptSha256':batch['scriptSha256'],'encoderScriptSha256':sha(Path(__file__)),'FmdlStudioSourceRevision':'d580b94215cc007df6c38bdb0bfce6a0f30e4701','FmdlStudioPortableDllSha256':'ec5ded0406f28c2d7bbdf7d7d138ec7d5c5c2068f60751a730ba0fb1685472c9','GzsToolVersion':'0.5.3','GzsToolExecutableSha256':'1a9c5b11e2355383ff485aee7e86abc026f5c1fad729daf8c0fd15ee0aae1c10','characterFmdlVirtualPath':'/Assets/tpp/chara/oce/Scenes/oce0_main0_def.fmdl','characterFmdlSha256':'54b95f689a5d4e9e0299e9a6ab128eff8d89e23feab3e86104179a7be08ed854','characterSourceFpkSha256':'bd493cbfb2edfa534a932b5001ebd87d7eaf6458bd22510245daa403c4c9d893'},'skinning':{'method':'Original stock mesh geometry and weight values; native groups mapped to author DEF names, duplicate target groups merged preserving per-vertex sums; standard Blender Armature modifier','duplicateNativeMappingChoices':{n:v for n,v in reference['boneMapChoices'].items() if len(v)>1},'duplicateChoice':'First/proximal split segment in author supplied map','secondaryBonesFollowMappedNativeAncestor':reference['secondaryBoneAncestorFallbacks'],'fallbackCount':len(reference['secondaryBoneAncestorFallbacks']),'secondaryMotion':'Hair/scarf/holster bones inherit mapped ancestor motion; no native secondary simulation'},'gifEncoding':{'palette':'256 colors per frame; MEDIANCUT; no dithering','deltaEncoding':True,'disposal':1,'verification':'Every decoded composited GIF frame equals its quantized clean/captioned source frame exactly'},'timing':{'chosenSourceFramesPerSecond':30,'sampling':'Every second source frame in 0..N-1; clean endpoint N saved separately','nativeFrameRate':None,'gifQuantization':'Durations rounded cumulatively to 10ms GIF units, preserving chosen total duration to nearest10ms'},'limits':['Reference Ocelot appearance does not identify the original source actor','No native Fox twist/cloth/physics/contact/gameplay proof','Receiver clips are not ordinary NPC attacker combos','LMG ready/reload and posture labels remain source-name interpretations without native weapon/contact proof','Each body clip is shown without its held LMG; reference appearance is stock Ocelot'],'entries':entries}
 (a.media_output/'preview-manifest.json').write_text(json.dumps(manifest,indent=2))
 sheet=Image.new('RGB',(1600,((len(contact_thumbs)+4)//5)*contact_thumbs[0].height),'#111a27')
 for i,im in enumerate(contact_thumbs):sheet.paste(im,((i%5)*320,(i//5)*im.height))
 sheet.save(a.contact_output/'Selected-LMG-Contact.png')
 private={'titledGifCount':len(entries),'thumbnailCount':len(entries),'cleanGifCount':len(entries),'cleanPngCount':sum(e['cleanPngFrameCount'] for e in entries),'mediaBytes':sum(e['titledGif']['bytes']+e['thumbnail']['bytes'] for e in entries),'manifestSha256':sha(a.media_output/'preview-manifest.json'),'renderBatchReceiptSha256':sha(a.renders/'batch-receipt.json')}
 (a.contact_output/'encoding-receipt.json').write_text(json.dumps(private,indent=2));print(json.dumps(private),flush=True)
if __name__=='__main__':main()
