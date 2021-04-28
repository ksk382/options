from tensor_time import munge
import os
import pandas as pd
import datetime as dt
from tensor_time import munge
from tensorflow.keras.models import load_model
from api_auth import get_auth_headers
from query_quote import api_quote
from api_calls import get_stock_df, get_balance, sell_stock, buy_stock, acct_num, get_holdings

def import_model():
    model_path = '../ML_logs/'
    #list_of_models = [(model_path + i) for i in os.listdir(model_path) if i.endswith('.h5')]
    # print (list_of_models)
    #latest_file = max(list_of_models, key=os.path.getctime)
    m_name = '2021-04-28_10.58_mse_0.11_return_0.0116_h_0.00867_model.h5'
    latest_file = '../ML_logs/'+ m_name
    print (latest_file)
    input('check this model filename')
    model = load_model(latest_file)
    hurdle = float(latest_file.split('_h_')[-1].replace('_model.h5', ''))
    return model, hurdle

def load_quote_df():
    quote_df_path = '../quote_dataframes/'
    flist = [(quote_df_path + i) for i in os.listdir(quote_df_path) if i.endswith('.csv')]
    latest_file = max(flist, key=os.path.getctime)
    quote_df = pd.read_csv(latest_file, compression='gzip')
    return quote_df

def load_df(day_str):
    df_path = '../combined_dataframes/'
    fname = df_path + day_str + '.csv'
    df = pd.read_csv(fname, compression = 'gzip')
    return df


def prep_data(today_str, yest_str):
    # load quote dataframe
    quote_df = load_quote_df()
    df1 = load_df(yest_str)
    df2 = load_df(today_str)
    print (today_str, yest_str)

    df3 = munge(df1, df2, quote_df)
    df3 = df3.reset_index()

    # trim to the proper columns
    final_cols = pd.read_csv('../ML_content/final_cols.csv', compression='gzip')
    final_cols = list(final_cols['0'])
    tensor_df = df3[final_cols]

    # norm the data
    train_stats = pd.read_csv('../ML_content/train_stats.csv', compression='gzip', index_col=0)
    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']
    tensor_df = norm(tensor_df)
    tensor_df.fillna(0, inplace=True)

    return df3, tensor_df


def report_holdings():
    x = get_holdings()
    # print (x)
    print(json.dumps(x, indent=4, sort_keys=True))

    df = pd.DataFrame([])
    for i in x['holding']:
        j = i['instrument']
        k = i['quote']
        del i['instrument']
        del i['quote']
        d4 = dict(i, **j);
        d4.update(k)
        df = df.append(d4, ignore_index=True)

    df['totalsecurities'] = x['totalsecurities']

    df = df[['sym', 'price', 'costbasis', 'purchaseprice', 'gainloss', 'lastprice',
             'marketvalue', 'marketvaluechange', 'accounttype', 'cfi', 'change', 'cusip', 'desc',
             'extendedquote', 'factor', 'format', 'matdt', 'mmy', 'mult',
             'putcall', 'qty', 'sectyp', 'sodcostbasis', 'strkpx',
             'underlying', 'totalsecurities']]

    now = dt.datetime.now()
    today_str = dt.datetime.strftime(now, "%Y-%m-%d")

    fname = f'../recs/{today_str}_holdings.csv'
    df.to_csv(fname, compression='gzip', index=False)


def get_recs(model, hurdle, df3, tensor_df):

    test_predictions = model.predict(tensor_df)

    rec = df3.merge(tensor_df, left_index=True, right_index=True,
                 how='outer', suffixes=('', '_zz'))
    rec.drop(rec.filter(regex='_zz$').columns.tolist(),axis=1, inplace=True)
    rec['test_pred'] = test_predictions

    #rec.columns = ['symbol', 'name', 'close_price']
    rec['hurdle'] = hurdle
    rec['hurdle_price'] = rec['latestPrice'] + rec['latestPrice'] * rec['hurdle']
    rec['hurdle_price'] = rec['hurdle_price'].round(2)
    rec['ba_hurdle'] = rec['hurdle_price'] - rec['ba_spread']
    rec['confidence'] = test_predictions
    rec['buy'] = (rec['confidence'] > .5) * 1

    return rec

def scrub_no_go(rec):
    no_go_df = pd.read_csv('../aws_scp/no_go.csv')
    x = no_go_df[no_go_df['exclude'] == 1]['Ticker']
    y = rec[rec['symbol'].isin(x)].index
    rec = rec.drop(rec.index[y])
    rec = rec.sort_values(by='confidence', ascending=False)
    return rec




def api_quote(symbol, headers):

    canonical_querystring = 'token=' + access_key
    canonical_uri = f'/v1/stock/{symbol}/quote'
    endpoint = "https://" + host + canonical_uri
    request_url = endpoint + '?' + canonical_querystring
    r = requests.get(request_url, headers=headers)
    d = r.json()
    df = pd.DataFrame([d])
    return df

def main():

    #run checks
    '''
    check whether the data for the day exists
    get account cash amount
    '''

    def prev_weekday(adate):
        adate -= dt.timedelta(days=1)
        while adate.weekday() > 4:  # Mon-Fri are 0-4
            adate -= dt.timedelta(days=1)
        return adate

    now = dt.datetime.now()
    #now = now - dt.timedelta(days=3)
    today_str = dt.datetime.strftime(now, "%Y-%m-%d")
    yest = prev_weekday(now)
    yest_str = dt.datetime.strftime(yest, "%Y-%m-%d")


    print (today_str, yest_str)
    input('check those dates')

    df3, tensor_df = prep_data(today_str, yest_str)


    # load model
    model, hurdle = import_model()

    #run the model
    rec = get_recs(model, hurdle, df3, tensor_df)

    # filter out nogos
    rec = scrub_no_go(rec)


    z = rec[rec['buy'] == 1]
    print(z)
    print(len(z.index))
    print('\n\n\n\n')

    rec_dir = '../recs/'
    if not os.path.exists(rec_dir):
        os.mkdir(rec_dir)
    out_name = rec_dir + f'rec_{today_str}_hurdle--{hurdle}.csv'
    z.to_csv(out_name, compression='gzip', index=False)

    return

if __name__ == '__main__':
    main()