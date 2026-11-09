"""Study parameters. Change these here, not inside the analysis code, so every
result in results/ can be traced back to one set of definitions."""

# --- Data (Databento) -------------------------------------------------------
DATASET = "GLBX.MDP3"   # CME Globex
SYMBOL = "NQ.v.0"       # continuous front contract, rolls to highest volume (same as Gabe)
SCHEMA = "ohlcv-1m"
STYPE_IN = "continuous"
RAW_DIR = "data/raw"

# --- Spending guard ----------------------------------------------------------
# Databento gives $125 of free historical credit. download.py keeps a running
# total in data/spend_log.json and refuses any download that would push that
# total past this cap, so the card on file is never needed. Keep it below 125.
MAX_TOTAL_SPEND = 100.00
MAX_PER_REQUEST = 10.00

# --- Session windows, America/New_York, [start, end) ------------------------
# Defaults follow NQStats' ALN study: Asia 20:00-02:00, London 02:00-08:00,
# NY 08:00-16:00. Asia starts the evening BEFORE the NY session it belongs to.
# Prof's diagram puts the NY open at 9:30; rerun with NY_START = "09:30" as a
# robustness check (London then stays 02:00-08:00 unless you change it too).
TZ = "America/New_York"
ASIA = ("20:00", "02:00")
LONDON = ("02:00", "08:00")
NY = ("08:00", "16:00")

# A session with fewer 1-min bars than this is treated as incomplete (holidays,
# data outages) and the whole day is dropped. Full sessions: 360 / 360 / 480.
MIN_BARS = {"asia": 180, "london": 180, "ny": 240}

# "Asia engulfs London": strict (>, <) matches the NQStats wording
# "Asia high exceeds London high and Asia low undercuts London low".
STRICT_ENGULF = True
