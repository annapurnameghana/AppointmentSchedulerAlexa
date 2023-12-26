# AppointmentSchedulerAlexa
Appointment scheduler using Alexa and AWS Lambda
<br>
4th sem project
<br>
Login in alexa console and aws lambda
<br>
Lambda has the code 
<br>
Integrated AWS Lambda with alexa
<br>
The interaction model is present 
<br>
Test the model :
- invoke the model
- Schedule an appointment
- If the time slot is not available it is known
- If available then the appointment is booked


Refer to this link:
https://youtu.be/hKxPajo1vgI

## First create a skill
- select custom model
- Hosting services: Provision your own
- Template : Start from scratch

## Change invocation name

## create a lambda function
- Author from sratch
- name the function
- change runtime to python

## copy the code and deploy

## add a layer
- create the layers(3)
- add layers
- custom layer
- choose the layer
- select version

## change general configeration 
- change timeout to 30 sec

## integrating aws lambda to alexa
- go to endpoint
- copy skill id
- go to lambda function and add trigger
- select alexa as source and paste the skill id
- copy function ARN and paste at default location

## test by invoking the alexa skill

## create new intent
- enter new intents
- create slots
- enable slot filling by entering prompts and utterances 


