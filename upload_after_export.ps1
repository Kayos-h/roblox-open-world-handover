$flag = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\EXPORT_V2_DONE.txt'
Write-Host 'Waiting for Kiro to finish re-exporting the models...'
Write-Host 'Leave this window open. Uploading starts automatically.'
while (-not (Test-Path $flag)) { Start-Sleep -Seconds 30; Write-Host ('  still waiting ' + (Get-Date -Format 'HH:mm')) }
Write-Host 'Export finished. Starting upload.' -ForegroundColor Green
for ($pass = 1; $pass -le 3; $pass++) {
  Write-Host "Upload pass $pass" -ForegroundColor Cyan
  & 'C:\Users\Nitro\.kiro\crew\workspace\town\upload_all.ps1'
}
'done' | Out-File 'C:\Users\Nitro\.kiro\crew\workspace\town\UPLOAD_DONE.txt' -Encoding utf8
Write-Host 'All uploads finished.' -ForegroundColor Green
