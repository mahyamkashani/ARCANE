import sys
from pathlib import Path

PR2_DIR = Path(__file__).resolve().parent / "pr2_controller"
sys.path.insert(0, str(PR2_DIR))

from pr2_controller import run_simulation
from logger import log_result
from constants import CONFIG, RESULT_FILE


def main():
    config_path = PR2_DIR / CONFIG
    result_path = PR2_DIR / RESULT_FILE

    output = run_simulation(str(config_path), use_ros=True)
    log_result(str(result_path), output)


if __name__ == "__main__":
    main()
