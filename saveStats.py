#!/usr/bin/python3
from libbasil_I2C import water, sample_data
from libbasil_history import setHistory
from config import config as cfg
import requests
import json

def post_webhook(url, msg):
    data = {}
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = msg
    data["username"] = "Basilbot"

    result = requests.post(url, data=json.dumps(msg), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def post_discord(msg):
    for url in cfg['webhooks']:
        post_webhook(url, msg)

moisture = sample_data(cfg['auto_measure']['num_samples'])

setHistory(moisture)

if cfg['auto_water']['active']:
    thresh = cfg['auto_water']['thresholds']
    if moisture < thresh['critical']:
        water(255, 60)
        post_discord('**CRITICAL WATER LEVEL!**\n Last recorded moisture: {:.2f}%'.format(moisture))
    elif moisture < thresh['low']:
        water(255, 60)
        post_discord('Automatically watering for 60s. Last recorded moisture: {:.2f}%'.format(moisture))
    elif moisture < thresh['target']:
        water(255, 20)
        post_discord('Automatically watering for 10s. Last recorded moisture: {:.2f}%'.format(moisture))
    elif moisture > thresh['high']:
        post_discord('The soil is verging on too damp. Last recorded moisture: {:.2f}%'.format(moisture))
