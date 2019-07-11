#Daniel Chan
#Insight Edgar Analytics Coding Challenge

from datetime import datetime

#returns the difference in seconds between two date times
def getTimeDifference(dateTimeOlder, dateTimeNewer):
    delta = dateTimeNewer - dateTimeOlder
    diffInSeconds = int(delta.total_seconds())
    return diffInSeconds

#converts unique request fields to a single string
def requestToString(cik, accession, extention):
    requestString = cik + " " + accession + " " + extention
    return requestString

#class for keeping track of a single ip address's requests and session
class edgarUser:
    def __init__(self, userIP, reqDateTime, reqString):
        self.ipAddress = userIP
        self.firstDateTime = reqDateTime
        self.latestDateTime = reqDateTime
        self.firstRequest = reqString
        self.latestRequest = reqString
        self.numRequests = 1
        self.activeSession = True
        self.waitingToOutput = False
        self.sessionEndTime = reqDateTime

    #check if this user's latest session has ended
    def isSessionOver(self, currentDateTime, timeLimit):
        if getTimeDifference(self.latestDateTime, currentDateTime) < timeLimit:
            return False
        else:
            return True

    #output session data as a string
    def outputSession(self):
        output = self.ipAddress + ","
        output += self.firstDateTime.strftime("%Y-%m-%d %H:%M:%S") + ","
        output += self.latestDateTime.strftime("%Y-%m-%d %H:%M:%S") + ","
        output += str(getTimeDifference(self.firstDateTime, self.latestDateTime) + 1) + ","
        output += str(self.numRequests)
        return output

def main():
    #create list that will hold IPs with active sessions
    requestQueue = []
    #create list that holds IPs in proper output order
    outputQueue = []
    #create dictionary that will hold edgarUsers
    userDict = {}

    #open log input file and output file
    inFile = open("../input/log.csv", "r")
    outFile = open("../output/edgar_sessions.txt", "w")

    #open file containing time limit for the session and store time limit in a variable
    timeLimitFile = open("../input/inactivity_period.txt", "r")
    sessionTimeLimit = int(timeLimitFile.readline())
    timeLimitFile.close()

    #datetime of the most recent request
    currentDateTime = datetime(1, 1, 1, 1, 1, 1)

    #loop through lines in log
    for line in inFile:
        #check to avoid header line
        if not line[0].isalpha():
            #extract relevant information from line
            fields = line.split(",")
            reqIP = fields[0]
            reqDate = fields[1]
            reqTime = fields[2]
            reqCIK = fields[4]
            reqAccession = fields[5]
            reqExtention = fields[6]

            #update current date time and request
            currentDateTime = datetime(int(reqDate[:4]), int(reqDate[5:7]), int(reqDate[8:10]), int(reqTime[:2]), int(reqTime[3:5]), int(reqTime[6:8]))
            print(currentDateTime)
            print(reqCIK)
            #print(requestQueue)
            currentRequest = requestToString(reqCIK, reqAccession, reqExtention)

            #check queue for sessions that have expired due to timeout and not file end, and output them
            if len(outputQueue) > 0:
                removeList = []
                for ip in outputQueue:
                    if userDict[ip].waitingToOutput and userDict[ip].sessionEndTime != currentDateTime:
                        removeList.append(ip)
                        outFile.write(userDict[ip].outputSession() + "\n")
                        userDict[ip].waitingToOutput = False
                for ip in removeList:
                    outputQueue.remove(ip)

            #add latest request to queue, remove ip from queue first if it's still active
            if reqIP in requestQueue:
                print(reqIP + " extended")
                requestQueue.remove(reqIP)
            else:
                outputQueue.append(reqIP)
            requestQueue.append(reqIP)

            #check dictionary for ip address, if not present add new edgarUser with ip as key, else modify edgarUser with new request data
            if reqIP in userDict:
                #user's latest session is still active
                if userDict[reqIP].activeSession:
                    #if the same request is made at the same time, ignore it
                    if not (userDict[reqIP].latestRequest == currentRequest and userDict[reqIP].latestDateTime == currentDateTime):
                        userDict[reqIP].latestDateTime = currentDateTime
                        userDict[reqIP].latestRequest = currentRequest
                        userDict[reqIP].numRequests += 1
                #user's latest session is no longer active, start a new session
                else:
                    userDict[reqIP].firstDateTime = currentDateTime
                    userDict[reqIP].latestDateTime = currentDateTime
                    userDict[reqIP].firstRequest = currentRequest
                    userDict[reqIP].latestRequest = currentRequest
                    userDict[reqIP].numRequests = 1
                    userDict[reqIP].activeSession = True
            else:
                userDict[reqIP] = edgarUser(reqIP, currentDateTime, currentRequest)
                print(reqIP + " added")

            #check queue for sessions that have just ended and output any that have
            if len(requestQueue) > 0:
                #index to cut off ended sessions from queue
                cutoffIndex = 0
                for ip in requestQueue:
                    if userDict[ip].isSessionOver(currentDateTime, sessionTimeLimit):
                        print(ip + " expired")
                        currentIP = userDict[ip].ipAddress
                        #outFile.write(userDict[ip].outputSession() + "\n")
                        userDict[ip].activeSession = False
                        userDict[ip].waitingToOutput = True
                        userDict[ip].sessionEndTime = currentDateTime
                        cutoffIndex += 1
                    else:
                        requestQueue[:] = requestQueue[cutoffIndex:]
                        break

            print(requestQueue)

    #end of file reached, any sessions that are still active will be output
    if len(requestQueue) > 0:
        for ip in outputQueue:
            outFile.write(userDict[ip].outputSession() + "\n")

    inFile.close()
    outFile.close()

if __name__== "__main__":
    main()
