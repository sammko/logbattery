#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"

poetry run ./logbattery.py BATT db.db
