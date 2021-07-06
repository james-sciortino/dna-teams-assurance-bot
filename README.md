# DNA-Microsoft-Teams-Assurance-Bot.py

*This code is created for the Cisco DNA Center and Microsoft Teams platforms.*
*The tutorial for this code will use Postman and Microsoft BotFramework Emulator for immediate functionality testing*
---

# Purpose
**The purpose of this code is to leverage a Microsoft Teams bot to receive proactive DNA Center Assurance alerts**
*NOTE: This code is for demonstration purposes only!*
The tutorial for this code will allow you to validate the Microsoft Teams bot displays your Assurance data properly as [Adaptive Cards](https://adaptivecards.io/).
Unfortunately, you cannot use the alwyas-on DNA Center appliance for testing, because you cannot modify API alerts. 
*You will need access to your own DNA Center appliance if you want to test this with a DNA Center deployment.*

# Intended Audience
**This code is intended for network engineers who manage DNA Center and use Microsoft Teams for collaboration, and want to improve their alerting and monitoring on the Cisco SD-Access fabric.**
Typically, DNA Center Assurance alerts are self-contained within the DNA Center GUI, which means you have to login to DNA Center and select the Assurance tab. This is not ideal.
To work around this issue, and to be sure you receive alerts as they occur, you can use a proactive Microsoft Teams bot to alert you of Assurance events.
If you deploy this bot into your Microsoft Teams enviornment, you can receive Assurance alerts on your mobile phone Teams app!

# How This Code Works
This code intends to accomplish the following tasks:
1. Listen for DNA Center API POST messages on the URL https://localhost:3978/api/assurance
2. Populate the POST data into an [Adaptive Card](https://adaptivecards.io/) of .json data.
3. Display the Adaptive Card(s) in Microsoft BotFramework Emulator, including the following info:
 - Assurance Issue Name
 - Assurance Issue Details
 - Assurance Issue Prioirty
 - Assurance Issue Category
 - Assurance Issue Status
 - Device Name

# Prerequesites
1. Microsoft Windows OS (for the BotFramework Emulator)
2. [Postman](https://www.postman.com/downloads/) installed
3. [Microsoft BotFramework Emulator](https://github.com/microsoft/BotFramework-Emulator) installed
4. [Python](https://www.python.org/downloads/) installed on your local machine.
5. [pip](https://packaging.python.org/tutorials/installing-packages/) is installed for Python

# Installation Steps
**PowerShell**
2. Clone this repository from a bash terminal:
```console
git clone https://github.com/james-sciortino/dna-teams-assurance-bot
```
2. Navigate into the directory:
```console
cd dna-teams-assurance-bot
```
3. Install the required dependencies specified in [requirements.txt](requirements.txt) from the <dna-get-interface-report> folder:
```console
pip3 install -r requirements.txt 
```
5. Run the code from your cloned git repository:
```console
python app.py
```
6. When you see the following output in your PowerShell terminal, the application is running successfully:
```console
======== Running on https://0.0.0.0:3978 ========
(Press CTRL+C to quit)
```

# Tutorial
1. Complete the installation steps listed above and be sure your bot is listening on TCP 3978
```console
======== Running on https://0.0.0.0:3978 ========
(Press CTRL+C to quit)
```
2. Verify [Postman](https://www.postman.com/downloads/) and [Microsoft BotFramework Emulator](https://github.com/microsoft/BotFramework-Emulator) are installed and working on your Windows OS.
3. Open Microsoft BotFramework Emulator, select **File > Open Bot** and enter the following URL:
```console
https://localhost:3978/api/messages
```
![Botframework Setup](images/BotFramework.gif "Botframework Setup")

4. Open Postman. Send a POST request with the following information:
 - HTTP Request: POST
 - HTTP URI: https://localhost:3978/api/assurance
 - Content-Type: application/json
 - Body: Select **raw** type and copy-paste the .json data from the example.json file included in this repository.
![Postman Setup](images/Postman.gif "Postman Setup")

5. View the P1 Assurance alert in the Microsoft BotFramework Emulator:
![Assurance P1](images/Assurance-P1.gif "Assurance P1")


# Additional Tutorials
Want to see how a Priority 2 or Priority 3 Assurance event will be displayed?
Or, want to see what happens when an Assurance event is resolved?
Modify the key-value for Assurance Issue Status in your .json data (in the body of your Postman POST request):

**Active Priority 2 Assurance will display a yellow theme**
Want to see what happens when an Assurance event is a Priority 2 or Priority 3?
Modify the key-value for *Assurance Issue Priority*  to *P2* in your .json data (in the body of your Postman POST request):
```console
    {
        "Type": "Network Device", 
        "Assurance Issue Details":"AP AP-Test-3 went down", 
        "Assurance Issue Priority": "P2", 
        "Device": "AP-Test-3", 
        "Assurance Issue Name": "AP AP-Test-3 went down", 
        "Assurance Issue Category": "availability", 
        "Assurance Issue Status": "active"
    },             
```
![Assurance P2](images/Assurance-P2.gif "Assurance P2")

**Resolved Priority 2 Assurance events will display in green theme**
Want to see what happens when an Assurance event is resolved?
Modify the key-value for *Assurance Issue Status* to *active* in your .json data (in the body of your Postman POST request):
# Tutorial for Active Priority 2 Assurance Event
```console
    {
        "Type": "Network Device", 
        "Assurance Issue Details":"AP AP-Test-3 went down", 
        "Assurance Issue Priority": "P2", 
        "Device": "AP-Test-3", 
        "Assurance Issue Name": "AP AP-Test-3 went down", 
        "Assurance Issue Category": "availability", 
        "Assurance Issue Status": "resolved"
    },             
```
![Assurance Resolved](images/Assurance-Resolved.gif "Assurance Resolved")
# FAQ 
1. What is the purpose of each file?
    - [app.py](app.py) -  Primary code. This is the file you execute to run this code. 


# Authors
Please contact me with questions or comments.
- James Sciortino - james.sciortino@outlook.com

# License
This project is licensed under the terms of the MIT License.
