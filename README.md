# Debater Early Access Program tutorial

This repository contains tutorials that demonstrate the usages of the IBM Debater Early Access Program. 
* The tutorial survey_usecase demonstrates how to use Project Debater services for analyzing and finding insights in free text survey data. It can be used with APIKEY. (In order to get an APIKEY, see instructions below).
* The tutorial pro_con_customization demonstrates how to customize the debater services by fine-tuning, and requires in addition to an APIKEY, a Docker image of the pro-con service of the Debater Early Access Program. Please contact eladv@il.ibm.com for more information.

## Environment setup

In order to run the tutorials, you need an Anaconda environment with the Early Access Program SDK installed on it, and a Jupyter notebook.

Create a conda env:
`conda create --name <name> python=3.7`

Activate env:
`conda activate <name>`

Get credentials for the Early Access Program site by sending an email to:
project.debater@il.ibm.com

Login to Early Access Program site:
https://early-access-program.debater.res.ibm.com/

Download and install SDK via instrcutions at:
https://early-access-program.debater.res.ibm.com/download_sdk.html

## Run the tutorial

Clone the tutrial repository:
`git clone https://github.com/IBM/debater-eap-tutorial.git`

Install requirements

`cd debater-eap-tutorial`

`pip install -r requirements.txt`

Run Jupyter notebook. replace the APIKEY with your APIKEY. You can get your APIKEY by clicking the tab API_KEY at the upper bar. 

`env DEBATER_API_KEY=APIKEY jupyter notebook`

Open the tutorial (e.g. click `survey usecase` and the `austin_demo.ipynb`).
