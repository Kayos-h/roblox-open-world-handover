$tpl = [IO.File]::ReadAllText('C:\Users\Nitro\.kiro\crew\workspace\town\job_export_folder.py')
$folders = 'roads','lighting','nature','props','capital','castle','rusty','alpine','elf','harbour','between','town1'
if ($args.Count -gt 0) { $folders = $args }
foreach ($f in $folders) {
  $job = 'C:\Users\Nitro\.kiro\crew\workspace\town\_job_' + $f + '.py'
  [IO.File]::WriteAllText($job, $tpl.Replace('__FOLDER__', $f))
  $t0 = Get-Date
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\blender_exec.ps1' -py $job -timeoutSec 1500
  "$r  ($([int]((Get-Date) - $t0).TotalSeconds)s)"
}
