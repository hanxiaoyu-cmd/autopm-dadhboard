$c = [System.IO.File]::ReadAllText("index.html")
$start = $c.IndexOf("function v16RenderRealProjectTasks")
$endFunc = $c.IndexOf("function ", $c.IndexOf("function v16FilterL4Dept") + 30)
$before = $c.Substring(0, $start)
$after = $c.Substring($endFunc)
$newCodeFromFile = [System.IO.File]::ReadAllText("_new_l4.txt", [System.Text.Encoding]::UTF8)
$result = $before + $newCodeFromFile + $after
[System.IO.File]::WriteAllText("index.html", $result, [System.Text.Encoding]::UTF8)
Write-Host "Done! Length: $($result.Length)"
