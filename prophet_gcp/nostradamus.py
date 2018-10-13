from fbprophet import Prophet
import dask.dataframe as dd
import pandas as pd

def run_prophet(timeserie, date_column="ds", y_column="y", index_column=None):
    """ Run prophet in a given timeserie 
        Arguments:
            timeserie: pd.Dataframe with the timeserie
            date_column: string with the name of the date column on the dataset
            y: name of the target variable
        Returns:
            Dataframe: pandas.Dataframe with the forecast result
    """
    assert index_column != None, "Must indicate an index_column"
    timeserie.rename(columns={date_column: 'ds', y_column: 'y'}, inplace=True)
    min_date, max_date = timeserie.ds.min(), timeserie.ds.max()
    idx = timeserie[index_column].unique()
    timeserie_ = _create_index_timeserie(min_date, max_date)
    model = Prophet(yearly_seasonality=True)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model.fit(timeserie)
    forecast = model.predict(timeserie_)
    timeserie_ = forecast.assign(index_column = lambda x: idx[0])
    return timeserie_

def _create_index_timeserie(min_date, max_date):
    time_index = pd.date_range(min_date, max_date)
    dates = pd.DataFrame({'ds': pd.to_datetime(time_index.values)}, \
                          index=range(len(time_index)))
    return dates