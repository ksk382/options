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


    # should the ticker list be shuffled? otherwise you always buy early on
    # large cap
    # for each ticker,
    #   pull a live quote

    # updated thought 4.10.21: if you're firing live like that, you don't
    # know what percentage of capital to throw at it. I.e. need all the buys
    # before you can estimate buy amounts

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