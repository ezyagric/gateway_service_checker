from flask import Blueprint, make_response, jsonify
from flask_restful import reqparse, Resource, Api
import logging
import os
import requests
from mailjet_rest import Client
import time
from datetime import datetime as date

class Gateway(Resource):
    def __init__(self, **kwargs):
        mail_api_key = os.getenv('MAIL_API_KEY')
        mail_api_secret = os.getenv('MAIL_API_SECRET')
        self.mail_jet = Client(auth=(mail_api_key, mail_api_secret))
    def send_email(self,sender,reciever,subject,text_message, html_message=''):
        # api_key = MAIL_API_KEY
        # api_secret = MAIL_API_SECRET
        # mailjet = Client(auth=(api_key, api_secret))
        data = {
            "FromEmail":  sender,
            "FromName": "EzyAgric",
            "To": reciever,
            "Subject": subject,
            'Text-part': text_message,
            'Html-part': html_message,
        }

        result = self.mail_jet.send.create(data=data)
        print(result.json())
        return result.json()

    def check_gateway_status(self):
        gateway_urls = ["http://35.222.247.11:4985/ezyagric-production/","http://34.71.255.89:4985/ezyagric-production/"]
        for x in gateway_urls:
            try:
                req = requests.get(x)
                
                if req.status_code == 200:
                    data = req.json()
                    if data['state'] == "Online":
                        receivers = os.getenv('RECIEVERS')
                    elif data['state'] == "Offline":
                        receivers = os.getenv('RECIEVERS')
                        senders = "sales@akorion.com"
                        html_message = '''<html><body><p><font face="verdana" color="black">Hi Admin''' '''
                                            <br>
                                            <br>Attention!
                                            <br>
                                            <br>The below gateway
                                            <br>
                                            <br>Gateway URL: '''+ x + '''
                                            <br>
                                            <br>Is in the following state .'''+data['state']+'''
                                            <br>
                                            <br><i>Creating Endless farming possibilities:</i>
                                            <br>
                                            <br>Thanks for choosing EzyAgric
                                            <br><br><br>EzyAgric TechTeam*</font></p></body>
                                            </html>'''

                        self.send_email(senders,receivers,'Your Production Gateway is offline','',html_message)
                    else:
                        receivers = os.getenv('RECIEVERS')
                        senders = "sales@akorion.com"
                        html_message = '''<html><body><p><font face="verdana" color="black">Hi Admin''' '''
                                            <br>
                                            <br>Attention!
                                            <br>
                                            <br>The below gateway
                                            <br>
                                            <br>Gateway URL: '''+ x + '''
                                            <br>
                                            <br>Is in the following state .'''+data['state']+'''
                                            <br>
                                            <br><i>Creating Endless farming possibilities:</i>
                                            <br>
                                            <br>Thanks for choosing EzyAgric
                                            <br><br><br>EzyAgric TechTeam*</font></p></body>
                                            </html>'''

                        self.send_email(senders,receivers,'Your Production Gateway is offline','',html_message)
                    # print("gateway: ",x," Is operational")
                    return {"message":'No action required'}
                else:
                    receivers = os.getenv('RECIEVERS')
                    senders = "sales@akorion.com"
                    html_message = '''<html><body><p><font face="verdana" color="black">Hi Admin''' '''
                                        <br>
                                        <br>Attention!
                                        <br>
                                        <br>The below gateways are unavailable
                                        <br>
                                        <br>Gateway URL: '''+ x + '''
                                        <br>
                                        <br>Please log into the gateway and check logs.
                                        <br>
                                        <br><i>Creating Endless farming possibilities:</i>
                                        <br>
                                        <br>Thanks for choosing EzyAgric
                                        <br><br><br>EzyAgric TechTeam*</font></p></body>
                                        </html>'''

                    self.send_email(senders,receivers,'Your Production Gateway is offline','',html_message)
                    return {"message":'Check complete and notice sent'}

            except requests.exceptions.RequestException as e:
                # print(e)
                receivers = os.getenv('RECIEVERS')
                senders = "sales@akorion.com"
                html_message = '''<html><body><p><font face="verdana" color="black">Hi Admin''' '''
                                    <br>
                                    <br>Attention!
                                    <br>
                                    <br>The below gateways are unavailable
                                    <br>
                                    <br>Gateway URL: '''+ x + '''
                                    <br>
                                    <br>Please log into the gateway and check logs.
                                    <br>
                                    <br><i>Creating Endless farming possibilities:</i>
                                    <br>
                                    <br>Thanks for choosing EzyAgric
                                    <br><br><br>EzyAgric TechTeam*</font></p></body>
                                    </html>'''

                self.send_email(senders,receivers,'Your Production Gateway is offline','',html_message)
                print("am here")
                return {"message":'Check complete and notice sent'}