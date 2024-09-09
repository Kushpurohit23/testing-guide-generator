import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
import json

def getTestLLM(context, screenshots):
    load_dotenv()
    SECRET_KEY = os.getenv('Secret_key')
    genai.configure(api_key=SECRET_KEY)
    if(len(context)==0):context="Not Available"
    print("*"*100)
    print(screenshots,"-"*100)
    image = Image.open(screenshots)
    buffer = io.BytesIO()
    image.save('static/input.png', format='PNG')
    buffer.seek(0)  
    myfile = genai.upload_file('static/input.png')
    # myfile = genai.upload_file(buffer)
    print("*"*100)
    model = genai.GenerativeModel("gemini-1.5-flash",generation_config={"response_mime_type": "application/json"})
    test = 1
    txt = ''
    while test :
        try :
            result = model.generate_content(
            [myfile, "\n\n", """	
                    Additional Context aboout image is : {} """.format(context)+ """
                    
                    You are an expert tester and Quality Assurance Engineer with 10+ Years of experience in domain, now you are given with the task of identifying various features for which testing has to be done before releasing product as an experienced person you find it very precisely. 
            
                    IMPORTANT : You are required to identify each and every component which needs to be tested from image     only.and provide at most 10 most relevent features.
            
                    features give response JSON format {Feature : [note down features here]}
                    here name of key must be Feature.
                    NOTE : ONLY provide feature name no other description
                    
            """])
            print("*"*100)
            txt = json.loads(result.text)
            if(len(txt['Feature']) > 0) : test = 0 
            print("*"*100)
            print(txt)
        except Exception as e :
            print(e)
    lsr = []
    psl = []
    i=0
    for feature in txt['Feature']:
        i+=1
        prommpt = """
                Additional Context aboout image is : {}
                
                You are an expert tester and Quality Assurance Engineer with 10+ Years of experience in domain, you are associated with writing steps for successfully testing an product.

                Now you are provided with task to write step-by-step guide on how to test functionality. 

                Functionality : {} """.format(context,feature) + """

                Based upon image and Functionality write guide as described below.

                ID : the tester will assign a unique identifier to the test case. This allows the tester to recall and identify the test case in the future easily.
                Description: What the test case is about.
                Pre-conditions: What needs to be set up or ensured before testing.
                Testing Steps: Clear, step-by-step instructions on how to perform the test.
                Expected Result: What should happen if the feature works correctly.


                Schema to be follwed for response IN JSON format is

                {
	                ID: "String",
	                Description : "string",
	                preConditions : [List of strings],
	                Steps : [List of strings],
	                ExpectedResults : [List of strings],
	
                }

                Exapmle : {

	                ID : "TC-01: Verify Login Functionality for a User",
	
                    Description: Test for Logging Into the application Given: A valid username and password for the web application When: User enters the username and password in the login page Then: the user should be able to log in to the application successfully. The Home page for the application should be displayed.",
	
	                prepreConditions : [  
	                    "The login page is accessible via the application's URL.",
	                    "The application is running and the server is up.",
	                    "The user has a valid account with registered credentials (username and password).",
	                    "The browser or client application is compatible with the login page.",
	                    "The user’s account is active and not locked or disabled.",
	                    "The login page does not have any critical JavaScript errors or broken links.",
	                    "The user has a stable internet connection.",
	                    "All required fields on the login page (username, password) are present and functional.",
	                    "The login page does not require additional authentication steps beyond username and password."
	                ]
	                Steps  : [
		                "Launch the login application under test.",
		                "Enter a valid username and password in the appropriate fields.",
		                "Click the ‘Login’ button.","Verify that the user has been successfully logged in.",
		                "Log out and check if the user is logged out of the system."
	                ]
	
	                ExpectedResults: [
		                "A user should be able to enter a valid username and password and click the login button.",
		                "The application should authenticate the user’s credentials and grant access to the application.",
		                "The invalid user should not be able to enter the valid username and password; click the login button.",
		                "The application should reject the user’s credentials and display an appropriate error message."
	                ]
    }

        Strictly follow the schema and write each and every part precisely none of the details shold be missed as it impose big financial loss."""
        try:
            result = model.generate_content(
                [myfile, "\n\n",prommpt])
            lsr.append(json.loads(result.text))
            psl.append(prommpt)
        except Exception as e:
            print(e)
    # print("*"*100)
    # print(lsr)
    # print("*"*100)
    return lsr 

    