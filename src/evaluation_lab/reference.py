"""Two independent reference routes: pandas and SQL (DuckDB/SQLite)."""
import sqlite3
import pandas as pd
from .scenarios import SEGMENTS, PERIODS

SQL_SUMMARY = """
SELECT period, segment, COUNT(*) AS eligible, SUM(converted) AS conversions
FROM trials GROUP BY period, segment ORDER BY period, segment
"""

def summarize_pandas(df):
    s=(df.groupby(["period","segment"],sort=True)
       .agg(eligible=("converted","size"),conversions=("converted","sum"))
       .reset_index())
    return s

def summarize_sql(df, engine="duckdb"):
    if engine == "duckdb":
        import duckdb
        con=duckdb.connect(database=":memory:")
        try:
            con.register("trials",df)
            return con.execute(SQL_SUMMARY).df()
        finally:con.close()
    if engine == "sqlite":
        con=sqlite3.connect(":memory:")
        try:
            df.to_sql("trials",con,index=False)
            return pd.read_sql_query(SQL_SUMMARY,con)
        finally:con.close()
    raise ValueError("engine must be duckdb or sqlite")

def decompose(summary):
    """Symmetric Kitagawa, returns rates and effects in percentage points."""
    def period_values(period):
        sub=summary.loc[summary.period == period].set_index("segment").reindex(SEGMENTS)
        if sub.isnull().any().any() or (sub.eligible <= 0).any():
            raise ValueError("Every segment must have a positive denominator")
        weights=(sub.eligible/sub.eligible.sum()).to_numpy(dtype=float)
        rates=(sub.conversions/sub.eligible).to_numpy(dtype=float)
        return weights,rates
    w0,r0=period_values(PERIODS[0]); w1,r1=period_values(PERIODS[1])
    baseline=float((w0*r0).sum()); after=float((w1*r1).sum())
    mix=float(((w1-w0)*(r0+r1)/2).sum())
    within=float(((r1-r0)*(w0+w1)/2).sum())
    return {"baseline_rate_pct":100*baseline,"after_rate_pct":100*after,
            "total_change_pp":100*(after-baseline),
            "mix_pp":100*mix,"within_pp":100*within}

def references(df, engine="duckdb"):
    return independent_references(df,engine=engine)


DECOMPOSITION_SQL = """
WITH segment_counts AS (
  SELECT period, segment, COUNT(*) AS eligible, SUM(converted) AS conversions
  FROM trials GROUP BY period, segment
), rates AS (
  SELECT period, segment,
    CAST(eligible AS DOUBLE) / SUM(eligible) OVER (PARTITION BY period) AS weight,
    CAST(conversions AS DOUBLE) / eligible AS rate
  FROM segment_counts
), paired AS (
  SELECT a.segment, a.weight AS w0, b.weight AS w1, a.rate AS r0, b.rate AS r1
  FROM rates a JOIN rates b ON a.segment = b.segment
  WHERE a.period = '2026-08' AND b.period = '2026-09'
)
SELECT 100*SUM(w0*r0) AS baseline_rate_pct,
       100*SUM(w1*r1) AS after_rate_pct,
       100*(SUM(w1*r1)-SUM(w0*r0)) AS total_change_pp,
       100*SUM((w1-w0)*(r0+r1)/2) AS mix_pp,
       100*SUM((r1-r0)*(w0+w1)/2) AS within_pp
FROM paired
"""

def sql_reference(df, engine="duckdb"):
    """Compute both aggregation AND decomposition using SQL, not pandas math."""
    if engine == "duckdb":
        import duckdb
        con = duckdb.connect(database=":memory:")
        try:
            con.register("trials", df)
            row = con.execute(DECOMPOSITION_SQL).df().iloc[0]
        finally:
            con.close()
    elif engine == "sqlite":
        con = sqlite3.connect(":memory:")
        try:
            df.to_sql("trials", con, index=False)
            row = pd.read_sql_query(DECOMPOSITION_SQL, con).iloc[0]
        finally:
            con.close()
    else:
        raise ValueError("engine must be duckdb or sqlite")
    return {k: float(row[k]) for k in
            ("baseline_rate_pct", "after_rate_pct", "total_change_pp", "mix_pp", "within_pp")}

def independent_references(df, engine="duckdb"):
    return decompose(summarize_pandas(df)), sql_reference(df, engine=engine)
