import sys
import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath): 
    '''
    Function combines two separate datasets for messages and categories and returns dataframe.
    input:
        messages_filepath: Filepath messages
        categories_filepath: Filepath categories
    returns:
        df: Merge of both datasets
    '''
    categories = pd.read_csv(categories_filepath)
    messages = pd.read_csv(messages_filepath)
    # merge datasets
    df = pd.merge(categories,messages, how='inner', on=['id'], left_index=True)
    
    
    # create a dataframe of the 36 individual category columns
    #categories = df['categories'].str.split(pat=';',expand=True)
    categories = df.categories.str.split(';', expand = True)
    
    # select the first row of the categories dataframe
    row = categories[0:1]
    
    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything
    # up to the second to last character of each string with slicing
    category_colnames = row.apply(lambda x: x.str[:-2]).values.tolist()
    
    
    # rename the columns of `categories`
    categories.columns = category_colnames
    
     #adapt related to binary
    categories.related.loc[categories.related == 'related-2'] = 'related-1'

    for column in categories:
        # set each value to be the last character of the string
        #categories[column] = categories[column].str[-1]
        categories[column] = categories[column].astype(str).str[-1]

        # convert column from string to numeric
        categories[column] = categories[column].astype(int)

    # drop the original categories column from `df`

    df.drop(['categories'], axis=1, inplace=True)

    # concatenate the original dataframe with the new `categories` dataframe
    combination = [df,categories]
    df = pd.concat(combination, axis=1)

    return df




def clean_data(df):
    '''
    Takes dataframe and drops duplicates
    Input: dataframe
    Returns: Dataframe without duplicates
    '''
    # drop duplicates
    df.drop_duplicates(inplace = True)
    return df


def save_data(df, database_filename):
     '''
    Saves dataframe in filepath in SQLITE
    Input: dataframe, name for file
    Returns: saves DF to to SQL DB
    '''
    engine = create_engine('sqlite:///'+database_filename)
    df.to_sql('DisasterResponse', engine,if_exists = 'replace', index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
