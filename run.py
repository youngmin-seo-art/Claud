"""
=============================================================================
STOCK BLOG AGENT - ROOT PROXY (run.py)
루트 디렉토리에서 바로 실행할 수 있도록 stock-blog-agent/run.py로 연결해주는 프록시
=============================================================================
사용법:
  python run.py --auto --schedule 360
  python run.py --auto
  python run.py --keyword "삼성전자 HBM4"
=============================================================================
"""
import sys
import subprocess
from pathlib import Path

agent_script = Path(__file__).resolve().parent / "stock-blog-agent" / "run.py"

if __name__ == "__main__":
    args = [sys.executable, str(agent_script)] + sys.argv[1:]
    sys.exit(subprocess.call(args))
