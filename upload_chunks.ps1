# upload skull mesh chunks into ServerStorage.SkullMeshData (StringValues) one batch per chunk
$dir = Join-Path $PSScriptRoot 'skullchunks'
$files = Get-ChildItem $dir -Filter 'c*.txt' | Sort-Object Name
$i = 0
foreach ($f in $files) {
  $data = Get-Content -Raw $f.FullName
  $lua = "local SS = game:GetService('ServerStorage')`n" +
         "local fo = SS:FindFirstChild('SkullMeshData')`n" +
         "if not fo then fo = Instance.new('Folder'); fo.Name = 'SkullMeshData'; fo.Parent = SS end`n" +
         "if " + $i + " == 0 then fo:ClearAllChildren() end`n" +
         "local v = Instance.new('StringValue'); v.Name = string.format('c%02d', " + $i + ")`n" +
         "v.Value = [==[" + $data + "]==]`n" +
         "v.Parent = fo`nreturn 'chunk " + $i + " len=' .. #v.Value"
  $tmp = Join-Path $PSScriptRoot '_chunk_run.lua'
  Set-Content -Path $tmp -Value $lua -NoNewline
  & (Join-Path $PSScriptRoot 'run_batch.ps1') -batch $tmp -nolib
  $i++
}
