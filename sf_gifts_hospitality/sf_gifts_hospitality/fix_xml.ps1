$c = Get-Content 'D:\AI Addons\18\sf_gifts_hospitality\views\report_gift_register.xml' -Raw
$c = $c -replace '&', '&'
Set-Content 'D:\AI Addons\18\sf_gifts_hospitality\views\report_gift_register.xml' -Value $c -Encoding UTF8
Write-Host 'Fixed'