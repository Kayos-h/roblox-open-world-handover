param([string]$text = '0.3')
# types into the control that currently has keyboard focus in the foreground window (Studio property cell): select all, text, Enter
Add-Type -AssemblyName System.Windows.Forms
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 150
[System.Windows.Forms.SendKeys]::SendWait($text)
Start-Sleep -Milliseconds 150
[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
Start-Sleep -Milliseconds 400
'typed ' + $text
