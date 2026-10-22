"""Generate row-level, seed-reproducible synthetic trial outcomes."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from .scenarios import SCENARIOS, SEGMENTS, PERIODS, BASE_SHARES, BASE_RATES

COLUMNS = ["trial_id", "customer_id", "period", "segment", "converted"]

def _exact_counts(n, shares):
    raw = np.array(shares) * n
    counts = np.floor(raw).astype(int)
    for i in np.argsort(-(raw - counts), kind="stable")[:n - int(counts.sum())]:
        counts[i] += 1
    return counts

def generate_case(case, *, seed=20261021, n_per_period=20000, mode="exact"):
    if mode not in {"exact", "sampled"}:
        raise ValueError("mode must be exact or sampled")
    if n_per_period <= 0:
        raise ValueError("n_per_period must be positive")
    rng = np.random.default_rng(seed)
    rows = []
    for period_index, period in enumerate(PERIODS):
        shares = BASE_SHARES if period_index == 0 else case.shares_after
        rates = BASE_RATES if period_index == 0 else case.rates_after
        sizes = rng.multinomial(n_per_period, shares) if mode == "sampled" else _exact_counts(n_per_period, shares)
        for seg, size, rate in zip(SEGMENTS, sizes, rates):
            converted = (rng.binomial(1, rate, int(size)) if mode == "sampled"
                         else np.r_[np.ones(round(int(size)*rate), dtype=int),
                                     np.zeros(int(size)-round(int(size)*rate), dtype=int)])
            rng.shuffle(converted)
            for outcome in converted:
                rows.append((period, seg, int(outcome)))
    rng.shuffle(rows)
    return pd.DataFrame({
        "trial_id": [f"trial_{i:06d}" for i in range(1, len(rows)+1)],
        "customer_id": [f"cust_{i:06d}" for i in range(1, len(rows)+1)],
        "period": [r[0] for r in rows], "segment": [r[1] for r in rows],
        "converted": [r[2] for r in rows],
    }, columns=COLUMNS)

def canonical_csv_bytes(df):
    return df.to_csv(index=False, lineterminator="\n").encode("utf-8")

def export_all(root, *, seed=20261021, n_per_period=20000, mode="exact"):
    root = Path(root)
    public = root/"public"; private = root/"private"
    public.mkdir(parents=True, exist_ok=True); private.mkdir(parents=True, exist_ok=True)
    manifest = {"generator_version":"0.1.0", "seed":seed, "mode":mode,
                "n_per_period":n_per_period,"cases":{}}
    for case in SCENARIOS:
        df = generate_case(case, seed=seed, n_per_period=n_per_period, mode=mode)
        payload=canonical_csv_bytes(df)
        (public/f"{case.identifier}.csv").write_bytes(payload)
        manifest["cases"][case.identifier] = {"sha256":hashlib.sha256(payload).hexdigest(),"rows":len(df)}
    (private/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output", default="data/generated")
    parser.add_argument("--seed",type=int,default=20261021)
    parser.add_argument("--n-per-period",type=int,default=20000)
    parser.add_argument("--mode",choices=["exact","sampled"],default="exact")
    args=parser.parse_args()
    manifest=export_all(args.output,seed=args.seed,n_per_period=args.n_per_period,mode=args.mode)
    print(json.dumps(manifest,indent=2))
if __name__ == "__main__":main()
