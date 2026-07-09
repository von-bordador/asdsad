"""Generate a deterministic hardware fault profile for the avionics lab."""

import argparse
import hashlib
import json
import random

CONFIG_FILE = "hardware_config.json"


def build_config(student_id: str) -> dict:
    if not (student_id.isdigit() and len(student_id) == 8):
        raise ValueError("Student ID must be exactly 8 digits.")

    digest = hashlib.sha256(student_id.encode("utf-8")).hexdigest()
    rng = random.Random(int(digest[:16], 16))

    return {
        "student_id": student_id,
        "signature_hash": digest[:12].upper(),
        "buffer_overflow_threshold": rng.randint(18, 32),
        "imu_voltage_drift": round(rng.uniform(1.0, 3.0), 4),
        "bus_race_delay_sec": round(rng.uniform(0.001, 0.006), 4),
        "seed_digest": digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate hardware_config.json from a student ID.")
    parser.add_argument("--id", required=True, dest="student_id", help="Unique 8-digit student ID")
    args = parser.parse_args()

    config = build_config(args.student_id)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print("[FAULT-SEED] Hardware profile locked")
    print(f"Student ID: {config['student_id']}")
    print(f"Signature: {config['signature_hash']}")
    print(f"Buffer Threshold: {config['buffer_overflow_threshold']}")
    print(f"IMU Drift: {config['imu_voltage_drift']}")
    print(f"Bus Race Delay: {config['bus_race_delay_sec']}s")
    print(f"Wrote: {CONFIG_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
