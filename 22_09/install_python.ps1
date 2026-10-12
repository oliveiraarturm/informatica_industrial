# ============================================================
# Install Python 3.11.9 - NO ADMIN REQUIRED
#
# - Installs Python only for the current Windows user
# - Installs pip
# - Installs the Python Launcher (py.exe) for current user
# - Adds Python and Scripts to the BEGINNING of USER PATH
# - Removes duplicate PATH entries
# - Tries to remove Microsoft Store Python aliases
# - Refreshes PATH in the current PowerShell session
# - Verifies python, pip and py
# ============================================================

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

$PythonVersion = "3.11.9"
$PythonMajorMinor = "311"

$InstallerName = "python-$PythonVersion-amd64.exe"

$DownloadUrl = `
    "https://www.python.org/ftp/python/$PythonVersion/$InstallerName"

$InstallerPath = Join-Path `
    $env:TEMP `
    $InstallerName

$InstallDir = Join-Path `
    $env:LOCALAPPDATA `
    "Programs\Python\Python$PythonMajorMinor"

$PythonExe = Join-Path `
    $InstallDir `
    "python.exe"

$ScriptsPath = Join-Path `
    $InstallDir `
    "Scripts"


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================"
Write-Host " Installing Python $PythonVersion"
Write-Host "============================================"
Write-Host ""

Write-Host "Installation directory:"
Write-Host "  $InstallDir"
Write-Host ""


# ------------------------------------------------------------
# Download installer
# ------------------------------------------------------------

Write-Host "Downloading Python installer..."
Write-Host ""

try {

    Invoke-WebRequest `
        -Uri $DownloadUrl `
        -OutFile $InstallerPath

}
catch {

    Write-Host ""
    Write-Error "Failed to download Python installer."
    Write-Error $_.Exception.Message
    exit 1

}


# ------------------------------------------------------------
# Install Python
# ------------------------------------------------------------

Write-Host "Installing Python..."
Write-Host ""

$InstallerArguments = @(
    "/quiet"
    "InstallAllUsers=0"
    "TargetDir=`"$InstallDir`""
    "PrependPath=0"
    "Include_pip=1"
    "Include_launcher=1"
    "InstallLauncherAllUsers=0"
    "Include_test=0"
    "Include_doc=0"
)

try {

    $Process = Start-Process `
        -FilePath $InstallerPath `
        -ArgumentList $InstallerArguments `
        -Wait `
        -PassThru

}
catch {

    Write-Host ""
    Write-Error "Failed to start Python installer."
    Write-Error $_.Exception.Message
    exit 1

}


# ------------------------------------------------------------
# Verify installer exit code
# ------------------------------------------------------------

if ($Process.ExitCode -ne 0) {

    Write-Host ""
    Write-Error "Python installer failed."
    Write-Error "Installer exit code: $($Process.ExitCode)"
    exit $Process.ExitCode

}

Write-Host "Python installer completed successfully."
Write-Host ""


# ------------------------------------------------------------
# Verify python.exe exists
# ------------------------------------------------------------

if (-not (Test-Path $PythonExe)) {

    Write-Host ""
    Write-Error "Python executable was not found:"
    Write-Error $PythonExe
    exit 1

}


# ------------------------------------------------------------
# Configure USER PATH
#
# Python goes FIRST so that:
#
#   python
#   pip
#
# resolve to this installation before WindowsApps aliases
# or older Python installations.
# ------------------------------------------------------------

Write-Host "Configuring USER PATH..."
Write-Host ""

$CurrentUserPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

if ($null -eq $CurrentUserPath) {
    $CurrentUserPath = ""
}


# Convert PATH into individual entries
$ExistingPaths = @(
    $CurrentUserPath -split ";" |
        Where-Object {
            -not [string]::IsNullOrWhiteSpace($_)
        }
)


# Remove Python directories we are about to add,
# preventing duplicates.
$FilteredPaths = @(
    $ExistingPaths |
        Where-Object {

            $Entry = $_.Trim().TrimEnd("\")

            ($Entry -ne $InstallDir.TrimEnd("\")) -and
            ($Entry -ne $ScriptsPath.TrimEnd("\"))
        }
)


# Put Python FIRST
$NewUserPaths = @(
    $InstallDir
    $ScriptsPath
) + $FilteredPaths


# Remove duplicate PATH entries while preserving order
$Seen = @{}

$UniquePaths = foreach ($Entry in $NewUserPaths) {

    $Normalized = $Entry.Trim().TrimEnd("\")

    if (-not $Seen.ContainsKey($Normalized.ToLowerInvariant())) {

        $Seen[$Normalized.ToLowerInvariant()] = $true

        $Normalized
    }
}


$NewUserPath = $UniquePaths -join ";"


# Save USER PATH permanently
[Environment]::SetEnvironmentVariable(
    "Path",
    $NewUserPath,
    "User"
)

Write-Host "USER PATH updated."
Write-Host ""


# ------------------------------------------------------------
# Disable Microsoft Store Python App Execution Aliases
#
# These normally live in:
#
# %LOCALAPPDATA%\Microsoft\WindowsApps
#
# This is best-effort. Even if Windows prevents their removal,
# our Python installation is first in PATH and therefore wins.
# ------------------------------------------------------------

Write-Host "Checking Microsoft Store Python aliases..."
Write-Host ""

$WindowsApps = Join-Path `
    $env:LOCALAPPDATA `
    "Microsoft\WindowsApps"

$AliasesToRemove = @(
    "python.exe"
    "python3.exe"
)


foreach ($Alias in $AliasesToRemove) {

    $AliasPath = Join-Path `
        $WindowsApps `
        $Alias

    if (Test-Path -LiteralPath $AliasPath) {

        try {

            Remove-Item `
                -LiteralPath $AliasPath `
                -Force `
                -ErrorAction Stop

            Write-Host "Removed alias:"
            Write-Host "  $AliasPath"

        }
        catch {

            Write-Warning "Could not remove alias: $AliasPath"
            Write-Warning $_.Exception.Message

            Write-Host ""
            Write-Host "This is not fatal."
            Write-Host "Python is placed before WindowsApps in PATH."

        }

    }
    else {

        Write-Host "Alias not present:"
        Write-Host "  $AliasPath"

    }

}

Write-Host ""


# ------------------------------------------------------------
# Refresh PATH for CURRENT PowerShell session
#
# Rebuild from:
#   USER PATH
#   MACHINE PATH
# ------------------------------------------------------------

Write-Host "Refreshing PATH for this PowerShell session..."
Write-Host ""

$UserPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

$MachinePath = [Environment]::GetEnvironmentVariable(
    "Path",
    "Machine"
)

$env:Path = "$UserPath;$MachinePath"


# ------------------------------------------------------------
# Remove installer
# ------------------------------------------------------------

if (Test-Path $InstallerPath) {

    try {

        Remove-Item `
            $InstallerPath `
            -Force

        Write-Host "Installer removed:"
        Write-Host "  $InstallerPath"

    }
    catch {

        Write-Warning "Could not remove installer:"
        Write-Warning $InstallerPath

    }

}

Write-Host ""


# ------------------------------------------------------------
# Verify Python directly
# ------------------------------------------------------------

Write-Host "============================================"
Write-Host " Testing Python installation"
Write-Host "============================================"
Write-Host ""

Write-Host "Direct Python executable:"
Write-Host "  $PythonExe"
Write-Host ""

& $PythonExe --version

Write-Host ""

& $PythonExe -m pip --version


# ------------------------------------------------------------
# Verify python command
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================"
Write-Host " PATH resolution"
Write-Host "============================================"
Write-Host ""

Write-Host "python command:"
Write-Host ""

try {

    python --version

}
catch {

    Write-Warning "The 'python' command could not be resolved."

}


Write-Host ""
Write-Host "python resolves to:"
Write-Host ""

Get-Command python `
    -ErrorAction SilentlyContinue |
    Select-Object `
        CommandType,
        Name,
        Source


# ------------------------------------------------------------
# Show every python.exe found in PATH
# ------------------------------------------------------------

Write-Host ""
Write-Host "All python.exe executables found in PATH:"
Write-Host ""

where.exe python 2>$null


# ------------------------------------------------------------
# Verify pip
# ------------------------------------------------------------

Write-Host ""
Write-Host "pip:"
Write-Host ""

try {

    pip --version

}
catch {

    Write-Warning "The 'pip' command could not be resolved."

}


Write-Host ""
Write-Host "pip resolves to:"
Write-Host ""

Get-Command pip `
    -ErrorAction SilentlyContinue |
    Select-Object `
        CommandType,
        Name,
        Source


# ------------------------------------------------------------
# Verify Python Launcher
# ------------------------------------------------------------

Write-Host ""
Write-Host "Python launcher:"
Write-Host ""

$PyCommand = Get-Command `
    py `
    -ErrorAction SilentlyContinue

if ($PyCommand) {

    py --version

    Write-Host ""
    Write-Host "py resolves to:"
    Write-Host ""

    $PyCommand |
        Select-Object `
            CommandType,
            Name,
            Source

}
else {

    Write-Host "Python Launcher (py.exe) not found in current PATH."

}


# ------------------------------------------------------------
# Final information
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================"
Write-Host " Python installation completed!"
Write-Host "============================================"
Write-Host ""

Write-Host "Version:"
Write-Host "  Python $PythonVersion"
Write-Host ""

Write-Host "Python:"
Write-Host "  $InstallDir"
Write-Host ""

Write-Host "Scripts:"
Write-Host "  $ScriptsPath"
Write-Host ""

Write-Host "Expected python.exe:"
Write-Host "  $PythonExe"
Write-Host ""

Write-Host "USER PATH begins with:"
Write-Host "  $InstallDir"
Write-Host "  $ScriptsPath"
Write-Host ""

Write-Host "Final check:"
Write-Host ""

python --version
python -m pip --version

Write-Host ""
Write-Host "Done."
Write-Host ""
