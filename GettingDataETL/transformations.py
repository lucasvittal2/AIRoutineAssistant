from pandas import DataFrame, to_datetime

def change_tz(df :DataFrame, datimecol: str, tz:str)-> DataFrame:
    """Change the timezone of a dataframe to the specified timezone

    Args:
        df (DataFrame): The dataframe to change the timezone
        tz (str): The timezone to change to

    Returns:
        DataFrame: The dataframe with the new timezone
    """
    tmp_df = df.copy()
    tmp_df[datimecol] = to_datetime(tmp_df[datimecol])
    if tmp_df[datimecol].dt.tz is None:
        # If the datetime objects are naive, localize them to UTC first
        tmp_df[datimecol] = to_datetime(tmp_df[datimecol]).dt.tz_localize('UTC').dt.tz_convert(tz)
    else:
        # If the datetime objects are already timezone-aware, directly convert them to the new timezone
        tmp_df[datimecol] = to_datetime(tmp_df[datimecol]).dt.tz_convert(tz)
    return tmp_df