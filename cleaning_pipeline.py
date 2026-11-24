import numpy as np
import pandas as pd


def clean_agent_data(txns: pd.DataFrame, agents: pd.DataFrame):
    """
    Clean raw mobile money agent transactions and merge agent metadata.

    Parameters
    ----------
    txns : pd.DataFrame
        Raw transaction records.
    agents : pd.DataFrame
        Master agent registry containing agent_id, county, and onboarded date.

    Returns
    -------
    tuple[pd.DataFrame, dict]
        (df_clean, cleaning_log) where df_clean is the standardized DataFrame
        and cleaning_log records row counts and anomalies at every step.
    """
    df = txns.copy()
    valid_agent_ids = set(agents["agent_id"].dropna().unique())

    cleaning_log = {
        "raw_row_count": int(len(df)),
        "duplicate_txn_ids_found": int(df.duplicated(subset=["txn_id"]).sum()),
        "duplicates_removed": 0,
        "missing_or_non_numeric_amounts_dropped": 0,
        "mixed_slash_dates_standardized": int(df["txn_date"].astype(str).str.contains("/").sum()),
        "txn_type_variants_before": sorted(df["txn_type"].dropna().unique().tolist()),
        "unregistered_agent_rows_flagged": 0,
        "outlier_amount_rows_flagged": 0,
        "final_clean_row_count": 0,
    }

    # 1. Deduplicate on txn_id, prioritizing rows with a valid registered agent_id
    df["_is_valid_agent_tmp"] = df["agent_id"].isin(valid_agent_ids)
    df = (
        df.sort_values(by=["txn_id", "_is_valid_agent_tmp"], ascending=[True, False])
        .drop_duplicates(subset=["txn_id"], keep="first")
        .drop(columns=["_is_valid_agent_tmp"])
        .reset_index(drop=True)
    )
    cleaning_log["duplicates_removed"] = cleaning_log["raw_row_count"] - int(len(df))

    # 2. Standardize txn_type (strip whitespace and title-case -> Deposit / Withdrawal)
    df["txn_type"] = df["txn_type"].astype(str).str.strip().str.title()

    # 3. Coerce amount to numeric and drop rows with missing / invalid amounts
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    invalid_amount_mask = df["amount"].isna()
    cleaning_log["missing_or_non_numeric_amounts_dropped"] = int(invalid_amount_mask.sum())
    df = df.loc[~invalid_amount_mask].copy()

    # 4. Parse mixed date formats (YYYY-MM-DD and YYYY/MM/DD) to datetime64[ns]
    df["txn_date"] = pd.to_datetime(
        df["txn_date"].astype(str).str.strip().str.replace("/", "-", regex=False),
        errors="coerce",
    )

    # 5. Flag unregistered agents and left-join master agent metadata
    df["is_valid_agent"] = df["agent_id"].isin(valid_agent_ids)
    cleaning_log["unregistered_agent_rows_flagged"] = int((~df["is_valid_agent"]).sum())

    agents_clean = agents.copy()
    agents_clean["onboarded"] = pd.to_datetime(agents_clean["onboarded"], errors="coerce")
    df = df.merge(agents_clean, on="agent_id", how="left")
    df["county"] = df["county"].fillna("Unknown")

    # 6. Flag extreme outlier amounts (>= KES 100,000) without deleting them
    df["is_outlier_amount"] = df["amount"] >= 100000
    cleaning_log["outlier_amount_rows_flagged"] = int(df["is_outlier_amount"].sum())

    # 7. Sort chronologically by txn_id and record final row count
    df = df.sort_values("txn_id").reset_index(drop=True)
    cleaning_log["final_clean_row_count"] = int(len(df))

    return df, cleaning_log
