<#
Replay the bounded FPK -> MTAR -> GANI stages using the caller's own game data.
Creates fresh output only. No live game installation or animation editing.
#>
param(
 [Parameter(Mandatory=$true)][string]$GzsTool,
 [Parameter(Mandatory=$true)][string]$MtarTool,
 [Parameter(Mandatory=$true)][string]$PlayerMtbsFpk,
 [Parameter(Mandatory=$true)][string]$PlayerResidentFpk,
 [Parameter(Mandatory=$true)][string]$SoldierCommonFpk,
 [Parameter(Mandatory=$true)][string]$Destination
)
$ErrorActionPreference='Stop'
$dest=[IO.Path]::GetFullPath($Destination)
if(Test-Path -LiteralPath $dest){throw 'Destination already exists. Use a fresh short private path.'}
$tools=@{}
foreach($pair in @(@('gzs',$GzsTool),@('mtar',$MtarTool))){
 $p=[IO.Path]::GetFullPath($pair[1])
 if(-not(Test-Path -LiteralPath $p -PathType Leaf)){throw "Missing tool: $p"}
 $tools[$pair[0]]=$p
}
$specs=@(
 @{Pack='player2_mtbs_motion';Input=$PlayerMtbsFpk;Name='player2_cqc';Folder='player2'},
 @{Pack='player2_resident_motion';Input=$PlayerResidentFpk;Name='player2_resident';Folder='player2'},
 @{Pack='Soldier2Common';Input=$SoldierCommonFpk;Name='Soldier_common';Folder='soldier2'}
)
foreach($s in $specs){if(-not(Test-Path -LiteralPath $s.Input -PathType Leaf)){throw "Missing FPK: $($s.Input)"}}
New-Item -ItemType Directory -Path $dest | Out-Null
function Get-Sha256([string]$Path){
 $stream=[IO.File]::OpenRead($Path)
 $algorithm=[Security.Cryptography.SHA256]::Create()
 try {return [BitConverter]::ToString($algorithm.ComputeHash($stream)).Replace('-','').ToLower()}
 finally {$stream.Dispose();$algorithm.Dispose()}
}
$receipts=@()
function Invoke-CommunityTool([string]$Exe,[string[]]$Arguments,[string]$Log){
 Push-Location -LiteralPath (Split-Path -LiteralPath $Exe)
 try {
  Write-Host ("Actual command: " + [IO.Path]::GetFileName($Exe) + " " + ($Arguments -join ' '))
  '' | & $Exe @Arguments 2>&1 | Tee-Object -FilePath $Log
  $toolExit=$LASTEXITCODE
  if($toolExit -ne 0){throw "Community tool exited $toolExit"}
 } finally {Pop-Location}
}
foreach($id in @('gzs','mtar')){
 $runtime=Join-Path $dest "runtime/$id"
 New-Item -ItemType Directory -Path $runtime -Force | Out-Null
 Copy-Item -LiteralPath (Split-Path -LiteralPath $tools[$id]) -Destination (Join-Path $dest "runtime/$id-source") -Recurse
 # Run the copied executable beside its original dictionaries and DLLs.
 $tools[$id]=Join-Path (Join-Path $dest "runtime/$id-source") ([IO.Path]::GetFileName($tools[$id]))
}
foreach($s in $specs){
 $inputPath=(Resolve-Path -LiteralPath $s.Input).Path
 $packPath=Join-Path $dest ($s.Pack+'.fpk')
 Copy-Item -LiteralPath $inputPath -Destination $packPath
 $sourceHash=(Get-Sha256 $inputPath)
 if((Get-Sha256 $packPath) -ne $sourceHash){throw 'Copy hash mismatch'}
 Invoke-CommunityTool $tools.gzs @($packPath) (Join-Path $dest ($s.Pack+'.gzstool.log'))
 $mtarSource=Join-Path $dest ($s.Pack+'_fpk/Assets/tpp/motion/mtar/'+$s.Folder+'/'+$s.Name+'.mtar')
 $motionDir=Join-Path $dest ('mtars/'+$s.Name)
 New-Item -ItemType Directory -Path $motionDir -Force | Out-Null
 $mtar=Join-Path $motionDir ($s.Name+'.mtar')
 Copy-Item -LiteralPath $mtarSource -Destination $mtar
 if(-not(Test-Path -LiteralPath $mtar)){throw "Expected MTAR not produced: $mtar"}
 Invoke-CommunityTool $tools.mtar @($mtar,'-n') (Join-Path $dest ($s.Name+'.mtartool.log'))
 if(-not(Test-Path -LiteralPath ($mtar+'.xml'))){throw 'MtarTool extraction failed'}
 $receipts+=@{SourceFpk=[IO.Path]::GetFileName($inputPath);SourceFpkSha256=$sourceHash;Mtar=$s.Name;MtarSha256=(Get-Sha256 $mtar)}
 if((Get-Sha256 $inputPath) -ne $sourceHash){throw 'Source input changed'}
}
$inventory=Get-ChildItem -LiteralPath $dest -Recurse -File | Where-Object {$_.FullName -notlike '*\runtime\*'} | ForEach-Object {
 @{Path=$_.FullName.Substring($dest.Length+1).Replace('\','/');Bytes=$_.Length;Sha256=(Get-Sha256 $_.FullName)}
}
$runtimeHashes=Get-ChildItem -LiteralPath (Join-Path $dest 'runtime') -Recurse -File | ForEach-Object {
 @{Path=$_.FullName.Substring($dest.Length+1).Replace('\','/');Sha256=(Get-Sha256 $_.FullName)}
}
@{SourceReceipts=$receipts;RuntimeHashes=$runtimeHashes;Inventory=$inventory;NativePlaybackProved=$false;FreshDatExtraction=$false} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $dest 'extraction-receipt.json') -Encoding UTF8
Write-Host 'Complete. Keep the MTAR, XML, GANI and all companion/layout files together.'

