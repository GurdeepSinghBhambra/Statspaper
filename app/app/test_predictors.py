from predictors import preprocessor, __testStockRegressors, __testSentiementIntensityClassifier
import pandas as pd
import os

invalid=False
while(True):
    print("**********************************************************************")
    print("\t\t\t\tWelcome\n")
    print("1. Test Stock Regressors")
    print("2. Test Sentiment Intensity Classifier")
    print("3. Exit")
    if(invalid):
        print("\nInvalid choice! Please Enter a valid Choice")
    print("**********************************************************************")

    choice = input("Enter your choice: ")
    if(choice == '1'):
        invalid=False
        filename = input("\nEnter test file path:")
        while(not os.path.isfile(filename)):
            print("Invalid File path, Please check your file path")
            filename = input("\nEnter test file path:")
        try:
            df = pd.read_csv(filename)
            test_high = [df.drop([col for col in df.keys() if col not in ["Open Price", "Low Price"]], axis=1).values]
            test_high.append(df["High Price"].values)
            test_low = [df.drop([col for col in df.keys() if col not in ["Open Price", "High Price"]], axis=1).values]
            test_low.append(df["Low Price"].values)
            print("Results:")
            __testStockRegressors(test_high, test_low)
        except Exception as exx:
            print("\nError:", exx.__repr__())
            print("\nMake sure correct file is provided and the file format or its contents aren't modified")
            print("Expected File is : test_data\\stock_test.csv\n")

    elif(choice == '2'):
        invalid=False
        filename = input("\nEnter test file path:")
        while(not os.path.isfile(filename)):
            print("Invalid File path, Please check your file path")
            filename = input("\nEnter test file path:")
 
        try:
            df = pd.read_csv(filename)
            headlines = df["Headlines"].values
            predictions = df["Sentiment"].values
            print("Results:")
            __testSentiementIntensityClassifier(headlines, predictions)
        except Exception as exx:
            print("\nError:", exx.__repr__())
            print("\nMake sure correct file is provided and the file format or its contents aren't modified")
            print("Expected File is : test_data\\sentiment_test.csv\n")

    elif(choice == '3'):
        break
    else:
        invalid=True
    print("\n")

