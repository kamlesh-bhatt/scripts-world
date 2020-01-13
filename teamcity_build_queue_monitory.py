import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import time

URL = "https://myteamcitydomain/app/rest/"
AUTH = HTTPBasicAuth('myusername', 'mypassword')


def getBuildQueue():
    print("Fetching Build Queue....")
    request = requests.get(
        URL + "buildQueue", auth=AUTH)
    print(request)
    build_queue = ET.fromstring(request.content)
    for child in build_queue.iter('build'):
        print(child.attrib['buildTypeId'] + " is in build queue..")
        getBuildAgent(child.attrib['buildTypeId'])


def getBuildAgent(BuildTypeId):
    _buildAgentRequest = requests.get(
        URL + "buildTypes/" + BuildTypeId, auth=AUTH)
    _buildAgent = ET.fromstring(_buildAgentRequest.content)
    for child in _buildAgent.iter('agent-requirement'):
        for agent in child.iter('property'):
            # print(agent.attrib['value'])
            matchAgentName(agent.attrib['value'])


def matchAgentName(AgentName):
    print("Finding Compatible Agents for the build to run..")
    _agents = requests.get(
        URL + "agents?locator=connected:true,authorized:any", auth=AUTH)
    _agentNames = ET.fromstring(_agents.content)
    for child in _agentNames.iter('agents'):
        for bagent in child.iter('agent'):
            print(bagent.attrib['name'])
            if bagent.attrib['name'] == AgentName:
                print("Inside...")
                print("Build is compatible to run on agent : " +
                      bagent.attrib['name'])
                checkIfAgentAuthorized(bagent.attrib['id'])


def checkIfAgentAuthorized(agentID):
    print("Checking if Agent is Authorized...")
    _isAgentAuthorized = requests.get(
        URL + "agents/id:" + agentID, auth=AUTH)
    _authorizeStatus = ET.fromstring(_isAgentAuthorized.content)
    for child in _authorizeStatus.iter('agent'):
        if child.attrib['authorized'] == "false":
            print("Agent Not Authorized....")
            AuthorizeAgent(agentID)


def AuthorizeAgent(agentId):
    print("Checking if Agent can be authorized...")
    _enableAgent = requests.put(URL + "agents/id:" + agentId + "/authorized", auth=AUTH,
                                data="true")
    if _enableAgent.status_code == 500:
        checkifBuildRunning()
    else:
        print("Successfully Authorized Agent...")

def checkifBuildRunning():
    print("Finding Agents with no builds running...")
    _agents = requests.get(
        URL + "agents?locator=connected:true,authorized:any", auth=AUTH)
    _agentNames = ET.fromstring(_agents.content)
    for running in _agentNames.iter('agent'):
        for buildRunningAgents in running.attrib['id']:
            runagent = requests.get(
                URL + "agents/id:" + buildRunningAgents, auth=AUTH)
            _isrunning = ET.fromstring(runagent.content)
            runnning_build = _isrunning.find('build')
            if runnning_build is None:
                print("No Build Running")
                for agents in _isrunning.iter('agent'):
                    print("un authorizing agent : ", agents.attrib['name'])
                    # unAuthorizeAgent(agents.attrib['id'])
                    unauthorized_agent(
                        agents.attrib['id'], agents.attrib['name'])
            else:
                print("waiting build to finish........")


def unauthorized_agent(agentid, agentname):
    _unauthorizeAgent = requests.put(URL + "agents/id:" + agentid + "/authorized",
                                     auth=AUTH, data="false")
    print("Successfully UnAuthorized agent: " + agentname)


while('true'):
    print("-------------------")
    time.sleep(20)
    KeyboardInterrupt
    getBuildQueue()

