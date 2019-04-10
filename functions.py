from config import *

#from models import *
from flask import request, Response, make_response
from slackclient import SlackClient
from flask import request, Response, make_response
import re
from datetime import datetime 
#from actions import handle_interactive



slack_token = SLACK_BOT_USER_TOKEN
sc = SlackClient(slack_token)


def send_channel(channel, message):

    return sc.api_call(
            "chat.postMessage",
            channel=channel,
            username="MatchBot",
            icon_emoji=":robot_face:",
            text=message
    )

def send_direct_message(user_id, message):
    return sc.api_call(
            "chat.postMessage",
            channel=user_id,
            text=message,
            as_user=True,
            username="MatchBOT",
            icon_emoji=":robot_face:"      
    )
     
    
def send_webhook(chan, user, message):
    web = URL_WEBHOOK
    channel = "#"+chan
    user_id = "@"+user
    payload = {
            "channel": channel,
            "username":"CAUSES",
            "text": message,
            "icon_emoji":":robot_face:" 
    }
    response = requests.post(web, data=json.dumps(payload))
    return response

def bot_response(event):
    slack_event = event

    if slack_event['token'] == SLACK_VERIFICATION_TOKEN:

        # verification challenge 
        if "challenge" in slack_event:
            mes = make_response(slack_event['challenge'], 200,{"content_type":"application/json"})

        elif "event" in slack_event:
            event = slack_event['event']
            handle_command(event)
            mes = make_response(slack_event['challenge'], 200,{"content_type":"application/json"})

        else:
            print("Connection failed. Exception traceback printed above.")

    return mes

def handle_command(event):
    #words = re.sub(r'<.*>'," ",event['text'].strip('').lower())

  
    if event['type'] == "app_mention":
        #words = re.sub(r'<.*>'," ",event['text'].strip('').lower())
        #text = "@appmention: "+ text_parse(words) 
        req = handle_interactive("app_mention")
    if event['type'] == "app_mention":
        req = handle_interactive("app_mention")
    
    if event['type'] == "message" and "subtype" not in event:
        # and not "subtype" in event:
        req = send_direct_message(event['channel'],"from localhost")
 
    if  event['type'] == "message" and event['subtype'] == 'bot_message':
        req = make_response(slack_event['challenge'], 200,{"content_type":"application/json"})

    if event['type'] == "interactive_message" and event['actions']['selected_options']['value'] == "yes":
        #verifier ds lq bdd si yser hqve cause si oui math si non ask ses cause
        req = send_direct_message(event['user'],"really ?")
    return req

def handle_message(event):

    #text = "Tword:" + text_parse(event['text'])
      #== 'im' or "channel":
    text = "from locals"
    
    if event['channel_type'] in event and  event['channel_type'] == 'im':
        response = send_direct_message(event['channel'],text)
        
    elif event['channel_type'] in event and  event['channel_type'] == 'channel':
        response = send_direct_message(event['channel'],text)

    else:
        response = send_direct_message(event['channel'],text)
  

    return response

def text_parse(words):
    if "match" in words:
        message = " wait offy match is comming..."
    elif "hello" in words:
        message = " how are you ?"
    elif "test" in words:
        message = " Again"
    else:
        message = words
    return message

def list_users():
    userslist = sc.api_call("users.list")
    members = userslist['members']
    #TO DO CREATE EMPTI LISTE ADD EAUC HUSER INROMATION 
    users = {}
    i = 1
    for user in members:
        user_id = user['id']
        name = user['profile']['real_name']
        slack_name = user['profile']['display_name']
        users[i] = ({1},{2},{3}).format(user_id, name, slack_name)
        #get tuple infromation users[0] ect add to the database
    return users

def run(slack_message):
    slack_client = SlackClient(SLACK_BOT_USER_TOKEN)
    bot_id = slack_client.api_call("auth.test")["user_id"]

    if slack_client.rtm_connect(with_team_state=False):
        print("Successfully connected, listening for events")
        while True:
            events = slack_client.rtm_read()
            for event in events:
                handle_event(event, slack_client, bot_id)
            time.sleep(1)
    else:
        print("Connection Failed")

def parse_userlist():
    offylist = sc.api_call("users.list")
    members = offylist['members']
    userslist = []
    for i in range(len(members)):
        slack_id =  members[i]['id']
        real_name = members[i]['profile']['real_name']
        slack_name =  members[i]['profile']['display_name']
        job = members[i]['profile']['title']
        time = members[i]['updated']
        last_update =  datetime.fromtimestamp(time).strftime("%Y-%m-%d")
        
        if slack_name in ('',None) == True:
            slack_name = real_name
        else : salck_name = slack_name
   
        user = {
            'slack_id':slack_id,
            'real_name': real_name,
            "slack_name":slack_name,
            "last_activity":last_update,
            "job":job,
            "last_match":""
        }
        userslist.append(user)
    return  userslist