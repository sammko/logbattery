#!/usr/bin/env python3
from pathlib import Path
from dataclasses import dataclass, asdict
from tzlocal import get_localzone_name
from arrow import Arrow


@dataclass
class BatteryReading:
    timestamp: str
    timezone: str
    battery_name: str
    charge_full_design: int
    charge_full: int
    charge_now: int
    current_now: int
    voltage_now: int
    status: str
    present: bool
    capacity: int
    capacity_level: str
    technology: str
    serial_number: str
    cycle_count: int

    @staticmethod
    def obtain(battery_name: str):
        fields = {
            "charge_full_design": int,
            "charge_full": int,
            "charge_now": int,
            "current_now": int,
            "voltage_now": int,
            "status": str,
            "present": lambda x: x == "1",
            "capacity": int,
            "capacity_level": str,
            "technology": str,
            "serial_number": str,
            "cycle_count": int,
        }

        path = Path("/sys/class/power_supply/") / battery_name

        data = {
            field: fn((path / field).read_text().strip())
            for field, fn in fields.items()
        }

        return BatteryReading(
            timestamp=str(Arrow.now().to(get_localzone_name())),
            timezone=get_localzone_name(),
            battery_name=battery_name,
            **data,
        )

    def insert(self, sqlite_cursor):
        data = [(k, v) for k, v in asdict(self).items()]
        cols = ", ".join([k for k, _ in data])
        vals = ", ".join(["?"] * len(data))
        sqlite_cursor.execute(
            f"INSERT INTO battery_reading ({cols}) VALUES ({vals})",
            [v for _, v in data],
        )


if __name__ == "__main__":
    import sqlite3
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("battery_name", type=str)
    parser.add_argument("sqlite_db_path", type=str)
    args = parser.parse_args()

    conn = sqlite3.connect(args.sqlite_db_path)
    cursor = conn.cursor()

    reading = BatteryReading.obtain(args.battery_name)
    reading.insert(cursor)

    conn.commit()
    conn.close()
