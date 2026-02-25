# Apply exported patch files to repository (PowerShell)
# Run this from the repo root: .\patch_export\apply_patch.ps1

$root = Resolve-Path ".."
Write-Host "Repository root inferred:" $root

$files = @(
    @{src="patch_export\core\services\llm_service.py"; dst="core\services\llm_service.py"},
    @{src="patch_export\pkg_resources.py"; dst="pkg_resources.py"}
)

foreach ($f in $files) {
    $src = Join-Path $PSScriptRoot (Split-Path $f.src -NoQualifier)
    $dst = Join-Path $PSScriptRoot "..\" + $f.dst
    Write-Host "Copying" $src "->" $dst
    Copy-Item -Path $src -Destination $dst -Force
}

Write-Host "Patch applied. Run your venv python manage.py check/migrate as needed."