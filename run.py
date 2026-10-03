"""
=============================================================================
STOCK BLOG AGENT - ROOT PROXY (run.py)
루트 디렉토리에서 바로 실행할 수 있도록 stock-blog-agent/run.py로 연결해주는 프록시
=============================================================================
특징:
  - 주말(토/일) 및 대한민국 공휴일/대체공휴일/증시 휴장일 자동 감지 및 자동 건너뜀
  - 주말/공휴일에 강제 실행을 원할 경우 --force 옵션 지원

사용법:
  1. 자동 트렌드 분석 & 발행 (주말/공휴일 자동 스킵):
     python run.py --auto
  2. 아침 8시 시황 모닝 브리핑 (주말/공휴일 자동 스킵):
     python run.py --morning
  3. 주말/공휴일에도 강제 발행:
     python run.py --auto --force
  4. 특정 종목/키워드 지정 수동 포스팅:
     python run.py --keyword "삼성전자 HBM4 반도체"
  5. 로컬 테스트 (Git 푸시 제외):
     python run.py --auto --test
  6. 매일 정기 시각 스케줄러 (주말/공휴일 자동 스킵):
     python run.py --daily-at 08:00
  7. 오늘 휴장일/공휴일 여부 확인:
     python run.py --check-holiday
=============================================================================
"""

import sys
import subprocess
from pathlib import Path

# 윈도우 콘솔 UTF-8 출력 호환성 보장
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

agent_script = Path(__file__).resolve().parent / "stock-blog-agent" / "run.py"

if __name__ == "__main__":
    args = [sys.executable, str(agent_script)] + sys.argv[1:]
    sys.exit(subprocess.call(args))
