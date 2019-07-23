#!/usr/bin/python3

import csv
import json
import requests
from time import strftime
from sys import exit

from libbasil_I2C import water, sample_data

CONFIG_PATH = '../basilbot_config.json'

# the default setup.
cfg = json.loads('''{
    auto_measure: {
        active: true,
        num_samples: 10
    },
    auto_water: {
        active: false,
        thresholds: {
            high: 85,
            target: 75,
            low: 60,
            critical: 40
        }
    },
    webhooks: []
}
''')

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

try:
    with open(CONFIG_PATH,'r') as f:
        cfg = json.load(f)
        if not cfg['auto_measure']['active']:
            exit(0)
except FileNotFoundError:
    print('No config file found at %s. Using defaults...' % CONFIG_PATH)

moisture = sample_data(cfg['auto_measure']['num_samples'])

with open("../data/history.csv",'a') as f:
    writer = csv.writer(f)
    writer.writerow([strftime('%Y-%m-%dT%H:%M:%S'), moisture])

if cfg['auto_water']['active']:
    thresh = cfg['auto_water']['thresholds']
    if moisture < thresh['critical']:
        water(255, 60)
        post_discord('**CRITICAL WATER LEVEL!**\n Last recorded moisture: {:.2f}%'.format(moisture))
    elif moisture < thresh['low']:
        post_discord('Automatically watering for 60s. Last recorded moisture: {:.2f}%'.format(moisture))
        water(255, 60)
    elif moisture < thresh['target']:
        post_discord('Automatically watering for 10s. Last recorded moisture: {:.2f}%'.format(moisture))
        water(255, 20)
    elif moisture > thresh['high']:
        post_discord('The soil is verging on too damp. Last recorded moisture: {:.2f}%'.format(moisture))
