#!/usr/bin/env python3
#@author mbhonsle

import argparse
import requests
import json

ORIGIN = "https://{0}"
REFERER_URI = "{0}/chatbots/botBuilder.app"
AURA_UTTERANCE_URL = "{0}/aura"
ACTION_DESCRIPTOR = "serviceComponent://ui.chatbots.components.aura.components.ChatbotIntentController/ACTION$createIntentUtterance"
AURA_CONTEXT_MODE = "PROD"
AURA_CONTEXT_APP = "chatbots:botBuilder"
AURA_PAGE_URI = "/chatbots/botBuilder.app#/bot/dialogs/intent?botId={0}&versionId={1}&dialogId={2}"


class Message:
    def __init__(self, intent_id, utterance, lang):
        self.actions = [
            {
                "id": "541;a",
                "descriptor": ACTION_DESCRIPTOR,
                "callingDescriptor": "UNKNOWN",
                "params": {
                    "utterance": {
                        "intentId": intent_id,
                        "utterance": utterance,
                        "language": lang
                    }
                }
            }
        ]


class AuraContext:
    def __init__(self, fwuid, lid):
        self.mode = AURA_CONTEXT_MODE
        self.fwuid = fwuid
        self.app = AURA_CONTEXT_APP
        self.loaded = {
            "APPLICATION@markup://chatbots:botBuilder": lid
        }
        self.dn = []
        self.globals = {}
        self.uad = True


parser = argparse.ArgumentParser()
parser.add_argument("-domain", dest='domain', help="My domain URI of your org", required=True)
parser.add_argument("-intent-id", dest='intent_id', help="Intent Id from the Aura page", required=True)
parser.add_argument("-lang", dest='lang', help="Bot Language", required=True)
parser.add_argument("-bot_id", dest='bot_id', help="Bot Id", required=True)
parser.add_argument("-bot_version_id", dest='bot_version_id', help="Bot Version Id", required=True)
parser.add_argument("-bot_dialog_id", dest='bot_dialog_id', help="Bot Dialog Id", required=True)
parser.add_argument("-token", dest='token', help="Aura Auth Token", required=True)
parser.add_argument("-sid", dest='sid', help="SID from the Aura UI Cookie", required=True)
parser.add_argument("-utterances", dest='utterances_file', help="Path to the local utterance file", required=True)

parser.add_argument("-fwuid", dest='fwuid', help="FWUID", required=False, default="NWrI6M9Dlk8srW9Z3QqRSA")
parser.add_argument("-lid", dest='lid', help="LID", required=False, default="N1tO5DAu7xvEqgT2o7t4fQ")

args = parser.parse_args()


def upload_utterance(utterance_str):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': ORIGIN.format(args.domain),
        'Referer': REFERER_URI.format(ORIGIN.format(args.domain)),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    params = {
        'r': '18',
        'ui-chatbots-components-aura-components.ChatbotIntent.createIntentUtterance': '1',
    }
    cookies = {"sid": args.sid}
    data = {
        'message': json.dumps(Message(args.intent_id, utterance_str, args.lang).__dict__),
        'aura.context': json.dumps(AuraContext(args.fwuid, args.lid).__dict__),
        'aura.pageURI': AURA_PAGE_URI.format(args.bot_id, args.bot_version_id, args.bot_dialog_id),
        'aura.token': args.token
    }
    res = requests.post(
        AURA_UTTERANCE_URL.format(ORIGIN.format(args.domain)),
        params=params,
        cookies=cookies,
        headers=headers,
        data=data
    )
    print(res)


def upload():
    with open(args.utterances_file) as file:
        for line in file:
            upload_utterance(line)


if __name__ == "__main__":
    upload()
