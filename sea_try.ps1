param([string]$tag, [string]$json)
# sets water via sea_test.luau, takes the three sea views (photo mode on), prints sampled pixel colours (numbers only)
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$dir = "$town\shots\v4\sea_$tag"
Write-Output (& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\st.ps1" -file "$town\rebuild\v4\sea_test.luau" -data $json | Out-String).Trim()
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode on -csv "$town\shots\v4\views_sea.csv" -dir $dir | Out-Null
python "$town\rebuild\v4\_sea_sample.py" $dir
