from tensor_time import munge

def main():

    #run checks
    '''
    check whether the data for the day exists
    get account cash amount
     
    '''

    # load model

    # load ticker list

    # load df1 and df2 (combined dataframes from today and yesterday)

    # for each ticker,
    #   pull a live quote

    #   merge the data into a tensor
    #   munge(df1, df2, quote_df)
    #   strip out the columns not used in the model
    #   normalize the data to the train norms
    #   push the tensor through the model to get a buy decision

    #   execute a buy decision
    #   log the buys

    return

if __name__ == '__main__':
    main()