import urllib2
import json
import sys
import getopt
import datetime

'''
   This function is used to retrieve the json from the
   the Email Server Blacklist API @ https://www.dnswatch.info/dns/rbl-lookup
'''

"Define global variables"
IP = '98.150.108.228'
defaultAPI = 'https://www.dnswatch.info/blacklist-lookup-progress'
defaultUserIDLookUpAddr = 'https://www.dnswatch.info/blacklist-lookup'
isShowProgress = False

def getJsonFromAPI(_completeURL):
    jsonResult = urllib2.urlopen(_completeURL).read()
    decodedJson = json.loads(jsonResult)
    return (jsonResult,decodedJson)

def getUserID(_ipaddr):
    "1. compose the URL of getting API userid"
    useridURL =  defaultUserIDLookUpAddr + '?host=' + _ipaddr
    "2.call getJsonFromAPI to get the json string returned from API"
    originJson,apiJson = getJsonFromAPI(useridURL)
    "3. get the userid from the json string"
    userid = apiJson['progressKey']

    if isShowProgress:
        print "The API user ID has been successfully retrieved from: " + defaultUserIDLookUpAddr
    return userid

def getBlacklistResult(_ipaddr):
    "1.compose new request URL"
    requestURL =  defaultAPI + '?uid=' + getUserID(_ipaddr)
    "2.call getJsonFromAPI to get the json string from API"
    originalJson, apiJson = getJsonFromAPI(requestURL)

    if  isShowProgress:
        print "Data has been successfully retrieved from API at address of: " + defaultAPI
        print "Returned data is: \n" + str(apiJson)
    return apiJson

def main(arguments):
    "use different options to specify parameters"
    "The getopt parameter with ':' followed means that it requires a value after the option"
    try:
        opts,args = getopt.getopt(arguments,"vi:")
        for option,optarg in opts:
            if option in ("-v", "--ShowProgress"):
                global isShowProgress
                isShowProgress = True;
            elif option in ("-i", "--TargetIP"):
                global IP
                IP = optarg
    except getopt.GetoptError as e:
        print "The errors shows as follows: \n" + str(e)

    if isShowProgress:
        print "Program starts at: " + str(datetime.datetime.now())
        print "IP address to check is: " + IP
        print "-----------------------------------------------------------------"

    "check the result"
    blacklistResultJson = getBlacklistResult(IP)

    "judge whether positiveReults has value or not"
    "You can change this IP to a variable."
    results = blacklistResultJson['positiveResults']
    if isShowProgress:
        print results

    if not results:
        print 'this IP is not blocked!'
    else:
        print 'This IP is blocked!'


"The program entry"
if __name__ == "__main__":
    main(sys.argv[1:])



