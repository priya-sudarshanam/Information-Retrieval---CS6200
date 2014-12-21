a) Python version - 2.7.5
b) Libraries employed - urllib, sys, httplib, time, re
c) The code employs two functions in addition to a loop

Function names and details regarding the functions:
a) approvedSites:
     Input: link
    Output: Boolean
    The objective of this function is to check  whether the link is in the list of disallowed links according to    
   robots.txt. Returns true if is allowed
b) crawl_web:
    Input : parsed link which is either a html, or pdf.   
    Output:  stack. 
    Objective: Each link, which if unvisited, is appended  to the stack and a dictionary.
c) Main function: 
    This is a loop which parses and 'creates' a new url and tries to connect with it after a 5 sec delay. On 
    approval, the header is checked for restricting the output to either html or pdf pages.

