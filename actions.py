import json 
from flask import request, Response, make_response
import requests
from attachements import attachements, offyvalues
from dialog import get_dialog
from time import sleep
from models import User, Cause, add_bdd, add_user_cause
from functions import sc, send_direct_message, parse_userlist
from datetime import datetime

def http_webhook(url_response):
    web = url_response
    payload = {
            "status":'200 OK',
            "Content-type":"application/json"
    }
    response = requests.post(web, data=json.dumps(payload))
    return response

def handle_slashcommand(data):
    user_id = data.get('user_id')
    channel =data.get('channel_id')
    command = data.get('command')
    response_url = data.get('response_url')

    if command == "/offyvalues":
        attachements_send(attachements['firstmessage'], user_id)
        print("IN /OFFYVALUE")

    elif command == "/meet":
        attachements_send(attachements['match'], user_id)
        print("IN /MEET")

    elif command == "/updatevalue":
        attachements_send(attachements['update'], user_id)
    
    elif command == "/planning":
        #req in bdd planning send message
        message = ""
        web = URL_WEBHOOK
        channel = "#"+channel
        payload = {
            "channel": channel,
            "username":"PLANNING",
            "text": message,
            "icon_emoji":":robot_face:" 
        }
        return requests.post(web, data=json.dumps(payload))

    
    return make_response(" ", 200 ,{"content_type":"application/json"})

def handle_interactive(payload):
    user_id =  payload['user']['id']
    channel = payload['channel']['id']
    message_ts = payload['message_ts']
    callback_id = payload['callback_id']
    value = payload['actions'][0].get('value')
    trigger_id = payload.get('trigger_id')

    if callback_id == "formcauses" or callback_id == "fristquestion" and value == "Enregister":
        dialog = get_dialog("fromcauses")
        dialog_send(dialog['askcauses'],trigger_id)

    elif callback_id == "update" and value == "update":
        dialog = get_dialog("update")
        dialog_send(dialog['askcauses'],trigger_id)

    elif callback_id == "confirmform" and value == "oui":
        #add bdd 
        attachements_send(attachements['match'], user_id)

    elif callback_id == "confirmform" and value == "non":
        dialog = get_dialog("update")
        dialog_send(dialog['askcauses'],trigger_id) 

    elif callback_id == "match":
            print("MAKE A MATCH")
           
    return make_response("", 200 ,{"content_type":"application/json"})

def handle_dialog(payload):
    callback_id = payload['callback_id']
    user_id = payload['user']['id']
    action_ts = payload['action_ts']
    #UPDATE USER LAST ACTIVITY
     
    if callback_id == "fromcauses" and payload['type'] == 'dialog_cancellation':
        send_direct_message(user_id,"Qu'attends-tu pour enter tes cause ?")
        attachements_send(attachements['enregister'], user_id)
    
    elif callback_id == "fromcauses" and payload['type'] == 'dialog_submission':
        print(" TO DATA BASE PROCESS ")
        user = user_info(user_id)
        parse_submit(payload['submission'], user_id)

    elif callback_id  == "update" and  payload['type'] =='dialog_cancellation':
        user = user_info(user_id)
        send_direct_message(user_id, "Tes causes n'ont pas été mis à jour")
        #SENS MESSAGE FEET BAC BIEN UPDATE NOW CAN MATCH
    elif callback_id  == "update" and  payload['type'] == 'dialog_submission' :
        # VERIF SI BIEN ENTERE
        user = user_info(user_id)
        parse_submit(payload['submission'], user_id)

    make_response(" ", 200 ,{"content_type":"application/json"}) 

def handle_event(event):
    user_id = event['user']
    eventype = event['type']
    eventext = event['text']
    #re.sub(r'<.*>'," ",event['text'].strip('').lower())
    time = event['event_ts']

    if eventype == "app_mention" or eventype =="message" and  eventext == 'user':
        broatcast()
    
    elif eventype == "app_mention" or eventype =="message" and  eventext in ("offyvalues","offyvalue",'/offyvalues'):
        attachements_send(attachements['firstmessage'], user_id)

    elif eventype == "app_mention" or eventype =="message" and eventext in ("meet","match") :
        attachements_send(attachements['match'], user_id)

    elif eventype == "app_mention" or eventype =="message" and eventext == "update":
        attachements_send(attachements['update'], user_id)
    
    elif eventype == "team_join":
        user = event['user']
        user_id = user['slack_id']
        attachements_send(attachements['firstmessage'], user_id)

    
    return make_response(" ", 200 ,{"content_type":"application/json"}) 



def validate_attchements(text, channel, message_ts):
    return sc.api_call(
        "chat.update",
        channel=channel,
        text=" ",
        as_user=True,
        ts=message_ts,
        attachments=[{	 
            "fallback": "validate actions response",
            "text": text,
            "attachment_type": "default",
            "color": "good"
        }] 
    )
                
def attachements_send(atcvalues, channel):
    return sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=" ",
        as_user=True,
        username="MatchBOT",
        icon_emoji=":robot_face:",
        attachments=atcvalues     
    )
def dialog_send(dialogvalue, trigger_id):
    return sc.api_call(
        "dialog.open",
        dialog=dialogvalue,
        trigger_id=trigger_id   
    )

def user_info(user_id):
    user_info = sc.api_call(
        "users.info",
        user=user_id  
    )
    user = user_info['user']
    activity = datetime.now().strftime("%Y-%m-%d")
    slack_id =  user['id']
    real_name = user['profile']['real_name']
    slack_name = user['profile']['display_name']
    job = user['profile']['title']
    time = user['updated']
    last_update =  datetime.fromtimestamp(time).strftime("%Y-%m-%d")

    if slack_name == '':
        slack_name = real_name
    else :
        salck_name = slack_name
    user = {
        'slack_id':slack_id,
        'real_name': real_name,
        "slack_name":slack_name,
        "last_activity":last_update,
        "job":job
    }

    return user

def confirm_form(text):
    mes =  [
		{
		 	"fallback": "find match",
            "callback_id": "confirmform",
            "title":"Merci d'avoir entrer tes causes ",
            "text":text,
            "color": "primary", 
            "actions":[
                {
                    "name": "oui",
                    "text": "Enregister",
                    "type": "button",
                    "value": "oui",
					"style":"primary"
                },
                {
                    "name": "non",
                    "text": "Modifier",
                    "type": "button",
                    "value": "non",
					"style":"primary"
                }
            ]  
        }		
    ]
    return mes

def parse_submit(causes,user_id):
    listcauses =[]
    for c in causes:
        if causes[c] == "1":
            listcauses.append(c)
        #ADD BDD USER CAUSE
    if len(listcauses) == 1:
        text = "Ta cause est : \n:white_check_mark: "+ offyvalues[listcauses[0]] 

    else:
        text = "Tes causes sont : \n"
        for c in listcauses :
            text = text +"\n:white_check_mark: "+ offyvalues[c]
  
    att = confirm_form(text) 
    return attachements_send(att,user_id)

def match():
    """ send match instruction"""
 
    add = add_values_bdd(user_values)
    resp = sc.api_call(
            "chat.postMessage",
            channel=user_id,
            text=" ",
            as_user=True,
            username="MatchBOT",
            icon_emoji=":robot_face:",
            attachments=add     
    )
    return resp

def broatcast():
    userslist = parse_userlist()
    for user in userslist:
        user_id  = user['slack_id']   
        attachements_send(attachements['firstmessage'],user_id)