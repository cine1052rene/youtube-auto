$f="C:\Program Files\Adobe\Adobe Premiere Pro 2026\AMT\application.xml"
$t=[IO.File]::ReadAllText($f)
$t=$t.Replace('<Data key="installedLanguages">ko_KR</Data>','<Data key="installedLanguages">en_US</Data>')
[IO.File]::WriteAllText($f,$t,(New-Object Text.UTF8Encoding $false))
