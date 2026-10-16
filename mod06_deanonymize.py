import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    # assign the identifiers
    identifiers = ["age", "gender", "zip3"]

    # filter out only the records that have a unique combination of identifiers
    anonUniques = anon_df.loc[
        ~anon_df.duplicated(subset=identifiers, keep=False)
    ]
    auxUniques= aux_df.loc[
        ~aux_df.duplicated(subset=identifiers, keep=False)
    ]

    # merge the unique lists into the matched one
    matches = anonUniques.merge(
        auxUniques,
        on=identifiers,
        how="inner",
        validate="one_to_one",
    )
    return matches[["anon_id", "name"]].rename(columns={"name": "matched_name"})


def deanonymization_rate(matches_df, anon_df):
    # simple fraction calculation
    return len(matches_df) / len(anon_df)
