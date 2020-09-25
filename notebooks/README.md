Here we have 3 notebooks, each answering a different question from the case study. 
Q1 - Is there a connection between number of orders 
Q2 - Is there a connection between number of orders and territories
Q3 - Freeform - Is there a connection between employees and the total amount of their sales? A connection between employees and the number of items in each of their sales?

There is also a functions.py file from which one can import the various functions all in one neat spot.

Our conclusions
Q1 - We reject the Null hypothesis and state there is not no relation between quantity ordered and discount

Q2 - The shapiro test with p-value 0.00118 which is less than 0.05. We can reject the null hypothises. Therefore the data does not fit the normal distribution. And we choose wilcoxon test which gives us p_value 0 which is less than 0.05. We can reject the null hypothises. Therefore there is difference in number of orders and territory

Q3 - There was indeed a connection between employees and total order price, as well as a connection between employees and total order quantity. Some employees outperforming others. Anne and Robert, in particular, excelled. See the notebooks for details.