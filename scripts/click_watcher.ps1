# Click Watcher for Living Narrator (PowerShell/Windows)
# Captures screenshots at each mouse click to record player decisions

param(
    [string]$OutputDir = "C:\Temp\NarratorScreenshots\clicks",
    [string]$DecisionsFile = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\civi\narrator\state\decisions.jsonl",
    [double]$Cooldown = 0.5,
    [switch]$KeepAll = $false  # Keep all clicks (disable filtering)
)

# Decision zones (percentages of screen) - clicks outside these are navigation
# CK3 event popups appear in center, character interactions on sides
$DecisionZones = @(
    @{ Name="event_popup"; X1=0.20; Y1=0.10; X2=0.80; Y2=0.85 },   # Center (main decisions)
    @{ Name="character_panel"; X1=0.0; Y1=0.15; X2=0.25; Y2=0.85 } # Left panel (character interactions)
)

# Ignore zones (definitely navigation)
$IgnoreZones = @(
    @{ Name="top_bar"; X1=0.0; Y1=0.0; X2=1.0; Y2=0.05 },           # Top bar (resources, speed)
    @{ Name="bottom_bar"; X1=0.0; Y1=0.95; X2=1.0; Y2=1.0 },        # Bottom bar
    @{ Name="minimap"; X1=0.85; Y1=0.0; X2=1.0; Y2=0.25 },          # Top-right minimap
    @{ Name="close_buttons"; X1=0.75; Y1=0.0; X2=0.85; Y2=0.10 }    # Close button area
)

function Test-InZone {
    param($X, $Y, $Width, $Height, $Zone)
    $nx = $X / $Width
    $ny = $Y / $Height
    return ($nx -ge $Zone.X1 -and $nx -le $Zone.X2 -and $ny -ge $Zone.Y1 -and $ny -le $Zone.Y2)
}

function Test-IsDecisionClick {
    param($X, $Y, $Width, $Height)

    # Check if in ignore zone
    foreach ($zone in $IgnoreZones) {
        if (Test-InZone $X $Y $Width $Height $zone) {
            return @{ IsDecision=$false; Reason="ignore:$($zone.Name)" }
        }
    }

    # Check if in decision zone
    foreach ($zone in $DecisionZones) {
        if (Test-InZone $X $Y $Width $Height $zone) {
            return @{ IsDecision=$true; Zone=$zone.Name }
        }
    }

    # Outside all zones = probably navigation
    return @{ IsDecision=$false; Reason="outside_decision_zones" }
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class MouseHook {
    public delegate IntPtr HookProc(int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern IntPtr SetWindowsHookEx(int idHook, HookProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll")]
    public static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll")]
    public static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll")]
    public static extern IntPtr GetModuleHandle(string lpModuleName);

    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out POINT lpPoint);

    [StructLayout(LayoutKind.Sequential)]
    public struct POINT {
        public int X;
        public int Y;
    }
}
"@

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Host "🖱️  Click Watcher started"
Write-Host "   Output: $OutputDir"
Write-Host "   Decisions: $DecisionsFile"
Write-Host "   Cooldown: ${Cooldown}s"
if ($KeepAll) {
    Write-Host "   Filter: DISABLED (keeping all clicks)" -ForegroundColor Yellow
} else {
    Write-Host "   Filter: ENABLED (decisions only)" -ForegroundColor Green
    Write-Host "   Decision zones: event_popup (center), character_panel (left)"
    Write-Host "   Ignored: top_bar, bottom_bar, minimap, close_buttons"
}
Write-Host ""
Write-Host "Watching for clicks... (Ctrl+C to stop)"
Write-Host "  Green = decision captured"
Write-Host "  Gray  = navigation skipped"
Write-Host ""

$lastClickTime = [DateTime]::MinValue

function Capture-Click {
    param([int]$X, [int]$Y)

    $now = Get-Date
    $elapsed = ($now - $script:lastClickTime).TotalSeconds

    if ($elapsed -lt $Cooldown) {
        return
    }
    $script:lastClickTime = $now

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen
    $width = $screen.Bounds.Width
    $height = $screen.Bounds.Height

    # Check if this is a decision click (unless KeepAll is set)
    if (-not $KeepAll) {
        $result = Test-IsDecisionClick $X $Y $width $height
        if (-not $result.IsDecision) {
            Write-Host "[$($now.ToString('HH:mm:ss'))] Skip ($X, $Y) - $($result.Reason)" -ForegroundColor DarkGray
            return
        }
        $zone = $result.Zone
    } else {
        $zone = "all"
    }

    # Capture screenshot
    $timestamp = $now.ToString("yyyy-MM-dd_HH-mm-ss-fff")
    $filename = "click_${timestamp}_${X}_${Y}.png"
    $filepath = Join-Path $OutputDir $filename

    try {
        $bitmap = New-Object System.Drawing.Bitmap($width, $height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($screen.Bounds.Location, [System.Drawing.Point]::Empty, $screen.Bounds.Size)
        $bitmap.Save($filepath)
        $graphics.Dispose()
        $bitmap.Dispose()

        # Create decision record
        $decision = @{
            timestamp = $now.ToString("yyyy-MM-ddTHH:mm:ss.fff")
            x = $X
            y = $Y
            screen_width = $width
            screen_height = $height
            screenshot_path = $filepath
            zone = $zone
            ocr_text = ""
            region_ocr = ""
        }

        # Append to decisions file
        $json = $decision | ConvertTo-Json -Compress
        Add-Content -Path $DecisionsFile -Value $json -Encoding UTF8

        Write-Host "[$($now.ToString('HH:mm:ss'))] " -NoNewline
        Write-Host "Decision" -ForegroundColor Green -NoNewline
        Write-Host " ($X, $Y) [$zone] -> $filename"
    }
    catch {
        Write-Host "Error capturing: $_" -ForegroundColor Red
    }
}

# Simple polling approach (more reliable than hooks in PowerShell)
$lastState = [System.Windows.Forms.Control]::MouseButtons

while ($true) {
    $currentState = [System.Windows.Forms.Control]::MouseButtons

    # Detect left click (transition from None to Left)
    if ($currentState -eq [System.Windows.Forms.MouseButtons]::Left -and $lastState -eq [System.Windows.Forms.MouseButtons]::None) {
        $point = [System.Windows.Forms.Cursor]::Position
        Capture-Click -X $point.X -Y $point.Y
    }

    $lastState = $currentState
    Start-Sleep -Milliseconds 50
}
