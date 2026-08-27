"""
루트 디렉토리 바로가기 실행기
사용법:
  python run_agent.py --auto
  python run_agent.py --keyword "삼성전자 HBM4"
"""
import sys
import subprocess
from pathlib import Path

agent_script = Path(__file__).resolve().parent / "stock-blog-agent" / "run.py"

if __name__ == "__main__":
    args = [sys.executable, str(agent_script)] + sys.argv[1:]
    sys.exit(subprocess.call(args))
