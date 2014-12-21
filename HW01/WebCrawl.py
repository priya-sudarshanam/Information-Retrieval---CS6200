# import libraries
import urllib, sys, httplib, time, re

##################################
#  global variables
seed = "http://www.ccs.neu.edu" 
httpref = "http://"
stack = []
stack.append(seed)
#dictionary to hold visited pages/links
visited = {}                
pagelimit = 28         
hrefvar = "a href=\""
httpvar = "http"
#header variable to check content-type link for html pages
htmllink = 'text/html'
#header variable to check content-type link for pdf pages
pdflink = 'application/pdf'
#output is redirected to this file
outputfile = 'C:/Users/Priya/Desktop/IR/HW01/Qn3output.txt' 
filemode = 'w'
getvar = "GET"
ctype = 'Content-Type'
path = "/"
invalid_links = []

################################################

# function: approvedSites
# input: url to be checked against robots.txt
# output: Returns True if link is not in robots.txt
def approvedSites(link):
   try:
      rp = robotparser.RobotFileParser()
      rp.set_url(link)
      rp.read()
      apSite = rp.apSite("*", link)
   except:
      apSite = True
   return apSite


#function: crawl_web
#input: takes in each url
#output: checks if it has been visited. If not visited,
#it is added to the stack
def crawl_web(html):
    for i in range(len(html)):
      if(hrefvar == html[i:i+len(hrefvar)]):
        url = ""
        i += len(hrefvar)
        while(html[i] != "\""):
          url += html[i]
          i += 1
        if(url[0:4] == httpvar):
           if not url in visited: 
                stack.append(url)
                visited[url] = True
    return stack

#main function
#pagelimit: number of pages visited on the web.
#Here if the pagelimit becomes 0, the stack is printed
#indicating the links it has visited the output is redirected
#to a text file
while (pagelimit >= 0):
 if pagelimit == 0:
    f = open(outputfile, filemode)
    for i in stack:
      f.write(i + '\n')
    f.close()
    print True
 
 pagelimit -= 1
 popped_page = stack.pop()
 
 if (popped_page.startswith(httpref)):
    url = popped_page.replace(httpref, "", 1)
    host = url
    split_url = url.split("/")

    if (len(split_url) > 1):
      host = split_url[0]
      path = url.replace(host, "", 1)

    #delay of 5 seconds between conecting with host
    time.sleep(5)
    conn = httplib.HTTPConnection(host)
    req = conn.request(getvar, path)

    #respect robots.txt
    if approvedSites(url):
        res = conn.getresponse()
         #checks header for either html/pdf
        if (htmllink in res.getheader(ctype)) or (pdflink in res.getheader(ctype)):
             html=res.read()
        else:
            invalid_links.append(res)
            continue
               
   
#executing the program
 if __name__ == '__main__':
     crawl_web(html)
