import urllib2
import urllib
import json
import sys
import getopt

"Define global variables"

'''
   This function is used to retrieve the json from the
   the Email Server Blacklist API @ https://www.dnswatch.info/dns/rbl-lookup
'''
def getJsonFromAPI(_completeURL):
    jsonResult = urllib2.urlopen(_completeURL).read()
    decodedJson = json.loads(jsonResult)
    return (jsonResult,decodedJson)

def getUserID(_ipaddr):
    "1. compose the URL of getting API userid"
    useridURL =  'https://www.dnswatch.info/blacklist-lookup' + '?host=' + _ipaddr
    "2.call getJsonFromAPI to get the json string returned from API"
    originJson,apiJson = getJsonFromAPI(useridURL)
    "3. get the userid from the json string"
    userid = apiJson['progressKey']
    return userid

def getBlacklistResult(_ipaddr):
    "1.compose new request URL"
    requestURL = 'https://www.dnswatch.info/blacklist-lookup-progress' + '?uid=' + getUserID(_ipaddr)
    "2.call getJsonFromAPI to get the json string from API"
    originalJson, apiJson = getJsonFromAPI(requestURL)
    return apiJson



def main():
    "use different options to specify parameters"

    "check the result"
    blacklistResultJson = getBlacklistResult('216.58.194.46')
    print blacklistResultJson
    "judge whether positiveReults has value or not"
    "You can change this IP to a variable."
    results = blacklistResultJson['positiveResults']
    print results
    if not results:
        print 'this IP is not blocked!'
    else:
        print 'This IP is blocked!'


"The program entry"
if __name__ == "__main__":
    "main(sys.argv[1:])"
    main()


