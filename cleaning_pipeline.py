import numpy as np
import pandas as pd


def clean_agent_data(txns: pd.DataFrame, agents: pd.DataFrame):
    """
    Clean raw mobile money agent transactions and reconcile against the master agent registry.

    Parameters
    ----------
    txns : pd.DataFrame
        Raw transaction records.
    agents : pd.DataFrame
        Master agent registry containing agent_id, county, and tier.

    Returns
    -------
    tuple[pd.DataFrame, dict]
        (df_clean, cleaning_log)
    """
    cleaning_log = {
        "raw_rows": int(len(txns)),
    }

    df = txns.copy()
    valid_agent_ids = set(agents["agent_id"].dropna().unique())

    # 1. Deduplicate on txn_id, prioritizing rows with registered agent_ids
    df["_valid_agent_priority"] = df["agent_id"].isin(valid_agent_ids).astype(int)
    df = (
        df.sort_values(by=["txn_id", "_valid_agent_priority"], ascending=[True, False])
        .drop_duplicates(subset=["txn_id"], keep="first")
        .drop(columns=["_valid_agent_priority"])
        .copy()
    )
    cleaning_log["duplicates_removed"] = int(cleaning_log["raw_rows"] - len(df))

    # 2. Standardize txn_type casing and whitespace
    raw_types = df["txn_type"].astype(str).tolist()
    df["txn_type"] = df["txn_type"].astype(str).str.strip().str.title()
    cleaning_log["txn_type_standardized"] = int(
        sum(r != c for r, c in zip(raw_types, df["txn_type"].tolist()))
    )

    # 3. Validate numeric amounts, attach transparent amount_flag & amount_imputed columns, and drop unrecoverable missing amounts
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    missing_mask = df["amount"].isna()
    cleaning_log["missing_or_invalid_amounts_dropped"] = int(missing_mask.sum())

    df["amount_flag"] = np.where(missing_mask, "missing_or_invalid_dropped", "valid")
    df["amount_imputed"] = False

    # Keep clean valid-amount ledger for financial reporting
    df = df.loc[~missing_mask].copy()

    # 4. Normalize slash date separators to hyphens before parsing
    date_str = df["txn_date"].astype(str).str.strip().str.replace("/", "-", regex=False)
    cleaning_log["mixed_date_formats_normalized"] = int(
        df["txn_date"].astype(str).str.contains("/", regex=False).sum()
    )
    df["txn_date"] = pd.to_datetime(date_str, format="%Y-%m-%d", errors="coerce")

    # 5. Reconcile against master agent registry
    meta_cols = [c for c in agents.columns if c == "agent_id" or c not in df.columns]
    df = df.merge(agents[meta_cols], on="agent_id", how="left")
    df["is_valid_agent"] = df["agent_id"].isin(valid_agent_ids)
    if "county" in df.columns:
        df["county"] = df["county"].fillna("Unknown")
    cleaning_log["unregistered_agent_rows_flagged"] = int((~df["is_valid_agent"]).sum())

    # 6. Flag extreme outlier amounts (>= KES 100,000) without deleting them
    df["is_outlier_amount"] = df["amount"] >= 100_000
    cleaning_log["extreme_outliers_flagged"] = int(df["is_outlier_amount"].sum())

    df = df.sort_values("txn_id").reset_index(drop=True)
    cleaning_log["final_clean_rows"] = int(len(df))
    cleaning_log["amount_flag_breakdown"] = {
        "valid": int(len(df)),
        "missing_or_invalid_dropped": cleaning_log["missing_or_invalid_amounts_dropped"],
    }

    return df, cleaning_log
