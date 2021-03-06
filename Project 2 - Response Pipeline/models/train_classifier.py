import sys
# import libraries
import pandas as pd
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
import re
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
import pickle
nltk.download(['punkt', 'wordnet'])


def load_data(database_filepath):
    '''
    Loads data from provided sql databse path. Reads source CSV as DF and defines X, Y and category names.
    Input: SQLite DB filepath
    Returns: X and Y with associated category names
    '''
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('DisasterResponse', engine)
    X = df['message']
    Y = df[df.columns[4:]]
    category_names = Y.columns.tolist()
    return X, Y, category_names
    load_data('response.db')



def tokenize(text):
    '''
    Splits a string into a sequence of tokens for later processing. Tokens then are lemmatized (grouping together of inflected forms) 
    Input: String
    Returns: tokenised and lemmatised string
    '''

    # get rid of special characters
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)

    # tokenize text
    tokens = word_tokenize(text)

    # initiate lemmatizer
    lemmatizer = WordNetLemmatizer()

    # iterate through each token
    clean_tokens = []
    for tok in tokens:

        # lemmatize, normalize case, and remove leading/trailing white space
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    '''
    Creates pipeline, defines parameters and tunes with Gridsearch
    Input: none
    Returns: Model
    '''
    # Set up the pipelines
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    
    parameters ={
        'tfidf__norm':['l2','l1'],
        'clf__estimator__min_samples_split':[2,3],
        }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    
    return cv 


def evaluate_model(cv, X_test, Y_test, category_names):
    '''
    Evaluate model by returning classification report
    Input: Grid search Model, X_test, Y_test, catgegory_names
    Returns: printed classification report
    '''
    y_pred = cv.predict(X_test)
    

    #Function to report scores
    def create_classification_report (Y_test, y_pred):
        for i, col in enumerate(Y_test.columns):
            print()
            print(col)
            print(classification_report(Y_test.iloc[:,i], y_pred[:,i]))

    create_classification_report(Y_test,y_pred)


def save_model(model, model_filepath):
    '''
    Saves the model as pkl
    Input: model and path to save model
    Returns: saved pkl file in file path
    '''
    #Export Pickle File
    file_name = 'model.pkl'
    with open (file_name, 'wb') as file:
        pickle.dump(model,file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
