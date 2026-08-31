# =============================================================================
# Stock Blog Morning Briefing - Windows Task Scheduler Auto Registration
# 매일 아침 8시 정각에 증시 시황을 자동 발행하는 윈도우 작업 스케줄러 등록 스크립트
# =============================================================================

$TaskName = "StockBlog_Morning_Briefing_0800"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BatPath = Join-Path $ScriptDir "run_morning.bat"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🤖 [Value Stock Labs] 아침 8시 시황 자동 발행 스케줄러 등록" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "실행 대상 파일: $BatPath" -ForegroundColor Yellow

# 기존 등록된 동일 작업이 있다면 제거
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# 작업 액션 정의 (배치 파일 실행)
$Action = New-ScheduledTaskAction -Execute $BatPath -WorkingDirectory $ScriptDir

# 매일 아침 8시 00분 트리거 정의
$Trigger = New-ScheduledTaskTrigger -Daily -At "08:00AM"

# 작업 설정 (네트워크 연결 시 실행, 실패 시 3회 재시도 등)
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# 작업 스케줄러 등록
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Value Stock Labs 매일 아침 8시 글로벌 증시 시황 및 경제 뉴스 자동 발행 에이전트" | Out-Null

Write-Host "🎉 [등록 성공] 'StockBlog_Morning_Briefing_0800' 작업이 매일 아침 8시 실행으로 등록되었습니다!" -ForegroundColor Green
Write-Host "확인 방법: 윈도우 검색창에서 '작업 스케줄러' 실행 후 작업 목록 확인" -ForegroundColor Cyan
