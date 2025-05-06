from functools import wraps


def log_pandas_pipefunc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        shape_before = args[0].shape
        shape_after = result.shape
        print(f"{func.__name__} => before shape:{shape_before} after shape:{shape_after}")
        return result
    return wrapper

@log_pandas_pipefunc
def rename_cols(df, renamer = str.lower, remove_s = ('dates',)):
    return (
        df
        .rename(columns=renamer)
        .rename(columns = {col: col[:-1] for col in remove_s})
    )

@log_pandas_pipefunc
def parse_date_types(df, date_cols = ('date',)):
    return (
        df
        .assign(**{col: lambda df: pd.to_datetime(df[col]) for col in date_cols})
    )

@log_pandas_pipefunc
def set_date_as_index(df, date_col='date'):
    return df.set_index(date_col).sort_index()

@log_pandas_pipefunc
def filter_date(df, start='2004', end='2014'):
    return df.loc[start:end]

@log_pandas_pipefunc
def resample(df, sample='M', value='category', agg='count'):
    return df.resample(sample)[[value]].agg(agg)

@log_pandas_pipefunc
def get_rolling(df, window=10, col='category', agg='mean'):
    return df.assign(**{f'col_rolling': lambda df: df[col].rolling(window).agg(agg)})

(
    sanfran
    .pipe(rename_cols)
    .pipe(parse_date_types)
    .pipe(set_date_as_index)
    .pipe(filter_date)
    .pipe(resample)
    .pipe(get_rolling)
).plot(figsize=(9,5), title='Crime Count in San Fransisco')