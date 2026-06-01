$c = [System.IO.File]::ReadAllText("index.html")
$start = $c.IndexOf("function v16RenderRealProjectTasks")
$endFunc = $c.IndexOf("function ", $c.IndexOf("function v16FilterL4Dept") + 30)
$before = $c.Substring(0, $start)
$after = $c.Substring($endFunc)
$newCode = $before + $newFunc + $after
[System.IO.File]::WriteAllText("index.html", $newCode, [System.Text.Encoding]::UTF8)
Write-Host "Done! New file length: $($newCode.Length)"
