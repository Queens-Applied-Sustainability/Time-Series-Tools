import timeflow

if __name__ == '__main__':

    timeflow.Rename(label='rename', data_from='time-series.csv',
                             columns={'Temperature': 'temperature'})


    timeflow.BooleanFilter(label='cool', data_from='rename',
                               column='temperature', operator='<', value=15.4)

    print timeflow.routines['cool'].get_all()
