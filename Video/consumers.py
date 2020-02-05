from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
import os
import numpy
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
import tensorflow
import tflearn
import random
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        call=text_data_json['call']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'call':call
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        call=event['call']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'call':call
        }))
    #  add 
    # - in receive: call=(29)/call:call(36)
    # - chat_message: call=(44)/call:call(49)

class ChatConsumerBot(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        response=chat(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'response': response
        }))

######### Open file json#########
with open('/home/klapeers17/Documents/prime/Chat/Video/static/intents.json') as file:
        data = json.load(file)

######### Use nltk stem lancaster 
stemmer = LancasterStemmer()

######### variable  pour les entrees du fichier json
words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents']:
    print(intent)
    for pattern in intent['patterns']:
        wrds=nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent['tag'])
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words=[stemmer.stem(w.lower()) for w in words if w != "?"]
words= sorted(list(set(words)))

labels = sorted(labels)

training = []
output=[]
out_empty=[0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag=[]
    wrds=[stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row=out_empty[:]
    output_row[labels.index(docs_y[x])]=1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output= numpy.array(output)

tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

#try:
#model.load("model.tflearn")
#except:
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i]=1
    return numpy.array(bag)

def chat(quest):
    response=""
    while True:
        if quest.lower()=="stop":
            resp="Bye"
        else:
            results = model.predict([bag_of_words(quest, words)])
            results_index = numpy.argmax(results)
            tag = labels[results_index]
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    response = tg['responses']

            resp=random.choice(response)
        return resp



