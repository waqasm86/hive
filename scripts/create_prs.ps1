# Usage: set $env:GITHUB_TOKEN locally, then run this script from repo root
# Example: $env:GITHUB_TOKEN = 'NEW_PAT'

if (-not $env:GITHUB_TOKEN) {
  Write-Error "GITHUB_TOKEN env var not set. Export it locally before running this script."
  exit 1
}

$headers = @{ Authorization = "token $env:GITHUB_TOKEN"; Accept = 'application/vnd.github+json' }
$pr_body = Get-Content PR_DESCRIPTION_ci_windows_fixes.md -Raw

$forkPayload = @{ title = 'ci: fix CI lint/test for Windows'; head = 'waqasm86:chore/fix-windows-tests-encoding-clean'; base = 'main'; body = $pr_body } | ConvertTo-Json
$upstreamPayload = @{ title = 'ci: Windows & CI fixes'; head = 'waqasm86:chore/fix-windows-tests-encoding-clean'; base = 'main'; body = $pr_body } | ConvertTo-Json

Write-Host "Creating PR on your fork (waqasm86/hive)..."
Invoke-RestMethod -Method Post -Uri 'https://api.github.com/repos/waqasm86/hive/pulls' -Headers $headers -Body $forkPayload | ConvertTo-Json | Write-Host

Start-Sleep -Seconds 1
Write-Host "Creating upstream PR to adenhq/hive (from your fork branch)..."
Invoke-RestMethod -Method Post -Uri 'https://api.github.com/repos/adenhq/hive/pulls' -Headers $headers -Body $upstreamPayload | ConvertTo-Json | Write-Host

Write-Host "Done. If requests fail, check token scope (needs repo) and that branch exists on your fork."