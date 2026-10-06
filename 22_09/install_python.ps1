# ============================================================
# Install Python 3.11.9 - NO ADMIN REQUIRED
# Installs Python only for the current Windows user
# ============================================================

$PythonVersion = "3.11.9"
$InstallerName = "python-$PythonVersion-amd64.exe"

$DownloadUrl = "https://www.python.org/ftp/python/$PythonVersion/$InstallerName"

$InstallerPath = Join-Path $env:TEMP $InstallerName

$InstallDir = Join-Path `
    $env:LOCALAPPDATA `
    "Programs\Python\Python311"


Write-Host ""
Write-Host "============================================"
Write-Host " Installing Python $PythonVersion"
Write-Host "============================================"
Write-Host ""

Write-Host "Downloading Python..."

Invoke-WebRequest `
    -Uri $DownloadUrl `
    -OutFile $InstallerPath


Write-Host ""
Write-Host "Installing Python..."
Write-Host "Destination:"
Write-Host $InstallDir
Write-Host ""


Start-Process `
    -FilePath $InstallerPath `
    -ArgumentList @(
        "/quiet",
        "InstallAllUsers=0",
        "TargetDir=$InstallDir",
        "PrependPath=0",
        "Include_pip=1",
        "Include_launcher=1",
        "InstallLauncherAllUsers=0",
        "Include_test=0"
    ) `
    -Wait


# ------------------------------------------------------------
# Add Python to USER PATH
# ------------------------------------------------------------

$PythonPath = $InstallDir
$ScriptsPath = Join-Path $InstallDir "Scripts"

$CurrentUserPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

$PathsToAdd = @(
    $PythonPath,
    $ScriptsPath
)

foreach ($Path in $PathsToAdd) {

    if ($CurrentUserPath -notlike "*$Path*") {

        if ([string]::IsNullOrWhiteSpace($CurrentUserPath)) {
            $CurrentUserPath = $Path
        }
        else {
            $CurrentUserPath += ";$Path"
        }
    }
}


[Environment]::SetEnvironmentVariable(
    "Path",
    $CurrentUserPath,
    "User"
)


# Update PATH for this PowerShell session too
$env:Path = "$PythonPath;$ScriptsPath;$env:Path"


# ------------------------------------------------------------
# Remove installer
# ------------------------------------------------------------

if (Test-Path $InstallerPath) {
    Remove-Item $InstallerPath -Force
}


# ------------------------------------------------------------
# Test installation
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================"
Write-Host " Testing installation"
Write-Host "============================================"
Write-Host ""

& "$InstallDir\python.exe" --version

Write-Host ""

& "$InstallDir\python.exe" -m pip --version


Write-Host ""
Write-Host "============================================"
Write-Host " Python installation completed!"
Write-Host "============================================"
Write-Host ""
Write-Host "Python:"
Write-Host $PythonPath
Write-Host ""
Write-Host "Scripts:"
Write-Host $ScriptsPath
Write-Host ""
Write-Host "You may need to reopen PowerShell / CMD"
Write-Host "for the new PATH to be visible everywhere."
Write-Host ""