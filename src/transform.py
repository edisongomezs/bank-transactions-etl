import pandas as pd

# ------------------------------------------
# LOAD DATA
# ------------------------------------------
def load_data(path):
    return pd.read_csv(path)


# ------------------------------------------
# CLEAN AMOUNT
# ------------------------------------------
def clean_amount(df):
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)
    return df

# ------------------------------------------
# CLEAN TIMESTAMP
# ------------------------------------------
def clean_timestamp(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

# ------------------------------------------
# SPLIT VALID / INVALID WITH REASON
# ------------------------------------------
def split_valid_invalid(df):

    df = df.copy()

    # Crear columna de error
    df["error_reason"] = None

    # Detectar errores
    invalid_amount = df["amount"].isna()
    invalid_timestamp = df["timestamp"].isna()

    # Asignar razones
    df.loc[invalid_amount & invalid_timestamp, "error_reason"] = "INVALID_AMOUNT_AND_TIMESTAMP"
    df.loc[invalid_amount & ~invalid_timestamp, "error_reason"] = "INVALID_AMOUNT"
    df.loc[~invalid_amount & invalid_timestamp, "error_reason"] = "INVALID_TIMESTAMP"

    # Separar datasets
    invalid_df = df[df["error_reason"].notna()].copy()
    valid_df = df[df["error_reason"].isna()].copy()

    # Opcional: quitar columna en válidos
    valid_df = valid_df.drop(columns=["error_reason"])

    return valid_df, invalid_df

# ------------------------------------------
# FILL NULLS
# ------------------------------------------
def fill_nulls(df):
    df["merchant"] = df["merchant"].fillna("UNKNOWN")
    return df

# ------------------------------------------
# DETECT OUTLIERS
# ------------------------------------------
def flag_outliers(df):
    df["is_outlier"] = df["amount"].abs() > 1000
    return df

# ------------------------------------------
# TRANSFORM PIPELINE
# ------------------------------------------
def transform_data(path):

    df = load_data(path)

    df = clean_amount(df)
    df = clean_timestamp(df)

    valid_df, invalid_df = split_valid_invalid(df)

    valid_df = fill_nulls(valid_df)
    valid_df = flag_outliers(valid_df)

    return valid_df, invalid_df