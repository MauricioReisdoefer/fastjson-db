# run_tests_and_commit.ps1

# Resetar terminal
Clear-Host

# Rodar pytest
Write-Host "Rodando testes com pytest..." -ForegroundColor Cyan
py -m pytest

# Verificar status do pytest
if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 5) {
    Clear-Host
    Write-Host "==================================" -ForegroundColor DarkGreen
    Write-Host "    TODOS OS TESTES PASSARAM! " -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor DarkGreen

    # Pedir mensagem do commit
    Write-Host ""
    $commitMessage = Read-Host "Digite a mensagem do commit: "

    # Fazer commit
    git add .
    git commit -m "$commitMessage"
    git push origin main

    Clear-Host
    Write-Host "==================================" -ForegroundColor DarkCyan
    Write-Host " 🚀 Commit enviado com sucesso! " -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor DarkCyan
}
else {
    Write-Host "==================================" -ForegroundColor DarkRed
    Write-Host " ❌ Testes falharam. Commit cancelado. " -ForegroundColor Red
    Write-Host "==================================" -ForegroundColor DarkRed
}