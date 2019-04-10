import json
from flask import request, Response, make_response
from flask_sqlalchemy import SQLAlchemy

import requests
from config import SLACK_VERIFICATION_TOKEN, SLACK_BOT_USER_TOKEN, MEET_TOKEN,VALUES_TOKEN,SLASH_TOKEN
from app import app 
from models import init_bdd,verif_user
from functions import send_channel, send_direct_message, send_webhook, bot_response
from actions import http_webhook, handle_interactive, handle_event, handle_slashcommand, handle_dialog ,broatcast
from slackclient import SlackClient
import time
import re

#from slackclient import *
#from urllib.parse import parse_qs

@app.route("/bdd", methods=["GET"])
def home():
  init_bdd()
  #verif_user("UG7HJSP5X")
  return make_response("IN BDD")

@app.route('/event',methods=['POST'])
def event():
  #VERIF MESSAGE AUTORISÉ
  words =['meet','/meet','/update','update',"offyvalue","offyvalues",'/offyvalues','user']
 
  slack_message = request.json

  if slack_message.get("challenge"):
    return bot_response(slack_message)

  elif slack_message['event'].get('type')== "team_join":
    handle_event(event)
    

    print(user_info)

  elif slack_message['event'].get('type') == "user_change":
    user_info = slack_message['user']
    print(user_info)
    
  elif slack_message['event'].get('subtypte')== "bot_message":
    return make_response("OK", 200 ,{"content_type":"application/json"})
  
  else:
    eventype = slack_message['event'].get('type')
    eventext = slack_message['event'].get('text')
    event =  slack_message['event']
    #parsetext = re.split('<.*>',' ',t.lower())

    if eventype == "app_mention" and eventext in words:
      #print("WORD:"+ parsetext )
      handle_event(event)

    if eventype == "message" and eventext in words and event['channel_type'] == "im":
      handle_event(event)

  return make_response("", 200 ,{"content_type":"application/json"})


@app.route('/interactive',methods=['POST'])
def interactive():
#request_type = request.content_type 

#if request_type == 'application/x-www-form-urlencoded':
  data = request.form.get('payload')
  payload = json.loads(data)
  
  if payload['token'] == SLACK_VERIFICATION_TOKEN and payload['type'] == "interactive_message":
    http_webhook(payload['response_url'])
    handle_interactive(payload)
  
  elif payload['token'] == SLACK_VERIFICATION_TOKEN and payload['type'] == "dialog_submission":
    handle_dialog(payload)

  elif payload['token'] == SLACK_VERIFICATION_TOKEN and payload['type'] == 'dialog_cancellation':
    handle_dialog(payload)

  return make_response("", 200 ,{"content_type":"application/json"})

@app.route('/slashcommand',methods=['POST','GET'])
def command():
  token_list = (SLACK_COMMAND_TOKEN_LIST)
  data = request.form.to_dict()

  token = data.get('token')
  if token in token_list:
    handle_slashcommand(data)
  return make_response("",200 ,{"content_type":"application/json"})


@app.route("/panning_receive", methods=["GET"])
def planning():
  data = request.json
  planning = Planning()
  add_bdd(planning)
  print("panning comming")
#add value in bdd 

@app.route("/send_broatcast", methods=["GET"])
def broatcast():
  #how send 1 fois le message 
  broatcast()
  return make_response(" ", 200 ,{"content_type":"application/json"}) 
