import pandas as pd


def charger_irve(chemin: str) -> pd.DataFrame:
    return pd.read_csv(chemin, dtype=str, low_memory=False)


def profil_colonnes(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "taux_manquants_%": (df.isna().mean() * 100).round(2),
            "valeurs_distinctes": df.nunique(),
            "exemple": df.apply(
                lambda col: col.dropna().iloc[0] if col.notna().any() else None
            ),
        }
    ).sort_values("taux_manquants_%", ascending=False)


def periode(df: pd.DataFrame, colonne: str) -> tuple:
    dates = pd.to_datetime(df[colonne], errors="coerce")
    return dates.min(), dates.max()
