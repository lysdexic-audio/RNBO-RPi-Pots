from gpiozero import MCP3008
from pythonosc import udp_client
import time

# send all messages to port 1234 on the local machine
client = udp_client.SimpleUDPClient("127.0.0.1", 1234)

# start the transport via OSC
client.send_message("/rnbo/jack/transport/rolling", 1)

# read from last two channels
potA = MCP3008(channel=6)
potB = MCP3008(channel=7)

try:
    while True:
        cutoff = potA.value
        res = potB.value
        print(f"PotA: {cutoff:.3f} PotB: {res:.3f} (Ctrl-C to exit)")
        client.send_message("/rnbo/inst/0/params/cutoff/normalized", cutoff)
        client.send_message("/rnbo/inst/0/params/resonance", res)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Exiting...")
