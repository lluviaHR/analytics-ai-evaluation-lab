"""Private scenario manifest; never mount this module or directory in agent sandbox."""
from dataclasses import dataclass

SEGMENTS = ("SMB", "Mid-market", "Enterprise")
PERIODS = ("2026-08", "2026-09")
BASE_SHARES = (0.50, 0.30, 0.20)
BASE_RATES = (0.10, 0.15, 0.25)

@dataclass(frozen=True)
class Scenario:
    identifier: str
    shares_after: tuple[float, ...]
    rates_after: tuple[float, ...]

SCENARIOS = (
    Scenario("case_001", (0.40, 0.30, 0.30), BASE_RATES),
    Scenario("case_002", BASE_SHARES, (0.12, 0.16, 0.25)),
    Scenario("case_003", (0.40, 0.30, 0.30), (0.12, 0.16, 0.25)),
    Scenario("case_004", BASE_SHARES, BASE_RATES),
)
