import sys


def load_data(database_filepath):
    engine = create_engine('sqlite:///'+ database_filepath)
    df = pd.read_sql_table('response','sqlite:///'+ database_filepath)
    X = df['message']
    Y = df[df.columns[4:]]
    category_names = Y.columns.tolist()
    return X, Y, category_names



def tokenize(text):
    
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
    # Set up the pipelines 
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])

    #Split data into train and test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state = 1)

    np.random.seed(13)
    #Fit pipeline
    pipeline.fit(X_train, Y_train)


def evaluate_model(model, X_test, Y_test, category_names):
    y_pred = pipeline.predict(X_test)

    #Function to report scores
    def create_classification_report (Y_test, y_pred):
        for i, col in enumerate(Y_test.columns):
            print()
            print(col)
            print(classification_report(Y_test.iloc[:,i], y_pred[:,i]))
        
    create_classification_report(Y_test,y_pred)


def save_model(model, model_filepath):
    #Export Pickle File
    file_name = 'model.pkl'
    with open (file_name, 'wb') as file:
        pickle.dump(cv,file)


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
