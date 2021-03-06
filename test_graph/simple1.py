import paho.mqtt.client as mqtt
import time

brokers = ["127.0.0.1", "192.168.0.32"]
port = 9001

client1 = mqtt.Client("client_py1", clean_session=True, userdata=None, transport="websockets")
client2 = mqtt.Client("client_py2", clean_session=True, userdata=None)

client1.connect(brokers[0], port)
client1.loop_start()

time.sleep(1)

client2.connect(brokers[1], 1883)
client2.loop_start()

print("pub")
client1.publish("test/publish/py", "string of characters")
time.sleep(1)

print("pub")
client2.publish("hi/test1", "hi")
time.sleep(1)

print("sub")
client1.subscribe("hi/test1", 1)
time.sleep(1)

print("sub")
client2.subscribe("test/publish/py")
time.sleep(1)

print("sub")
client1.subscribe("test/+/py")
time.sleep(1)

print("unsub")
client1.unsubscribe("test/publish/py")
time.sleep(1)

print("pub")
client1.publish("test1/publish/js", "on", retain=False)
time.sleep(1)

print("sub")
client1.subscribe("test1/+/js")
time.sleep(1)

print("sub")
client2.subscribe("+/publish/js", 2)
time.sleep(1)

print("pub")
client1.publish("test1/publish/js", "on", retain=False)
time.sleep(1)

print("sub")
client2.subscribe("test1/#", 1)
time.sleep(1)

print("unsub")
client1.unsubscribe("+/+/py")
time.sleep(1)

client2.disconnect()
client2.loop_stop()

time.sleep(1)

client1.disconnect()
client1.loop_stop()
