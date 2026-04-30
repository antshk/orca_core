#!/usr/bin/env python3
import argparse
from pathlib import Path

from common import PROJECT_ROOT, connect_hand, create_hand, shutdown_hand

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "orca_core" / "models" / "v1" / "orcahand_middle3_right" / "config.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrate the v1 middle3 right-hand setup.")
    parser.add_argument("config_path", nargs="?", default=str(DEFAULT_CONFIG_PATH), help="Path to config.yaml")
    parser.add_argument("--mock", action="store_true", help="Use MockOrcaHand instead of hardware")
    parser.add_argument("--force-wrist", action="store_true", help="Pass through force_wrist to calibrate().")
    args = parser.parse_args()

    hand = create_hand(args.config_path, use_mock=args.mock)
    try:
        connect_hand(hand)
        print(f"Starting calibration with: {Path(args.config_path)}")
        hand.calibrate(force_wrist=args.force_wrist)
        print("Calibration complete.")
        return 0
    finally:
        shutdown_hand(hand)


if __name__ == "__main__":
    raise SystemExit(main())
