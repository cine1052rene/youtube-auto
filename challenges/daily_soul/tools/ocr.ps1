param([string]$img)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# 윈도우 내장 OCR: 각 줄의 텍스트와 위치(x,y,w,h)를 탭 구분으로 출력
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$t) { $task = $asTask.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait() | Out-Null; $task.Result }
$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($img)) ([Windows.Storage.StorageFile])
$stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$dec = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bmp = Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$null = [Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime]
$lang = [Windows.Globalization.Language]::new('en-US')
$eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$res = Await ($eng.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
foreach ($ln in $res.Lines) {
  $ws = $ln.Words; $x0 = ($ws | ForEach-Object { $_.BoundingRect.X } | Measure-Object -Minimum).Minimum
  $y0 = ($ws | ForEach-Object { $_.BoundingRect.Y } | Measure-Object -Minimum).Minimum
  $x1 = ($ws | ForEach-Object { $_.BoundingRect.X + $_.BoundingRect.Width } | Measure-Object -Maximum).Maximum
  $y1 = ($ws | ForEach-Object { $_.BoundingRect.Y + $_.BoundingRect.Height } | Measure-Object -Maximum).Maximum
  "{0}`t{1}`t{2}`t{3}`t{4}" -f [int]$x0, [int]$y0, [int]($x1-$x0), [int]($y1-$y0), $ln.Text
}
foreach ($ln in $res.Lines) { foreach ($w in $ln.Words) { "W`t{0}`t{1}`t{2}`t{3}`t{4}" -f [int]$w.BoundingRect.X, [int]$w.BoundingRect.Y, [int]$w.BoundingRect.Width, [int]$w.BoundingRect.Height, $w.Text } }
