# mercedClassAlert
A bot that checks if there is space in a class and sends an email or text alert

This program runs python 2.7 and requires requests for python found at http://docs.python-requests.org

Or if running linux with pip installed the command: pip install requests


HOW TO USE:
First edit the classAlert.py file, and change email@gmail.com to a valid email, and password to that email's password. If an error occurs when run, the email may not allow unsafe apps to run using it, which can be changed at: https://myaccount.google.com/u/1/lesssecureapps

Go to this website: https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.p_selectsubject
and find the class you want an alert for. Find the subject code (i.e. CHEM, ENGR etc.) and the three didgit number or CRN

Enter this information when prompted in terminal

Once entered it will run until the class has been found

If you desire to reset it once a class has been found, changing the line SKIP in classList.txt to N will allow it to trigger again.

This program will persist through server restarts, or loss of internet, and will automatically reconnect when possible