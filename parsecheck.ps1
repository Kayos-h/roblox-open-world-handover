$errs = $null
[System.Management.Automation.Language.Parser]::ParseFile('C:\Users\Nitro\.kiro\crew\workspace\town\upload_all.ps1', [ref]$null, [ref]$errs) | Out-Null
if ($errs.Count) { $errs | ForEach-Object { "$($_.Extent.StartLineNumber): $($_.Message)" } } else { 'parse OK' }
