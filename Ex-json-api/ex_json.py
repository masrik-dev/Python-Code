import json
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    count=0
    url = input("Enter location: ")
    if len(url) < 1:
        break
    print("Retrieving", url)
    uh = urllib.request.urlopen(url, context=ctx)

    data = uh.read()
    print("Retrieved", len(data), "characters")

    info = json.loads(data)
    print("Count: ", len(info))

    for item in info["comments"]:
        n = int(item["count"])
        count = count + n

    print("Sum: ", count)