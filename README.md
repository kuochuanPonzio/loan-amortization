# Loan Amortization
Hello friends, please find the included usage instructions for the Loan Amortization tool.

## Importing Loan Data
This tool is preprogrammed to integrate with VSAC loans. The HTML parser function will read the loan details available on the "Loans in Repayment" page in the myVSAC portal. 

To import this information into the pragram navigate to the "Loans in Repayment" page in your web browser and pess ctrl+s or right click and select "Save as..." to save the HTML document to your local repo. Note: the tool expects your HTML file to be named "vsac.html". Now that you've saved the html file to the same directory as the parse_VSAC.py file, the program will be able to read and parse your loan information from the file at runtime.

## Executing the program
To run the program, it is as simple as executing the `python3 amor.py` command from the commandline and entering the requested input. You'll be asked what your monthly payment is and for how many months you plan to make this payment. As long as you enter a number for the month duration, the program will keep asking you for these details. This is so that if you plan to pay $500 towards your loans for the next 6 months, then $1000 for the following 2 months and then $800 for the remainder of the loan term (or something of this sort), you can indicate this by entering 
```
>500
>6
>1000
>2
>800
>[enter]
```
There will be prompt messages inbetween each input so the contents of the commandline won't look exactly like the above snippet. Once you've completed entering your repayment plan, the rest of the program will run and generate the "payments.csv" file which is a detailed month-by-month breakdown of your loan term defined by the schedule you entered.

## Repayment strategy
The program will collect loans into groups of like interest rates and put all extra payment towards the groups with the highest rates. This is the optimal strategy for paying the least interest and getting out of debt the quickest. 

**Note**: VSAC will not do this for you automatically so call them and request that they put a rule on your account to handle prepayment as such.
