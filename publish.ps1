# publish.ps1

# Carrega variáveis do .env
$envPath = ".\.env"
if (Test-Path $envPath) {
    Get-Content $envPath | ForEach-Object {
        if ($_ -match "^\s*([^#=]+)\s*=\s*(.+)\s*$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
} else {
    Write-Error ".env file not found!"
    exit 1
}

# Verifica se o token do PyPI está definido
if (-not $env:PYPI_TOKEN) {
    Write-Error "PYPI_TOKEN not found in .env"
    exit 1
}

# Limpa builds antigos
if (Test-Path ".\dist") { Remove-Item -Recurse -Force ".\dist" }

# Build da biblioteca
python -m build

# Envia para PyPI
python -m twine upload dist/* -u __token__ -p $env:PYPI_TOKEN
