param([Parameter(Mandatory=$true)][int]$TrialPid, [Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
'timestamp_utc,dedicated_bytes,shared_bytes' | Set-Content -LiteralPath $OutputPath -Encoding utf8
while (Get-Process -Id $TrialPid -ErrorAction SilentlyContinue) {
    try {
        $snapshot = Get-Counter -Counter '\GPU Process Memory(*)\Dedicated Usage','\GPU Process Memory(*)\Shared Usage' -MaxSamples 1 -ErrorAction SilentlyContinue
        $samples = @($snapshot.CounterSamples | Where-Object { $_.InstanceName -like "pid_${TrialPid}_*" -and $_.Status -in @(0,1) })
        if ($samples.Count -lt 2) { Start-Sleep -Milliseconds 500; continue }
        $dedicated = ($samples | Where-Object { $_.Path -like '*\dedicated usage' } | Measure-Object CookedValue -Sum).Sum
        $shared = ($samples | Where-Object { $_.Path -like '*\shared usage' } | Measure-Object CookedValue -Sum).Sum
        if ($null -eq $dedicated) { $dedicated = 0 }
        if ($null -eq $shared) { $shared = 0 }
        "$(Get-Date -AsUTC -Format o),$([long]$dedicated),$([long]$shared)" | Add-Content -LiteralPath $OutputPath -Encoding utf8
        Start-Sleep -Milliseconds 500
    } catch {
        $_.Exception.Message | Add-Content -LiteralPath ($OutputPath + '.error.txt') -Encoding utf8
        Start-Sleep -Milliseconds 500
    }
}
