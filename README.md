# DNA-Microsoft-Teams-Assurance-Bot.py

*This code is created for Cisco DNA Center and Microsoft Teams.*

*The included tutorial(s) will use Postman and Microsoft BotFramework Emulator; no DNA Center appliance needed!*
---

## Purpose
**The purpose of this code is to leverage a Microsoft Teams bot to receive proactive DNA Center Assurance alerts**

The tutorial for this code will allow you to validate that your Microsoft Teams bot displays your Assurance data properly as [Adaptive Cards](https://adaptivecards.io/).

You can try testing this code by **reserving** the [Cisco DevNet Sandbox for DNA Center 2.1.2.5](https://devnetsandbox.cisco.com/) -- please note, you cannot test with the **always-on** sandbox, because it does not offer adequate permissions to modify API Events.

Even better, you can try testing this with an actual DNA Center appliance.

If you do not have access to the Cisco DevNet sandbox environment or a physical DNA Center deployment, the tutorials provided below will allow you to test this bot with actual .json data from DNA Center Assurance events(using Postman).

### Intended Audience
**This code is intended for network engineers who manage DNA Center and use Microsoft Teams for collaboration, and want to improve their alerting and monitoring on the Cisco SD-Access fabric.**

Typically, DNA Center Assurance alerts are self-contained within the DNA Center GUI, which means you have to login to DNA Center and select the Assurance tab. This is not ideal and can prevent you from being notified from critial P1 alerts in your SD-Access topology.

This code intends to solve this issue by integrating DNA Center's Event API with Microsoft Teams. With this code, you can receive alerts as they occur in real-time. You proactive Microsoft Teams bot will alert you to Assurance events as soon as they appear.

Even better, your entire team can be alerted to Assurance events on their mobile phone or laptop using the Microsoft Teams app! Never miss a critial infrastructure alert ever again!

## How This Code Works
This code intends to accomplish the following tasks:
1. Listen for DNA Center's Event API POST requests on the URL https://localhost:3978/api/assurance
2. Populate the POST data into an [Adaptive Card](https://adaptivecards.io/) consisting of .json data.
3. Display the Adaptive Card(s) in Microsoft BotFramework Emulator, including the following info:
    - Assurance Issue Name
    - Assurance Issue Details
    - Assurance Issue Prioirty
    - Assurance Issue Category
    - Assurance Issue Status
    - Device Name

## Prerequisites
1. Microsoft Windows OS (for the BotFramework Emulator)
2. [Postman](https://www.postman.com/downloads/) installed
3. [Microsoft BotFramework Emulator](https://github.com/microsoft/BotFramework-Emulator) installed
4. [Python](https://www.python.org/downloads/) installed on your local machine.
5. [pip](https://packaging.python.org/tutorials/installing-packages/) installed for Python

## Installation Steps
1. Clone this repository from a **PowerShell** terminal:
`git clone https://github.com/james-sciortino/dna-teams-assurance-bot`

2. Navigate into the directory:
`cd dna-teams-assurance-bot`

3. Install the required dependencies specified in [requirements.txt](requirements.txt) from the <dna-get-interface-report> folder:
`pip3 install -r requirements.txt`

5. Run the code from your cloned git repository:
`python app.py`

6. When you see the following output in your PowerShell terminal, the application is running successfully:
```console
======== Running on https://0.0.0.0:3978 ========
(Press CTRL+C to quit)
```

## Tutorial
1. Complete the installation steps listed above and be sure your bot is listening on TCP 3978
2. Verify [Postman](https://www.postman.com/downloads/) and [Microsoft BotFramework Emulator](https://github.com/microsoft/BotFramework-Emulator) are installed and working on your Windows OS.
3. Open Microsoft BotFramework Emulator, select **File > Open Bot** and enter the following URL:
```console
https://localhost:3978/api/messages
```
![Botframework Setup](images/BotFramework.gif "Botframework Setup")

4. Open Postman and send an HTTP POST request with the following information:
    - HTTP Request: **POST**
    - HTTP URI: **https://localhost:3978/api/assurance**
    - Content-Type: **application/json**
    - Body: Select **Selct *raw*, then copy-paste the .json data from the [example.json](resources/example.json) file included in this repository!**
![Postman Setup](images/Postman.gif "Postman Setup")

5. View the P1 Assurance alert in the Microsoft BotFramework Emulator:
![Assurance P1](images/Assurance-P1.gif "Assurance P1")

### Additional Info
This code includes conditional logic to display color-coded alerts:
* Active P1 Alerts = Red
* Active P2 Alerts = Orange
* Active P3 Alerts = Green
* Resolved Alerts = Green

**Active P2 Assurance Alerts will display with an Orange theme!**

Modify the key-value for **"Assurance Issue Status"** to a **"P2"** in your [example.json](resources/example.json) data (the payload of your POST request).
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
When this payload is sent to your Microsoft Teams bot...
![Assurance P2](images/Assurance-P2.gif "Assurance P2")

**Resolved Assurance events (of any priority) will display with a green theme!**

Modify the key-value for **"Assurance Issue Status"** to **"resolved"** in your [example.json](resources/example.json) data (the payload of your POST request).
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
When this payload is sent to your Microsoft Teams bot...
![Assurance Resolved](images/Assurance-Resolved.gif "Assurance Resolved")

### Configuring DNA Center
If you have access to a DNA Center appliance, perform the following steps to configure the Event API for Assurance alerts:

1. Login to the DNA Center GUI
2. Navigate to the ______ tab.
3. Select one or more events.
4. Select
5. 

### Ready for Deployment
Follow Microsoft's [guide](https://docs.microsoft.com/en-us/microsoftteams/platform/get-started/first-app-bot?tabs=vscode) to deploy your bot to Microsoft Teams!

### FAQ 
1. What is the purpose of each file?
    - [app.py](app.py) -  Primary code. This is the file you execute to run this code. 

### Authors
Please contact me with questions or comments.
- James Sciortino - james.sciortino@outlook.com

# License
This project is licensed under the terms of the MIT License.
