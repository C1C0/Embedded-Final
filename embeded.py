from paho.mqtt import client as mqtt
import pandas
from datetime import datetime
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import AnchoredText
import _thread

datTem = 0
datHum = 0
datPre = 0

datCheckSum = 0
# Getting the current date and time

df = pandas.read_csv('data.csv')


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("outTopicTem")
    client.subscribe("outTopicHum")
    client.subscribe("outTopicPre")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    dataPayload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    print(topic+" "+dataPayload)

    sort(topic, dataPayload)


def sort(topic, payload):
    global datTem
    global datHum
    global datPre
    global datCheckSum
    dt = datetime.now().strftime('%H:%M:%S')

    if topic == "outTopicTem" and datCheckSum == 0:
        datTem = payload
        datCheckSum += 1
    if topic == "outTopicHum" and datCheckSum == 1:
        datHum = payload
        datCheckSum += 1
    if topic == "outTopicPre" and datCheckSum == 2:
        datPre = payload
        datCheckSum = 0
        df.loc[len(df.index)] = [dt, datTem, datHum, datPre]
        df[-20:].to_csv('data.csv', index=None)
        print(df[-20:])



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)



# Create figure for plotting
fig1 = plt.figure()
ax1 = fig1.add_subplot(5, 1, 1)
ax2 = fig1.add_subplot(5, 1, 3)
ax3 = fig1.add_subplot(5, 1, 5)
# This function is called periodically from FuncAnimation
def animate(i):

    df2 = pandas.read_csv('data.csv')
    x = df2["Time"][-20:].tolist()
    y1 = df2["Temperature"][-20:].tolist()
    y2 = df2["Humidity"][-20:].tolist()
    y3 = df2["Preasure"][-20:].tolist()
    
    # Draw x and y lists
    ax1.clear()
    ax2.clear()
    ax3.clear()
    #ax1.plot(x, y, 'm')
    ax1.plot(x, y1, 'b')
    ax2.plot(x, y2, 'g')
    ax3.plot(x, y3, 'm')
    ax1.set_title('Temperature')
    ax1.set_ylabel('°C', rotation=0,labelpad=20)
    ax2.set_title('Humidity')
    ax2.set_ylabel('%', rotation=0,labelpad=20)
    ax3.set_title('Preasure')
    ax3.set_ylabel('hPa', rotation=0,labelpad=20)
    # Format plot
    ax1.tick_params(axis='x', labelrotation=45)
    ax2.tick_params(axis='x', labelrotation=45)
    ax3.tick_params(axis='x', labelrotation=45)
    #plt.subplots_adjust(bottom=0.30)
    anchored_text1 = AnchoredText(df2["Temperature"][-1:].to_string(index=None), loc=2)
    anchored_text2 = AnchoredText(df2["Humidity"][-1:].to_string(index=None), loc=2)
    anchored_text3 = AnchoredText(df2["Preasure"][-1:].to_string(index=None), loc=2)
    ax1.add_artist(anchored_text1)
    ax2.add_artist(anchored_text2)
    ax3.add_artist(anchored_text3)

# Set up plot to call animate() function periodically
ani1 = animation.FuncAnimation(fig1, animate, fargs=(), interval=2000)


# Create two threads as follows
try:
   _thread.start_new_thread( client.loop_forever, () )
except:
    print("Error: unable to start thread")
    
plt.show()
