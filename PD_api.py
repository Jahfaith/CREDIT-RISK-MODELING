#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing relevant libraries.
from flask import Flask, request, render_template, json, jsonify
import pickle


# In[2]:


# Create a flask object.
app = Flask('PD_Model')


# In[3]:


# Load (deserialize) the pickled model.
model = pickle.load(open('PD_Model.pkl', 'rb'))


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
        age = int(request.form['age'])
        # Setting a condition to ensure that age is above 17.
        if age < 18:
            return render_template('index.html', prediction_text='Not within eligible age')
        elif age > 75:
            return render_template('index.html', prediction_text='Not within eligible age')
        
        loanamount = int(request.form['loanamount'])
        # Setting a condition to ensure that the amount entered is between 5000 and 60000.
        if loanamount < 5000:
            return render_template('index.html', prediction_text='Please enter a loan amount above 4999')
        elif loanamount > 60000:
            return render_template('index.html', prediction_text='Please enter a loan amount below 61000')
      
        loannumber = int(request.form['loannumber'])
        # Setting a condition to ensure that zero is not allowed in this field.
        if loannumber < 1:
            return render_template('index.html', prediction_text='Please enter a loan number')

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
        
        employed_other = employment_status_clients_Employed * bank_account_type_Other
        if (employment_status_clients_Employed == 'Employed') and (bank_account_type_Other == 'Other'):
            return employed_other
            
        age_employed = age * employment_status_clients_Employed
        if (employment_status_clients_Employed == 'Employed'):
            return age_employed
                    
        age_other = age * bank_account_type_Other
        if (bank_account_type_Other == 'Other'):
            return age_other
                    
        # Prediction.
        features = [[age, loanamount, loannumber, termdays_15, termdays_30, termdays_60, bank_account_type_Other,
                     bank_account_type_Savings, employment_status_clients_Employed, employment_status_clients_Others,
                     employment_status_clients_Self_Employed, employment_status_clients_Student, age_per_loannumber, 
                     amount_per_loannumber, age_per_loanamount, employed_other, age_employed, age_other]]
        
        # Probability of Default 
        pd = model.predict_proba(features)[:, 0]
        output = pd * 100
        
        # Outputting the result
                
        # Taking care of invalid outputs -that is, results less than 0 or greater than 100.
        if output<0:
            return render_template('index.html', prediction_text='Invalid result for this user')
        
        elif output>100:
            return render_template('index.html', prediction_text='Invalid result for this user')
        
        # If there are no anomalies in the result, print the output.
        else:
            return render_template('index.html', prediction_text="Your Probability of Default is {}%".format(output))
     
    # Display the form.
    else:
        return render_template('index.html')

if __name__ == '__main__':
        app.run(debug=True)


# 

# In[ ]:




