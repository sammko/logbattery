CREATE TABLE battery_reading (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    timezone TEXT NOT NULL,
    battery_name TEXT NOT NULL,
    charge_full_design INTEGER NOT NULL,
    charge_full INTEGER NOT NULL,
    charge_now INTEGER NOT NULL,
    current_now INTEGER NOT NULL,
    voltage_now INTEGER NOT NULL,
    status TEXT NOT NULL,
    present BOOLEAN NOT NULL,
    capacity INTEGER NOT NULL,
    capacity_level TEXT NOT NULL,
    technology TEXT NOT NULL,
    serial_number TEXT NOT NULL,
    cycle_count INTEGER NOT NULL
);