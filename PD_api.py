#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing relevant libraries.
from flask import Flask, request, render_template, json, jsonify
import pickle
import logging


# In[2]:


# Create a flask object.
app = Flask('PD_Model')


# In[3]:


# Load (deserialize) the pickled model.
model = pickle.load(open('PD_Model.pkl', 'rb'))


# In[4]:


# Include logging endpoints for healthcheck/status and metrics
@app.route('/status')
def healthcheck():
    response = app.response_class(
            response = json.dumps({'status': 'OK'}),
            status = 200,
            mimetype = 'application/json'
    )
        
    app.logger.info('Status request was successful!')
    return response


# In[5]:


@app.route('/metrics')
def metrics():
    response = app.response_class(
                response = json.dumps({'result': 'success'}),
                status = 200,
                mimetype = 'application/json'
    )
    
    app.logger.info('Metrics request was successful!')
    return response


# In[6]:


# Stream logs to a file.
logging.basicConfig(filename='PD_api.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


# In[7]:


# Define the route to which we wil send HTTP requests
@app.route('/', methods=['GET'])

# creating a home endpoint that will display an html form.
def Home():
    return render_template('index.html')

# Define a route for making prediction through a post method.
@app.route('/predict', methods=['POST'])

# Define the predict function to use the pickled model to predict inputs from the form.
def predict():
    if request.method == 'POST':
        
        # Numeric features.
        age = request.form['age']
        loanamount = request.form['loanamount']
        loannumber = request.form['loannumber']
        
        # Categorical features.
        # loanterm -15days, 30days, 60days, 90days(reference category).
        termdays_15 = request.form['termdays_15']
        if termdays_15 == '15':
            termdays_15 = 1
            termdays_30 = 0
            termdays_60 = 0
            #termdays_90 = 0
            
        elif termdays_15 == '30':
            termdays_15 = 0
            termdays_30 = 1
            termdays_60 = 0
            #termdays_90 = 0
            
        elif termdays_15 == '60':
            termdays_15 = 0
            termdays_30 = 0
            termdays_60 = 1
            #termdays_90 = 0
            
        else:
            termdays_15 = 0
            termdays_30 = 0
            termdays_60 = 0
            #termdays_90 = 1

            
        # Bank_account_type
        # Savings, Other, Current(reference category)
        bank_account_type_Other = request.form['bank_account_type_Other']
        if bank_account_type_Other == 'Other':
            bank_account_type_Other = 1
            bank_account_type_Savings = 0
        
        elif bank_account_type_Other == 'Savings':
            bank_account_type_Other = 0
            bank_account_type_Savings = 1
            
        else:
            bank_account_type_Other = 0
            bank_account_type_Savings = 0
            
        # Employment_status.
        # Employed, Others, Self-Employed, Student, Unemployed(ref category)
        employment_status_clients_Employed = request.form['employment_status_clients_Employed']
        if employment_status_clients_Employed == 'Employed':
            employment_status_clients_Employed = 1
            employment_status_clients_Others = 0
            employment_status_clients_Self_Employed = 0
            employment_status_clients_Student = 0
            
        elif employment_status_clients_Employed == 'Others':
            employment_status_clients_Employed = 0
            employment_status_clients_Others = 1
            employment_status_clients_Self_Employed = 0
            employment_status_clients_Student = 0
            
        elif employment_status_clients_Employed == 'Self_Employed':
            employment_status_clients_Employed = 0
            employment_status_clients_Others = 0
            employment_status_clients_Self_Employed = 1
            employment_status_clients_Student = 0
            
        elif employment_status_clients_Employed == 'Student':
            employment_status_clients_Employed = 0
            employment_status_clients_Others = 0
            employment_status_clients_Self_Employed = 0
            employment_status_clients_Student = 1
            
        else:
            employment_status_clients_Employed = 0
            employment_status_clients_Others = 0
            employment_status_clients_Self_Employed = 0
            employment_status_clients_Student = 0
            
        # Engineered Features.
        age_per_loannumber = round(age/loannumber, 2)
        amount_per_loannumber = round(loanamount/loannumber, 2)
        age_per_loanamount = round(age/loanamount, 2)
        
        if (employment_status_clients_Employed == 'Employed') and (bank_account_type_Other == 'Other'):
            employed_other = employment_status_clients_Employed * bank_account_type_Other
            
        if (employment_status_clients_Employed == 'Employed'):
            age_employed = age * employment_status_clients_Employed
            
        if (bank_account_type_Other == 'Other'):
            age_other = age * bank_account_type_Other
            
        # Prediction.
        features = [[age, loanamount, loannumber, termdays_15, bank_account_type_Other, 
                     employment_status_clients_Employed, age_per_loannumber, amount_per_loannumber, 
                     age_per_loanamount, employed_other, age_employed, age_other]]
        
        # Probability of Default 
        #pd = model.predict_proba(features)[:, 0]
        pd = model.predict(features)
        #output = pd * 100
        
        # Taking care of invalid outputs -that is, results less than 0 or greater than 100.
        if pd<0:
            return render_template('index.html', prediction_text='Invalid result for this user')
        
        elif pd>1:
            return render_template('index.html', prediction_text='Invalid result for this user')
        
        # If there are no anomalies in the result, print the output.
        else:
            return render_template('index.html', prediction_text='Your Probability of Default is {}'.format(pd))
     
    # Display the form.
    else:
        return render_template('index.html')

if __name__ == '__main__':
        app.run(debug=True)


# 

# In[ ]:




