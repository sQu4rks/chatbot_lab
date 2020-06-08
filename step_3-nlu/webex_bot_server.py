import os

from mindmeld.components import NaturalLanguageProcessor
from mindmeld.bot import WebexBotServer
from mindmeld import configure_logs

if __name__ == '__main__':
   # Create web hook here: https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook
   WEBHOOK_ID = os.environ.get('WEBHOOK_ID')

   # Create bot access token here: https://developer.webex.com/my-apps/new
   ACCESS_TOKEN = os.environ.get('BOT_ACCESS_TOKEN')

   configure_logs()
   nlp = NaturalLanguageProcessor('.')
   nlp.build()

   server = WebexBotServer(name=__name__, app_path='.', nlp=nlp, webhook_id=WEBHOOK_ID,
                           access_token=ACCESS_TOKEN)

   port_number = 8080
   print('Running server on port {}...'.format(port_number))

   server.run(host='localhost', port=port_number)
