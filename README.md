# CREDIT-RISK-MODELING
Using Machine Learning to determine customers' credit worthiness based on their risk of default on loans. A customer's credit worthiness 
is inversely proportional to their probability of default (PD). This implies that the higher the PD the lower the credit worthiness of a person.

## DATA WRANGLING
The data collected showed that the bank makes small loans (N3000 - N60000) available to individuals without requesting their income level.
Analysis of the data showed that people with account type 'Others' performed better at loan repayment than people with account type 'Savings' and 'Current.'
Also, Unemployed people had a lesser percentage of default than Self-Employed and Employed people, implying that they were more likely to not default. 

These biases can somewhat be attributed to the amount of those data points available in the dataset. There are more data points on 'Employed' and 'Savings' than any other 
in their respective categories. Thus, there are more entries/record of defaulters in these categories than the entire records available for the other categories.
Example. total number of Employed = 300 (non-defaulters=200, defaulters=100; default rate=33.33%) while Unemployed = 95 (non-defaulters=80, defaulters=15; default rate=15.8%)

## MODEL SELECTION
After employing several classification models including Logistic Regression, KNN, SVC, and Naive_Bayes, Random Forest was chosen because it performed better 
with an AUC_ROC of 73% and F1_score of 72%.

## DEPLOYMENT
The model was deployed using Heroku. It takes in user's input through the User Interface (created using html) and then outputs their probability of default (PD). 
The higher the PD, the more risky the user.
