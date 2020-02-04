#!/usr/bin/env python
# coding: utf-8

# # Getting Insights from Data
# 
# Demostración del dataset

# In[1]:


import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.express as px
import numpy as np


path = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRORx2TSYJz4kdDYn2Mev8sDrWkc6eT6PwRoRjK4fZdyedsSTWs1c80A8ZbsSkFNPqe_BYn8kaQUHal/pub?output=csv"

data = pd.read_csv(path)

data.head()


# In[2]:


data_day = data.groupby(("ORDERDATE")).agg(
                                  {'SALES': 'sum', "ORDERDATE": "max" })


# ## Ventas por dias

# In[3]:


# Figura
fig = go.Figure()
fig.add_trace(go.Scatter(x = data_day["ORDERDATE"], y = data_day["SALES"], name="Sales"))


fig.update_layout(title_text='Ventas por dias',
                    xaxis_rangeslider_visible=True,
                    scene = dict( aspectratio = dict( x = 1.7, y = 0.5, z = 1) ), margin=dict(l=0, r=0, b=20, t=0),
                    template="plotly_dark"
                 )
fig.show()


# ## Ventas por meses

# In[4]:


data_month = data.groupby(("ORDERMONTH")).agg(
                                  {'SALES': 'sum', "ORDERMONTH": "max" })


data_month.insert(loc=0, column='index', value=np.arange(len(data_month)))
dic1 = pd.merge(data_month, data_month["SALES"], left_on = data_month["index"], right_on = data_month["index"]+1, how='outer')
dic1 = dic1.dropna(axis = 0, thresh = 3)
dic1["%"] = round(((dic1["SALES_x"]/dic1["SALES_y"])-1)*100, 2)


# In[5]:


# Figura
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x = dic1["ORDERMONTH"], y = dic1["SALES_x"], name="Sales"),secondary_y=False)
fig.add_trace(go.Bar(x = dic1["ORDERMONTH"], y = dic1["%"], name="%"),secondary_y=True),

fig.update_layout(title_text='Ventas por dias',
                    
                    scene = dict( aspectratio = dict( x = 1.7, y = 0.5, z = 1) ), margin=dict(l=10, r=10, b=20, t=0),
                    template="plotly_dark"
                 )
fig.show()


# ## Where go we sell more, and what do we sell in those places?

# In[6]:


data_contry = data.groupby(("COUNTRY")).agg(
                                  {'SALES': 'sum'})
data_contry.sort_values(by=['SALES'], ascending=False).head(15)


# In[7]:


data_contry1 = data.groupby(("COUNTRY", "PRODUCTLINE")).agg(
                                  {'SALES': 'sum'})
data_contry1.sort_values(by=['SALES', "COUNTRY"], ascending=False).head(30)


# ## How many customers do we have?

# In[8]:


data_contry2 = data.groupby(("CUSTOMERNAME")).nunique() 
data_contry2 = data_contry2.shape
print("El total de clientes es: " + str(data_contry2[0]) )


# ## Is there any product line that has decreased sales dramatically during the last year?

# In[51]:


fecha1 = ["2005-01-01", "2005-12-31"] 
data1 = np.logical_and( data["ORDERDATE"] >= fecha1[0], data["ORDERDATE"] <= fecha1[1] )
data1 = data[data1]

data_product = data1.groupby(("ORDERMONTH", "PRODUCTLINE")).agg(
                                  {'SALES': 'sum', "ORDERMONTH": "max", "PRODUCTLINE": "max" })
dic2 = pd.merge(data_product, data_product["SALES"], left_on = data_product.index, right_on = data_product.index, how='outer')
dic2


# In[93]:


fig = px.line(dic2, x="ORDERMONTH", y="SALES_x", color='PRODUCTLINE')
fig.update_layout(scene = dict(aspectratio = dict( x = 2, y = 1.1), 
                                yaxis = dict( nticks = 7 ),
                
                   
                                xaxis_title='Month',
                                yaxis_title=''
                              ),template="plotly_dark", 
                  margin = dict(l=0, r=0, b=30, t=0)
                 )
fig.show()


# In[95]:


from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')

