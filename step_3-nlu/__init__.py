# -*- coding: utf-8 -*-
"""This module contains a template MindMeld application"""
from mindmeld import Application

import datetime as dt
import histopy

app = Application(__name__)

__all__ = ['app']


@app.handle(default=True)
def default(request, responder):
    """This is a default handler."""
    responder.reply('Hello there!')

@app.handle(intent='greet')
def greet(request, responder):
    responder.reply('Hello, {name}. Ask me about what happend on a day in history.')
    responder.listen()

@app.handle(intent='on_day')
def on_day(request, responder):
    time_stamp = next((e for e in request.entities if e['type'] == 'sys_time'), None)
    if time_stamp:
        responder.slots['date'] = time_stamp['value']

        date_str = time_stamp['value'][0]['value']
        date_str = date_str.split("T")[0]
        date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d")
        
        happened_on_day = histopy.load_history(date_obj)
        events = histopy.load_events(happened_on_day)
        
        choices = []
        for year, description in events.items():
            choices.append(f"{year}: {description}")
        responder.slots['date'] = date_obj
        #responder.reply("The following event happened on {date}")
        responder.reply(choices)
    else:
        responder.reply(f"Checking what happend")
    responder.listen()