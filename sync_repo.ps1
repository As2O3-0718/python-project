[CmdletBinding()]
param(
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
    param(
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: git $($Arguments -join ' ')"
    }
}

try {
    $repoPath = $PSScriptRoot
    Set-Location -LiteralPath $repoPath

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw "Git was not found. Install Git and reopen PowerShell."
    }

    $gitRoot = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0) {
        throw "The script directory is not a Git repository: $repoPath"
    }

    $resolvedScriptRoot = (Resolve-Path -LiteralPath $repoPath).Path.TrimEnd('\')
    $resolvedGitRoot = (Resolve-Path -LiteralPath $gitRoot).Path.TrimEnd('\')
    if ($resolvedScriptRoot -ne $resolvedGitRoot) {
        throw "Place this script in the repository root: $resolvedGitRoot"
    }

    $currentBranch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $currentBranch) {
        throw "Cannot determine the current Git branch."
    }
    if ($currentBranch -ne $Branch) {
        throw "Current branch is '$currentBranch'; expected '$Branch'."
    }

    & git remote get-url $Remote *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Remote '$Remote' was not found."
    }

    $changes = @(& git status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "Cannot inspect the working tree."
    }
    if ($changes.Count -gt 0) {
        Write-Host "Uncommitted changes detected. Sync stopped:" -ForegroundColor Yellow
        & git status --short
        Write-Host "Commit or discard these changes, then run the script again." -ForegroundColor Yellow
        exit 2
    }

    Write-Host "Fetching the latest state from GitHub..." -ForegroundColor Cyan
    Invoke-Git -Arguments @("fetch", $Remote, $Branch)

    & git show-ref --verify --quiet "refs/remotes/$Remote/$Branch"
    if ($LASTEXITCODE -ne 0) {
        throw "Remote branch '$Remote/$Branch' does not exist."
    }

    $countsText = (& git rev-list --left-right --count "$Remote/$Branch...HEAD").Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Cannot compare local and remote commits."
    }

    $counts = $countsText -split '\s+'
    if ($counts.Count -ne 2) {
        throw "Cannot parse commit counts: $countsText"
    }

    $behind = [int]$counts[0]
    $ahead = [int]$counts[1]

    Write-Host "Local is ahead by $ahead commit(s) and behind by $behind commit(s)."

    if ($ahead -gt 0 -and $behind -gt 0) {
        Write-Host "Local and remote histories have diverged. No automatic merge will be attempted." -ForegroundColor Red
        Write-Host "Inspect: git log --oneline --graph --all" -ForegroundColor Yellow
        exit 3
    }

    if ($CheckOnly) {
        if ($ahead -eq 0 -and $behind -eq 0) {
            Write-Host "Check complete: local and GitHub are in sync." -ForegroundColor Green
        }
        elseif ($behind -gt 0) {
            Write-Host "Check complete: remote updates can be fast-forwarded safely." -ForegroundColor Yellow
        }
        else {
            Write-Host "Check complete: local commits can be pushed safely." -ForegroundColor Yellow
        }
        exit 0
    }

    if ($behind -gt 0) {
        Write-Host "Fast-forwarding remote updates..." -ForegroundColor Cyan
        Invoke-Git -Arguments @("pull", "--ff-only", $Remote, $Branch)
    }
    elseif ($ahead -gt 0) {
        Write-Host "Pushing local commits..." -ForegroundColor Cyan
        Invoke-Git -Arguments @("push", $Remote, $Branch)
    }
    else {
        Write-Host "No action needed: local and GitHub are in sync." -ForegroundColor Green
        exit 0
    }

    Write-Host "Sync complete." -ForegroundColor Green
    & git status -sb
}
catch {
    Write-Host "Sync failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
