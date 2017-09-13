# mercedClassAlert
A bot that checks if there is space in a class and sends an email or text alert
This program requires requets for python found at http://docs.python-requests.org


HOW TO USE:
First edit the classAlert.py file, and change email@gmail.com to a valid email, and password to that email's password. If an error occurs when run, the email may not allow unsafe apps to run using it, which can be changed at: https://myaccount.google.com/u/1/lesssecureapps

Go to this website: https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.p_selectsubject
and find the class you want an alert for. Find the subject code (i.e. CHEM, ENGR etc.) and the three didgit number
Put your info in classList.txt in this layout:

%
N
SUBJECT
NUMBER	
EMAIL

continue to do this for all classes wanted, at the end of the file type:
#END

When this is done simply run the classAlert.py file
