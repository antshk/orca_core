#!/usr/bin/env python3
import argparse
import math
import time
from pathlib import Path

from common import PROJECT_ROOT, connect_hand, create_hand, shutdown_hand

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "orca_core" / "models" / "v1" / "orcahand_middle3_right" / "config.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo each middle-finger motor sequentially (motor-space).")
    parser.add_argument("config_path", nargs="?", default=str(DEFAULT_CONFIG_PATH), help="Path to config.yaml")
    parser.add_argument("--mock", action="store_true", help="Use MockOrcaHand instead of hardware")
    parser.add_argument("--cycles", type=int, default=3, help="Number of times to run through all three motors")
    parser.add_argument("--delta", type=float, default=6.0, help="Joint excursion in degrees from neutral")
    parser.add_argument("--pause", type=float, default=0.6, help="Pause in seconds between moves")
    args = parser.parse_args()

    hand = create_hand(args.config_path, use_mock=args.mock)
    try:
        connect_hand(hand)
        print(f"Running sequential middle3 demo with: {Path(args.config_path)}")
        motor_ids = list(hand.config.motor_ids)
        delta_rad = math.radians(args.delta)

        for cycle in range(1, args.cycles + 1):
            print(f"Cycle {cycle}/{args.cycles}")
            for motor_id in motor_ids:
                print(f"  -> move motor {motor_id} by +{args.delta} deg")
                current = hand.get_motor_pos(as_dict=True)
                target = current[motor_id] + delta_rad
                hand._motor_client.write_desired_pos([motor_id], [target])
                time.sleep(args.pause)

                print(f"  -> return motor {motor_id}")
                hand._motor_client.write_desired_pos([motor_id], [current[motor_id]])
                time.sleep(args.pause)

        return 0
    except KeyboardInterrupt:
        print("Interrupted by user.")
        return 0
    finally:
        shutdown_hand(hand)


if __name__ == "__main__":
    raise SystemExit(main())
