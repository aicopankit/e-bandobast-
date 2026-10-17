$proc = Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--headless=new', '--enable-logging=stderr', '--v=1', '--dump-dom', 'http://localhost:8000/index.html' -NoNewWindow -PassThru -RedirectStandardOutput 'scratch/chrome_out.txt' -RedirectStandardError 'scratch/chrome_err.txt'
Start-Sleep -Seconds 5
if (-not $proc.HasExited) {
    $proc.Kill()
}
Get-Content 'scratch/chrome_err.txt' -Head 40
