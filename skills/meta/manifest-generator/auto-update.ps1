# Claude Code Skill Manifest Auto-Update Script
Write-Host "Updating Claude Code Skill Manifest..." -ForegroundColor Green

$skillsPath = Join-Path $env:USERPROFILE ".claude\skills"
$generatorPath = Join-Path $skillsPath "meta\manifest-generator\generate_manifest_simple.py"

Set-Location $skillsPath

if (Test-Path $generatorPath) {
    Write-Host "Running manifest generator..." -ForegroundColor Yellow
    python3 $generatorPath
    
    Write-Host "Manifest update complete!" -ForegroundColor Green
    
    # Count total skills
    $skillCount = (Get-ChildItem -Path $skillsPath -Recurse -Name "SKILL.md" | Measure-Object).Count
    Write-Host "Total skills found: $skillCount" -ForegroundColor Cyan
    
    # Show categories
    Write-Host "`nSkills by category:" -ForegroundColor Cyan
    Get-ChildItem -Path $skillsPath -Directory | ForEach-Object {
        $category = $_.Name
        $categorySkills = (Get-ChildItem -Path $_.FullName -Recurse -Name "SKILL.md" | Measure-Object).Count
        if ($categorySkills -gt 0) {
            Write-Host "  $category`: $categorySkills" -ForegroundColor White
        }
    }
    
    Write-Host "`n✅ Manifest is now up-to-date!" -ForegroundColor Green
} else {
    Write-Host "Error: Manifest generator not found at $generatorPath" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")