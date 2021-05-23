# Project Debater Early Access Program tutorials

This repository contains tutorials that demonstrate the usage of the IBM Project Debater Early Access Program. 

To run these tutorials you will need to request an API key, per the instructions below.

* The tutorial `survey_usecase` demonstrates how to use Project Debater services for analyzing and finding insights in free text survey data. 
* The tutorial `pro_con_customization` demonstrates how to customize the Project Debater services to specific domains and tasks by fine-tuning the model with user provided examples.  In addition to an APIKEY, this tutorial requires a Docker image of the pro-con service of the Debater Early Access Program. Please contact eladv@il.ibm.com for more information.

## Environment setup

In order to run the tutorials, you need an Python Anaconda environment with the Early Access Program SDK installed on it and a Jupyter notebook.

Create a conda env:
`conda create --name <name> python=3.7`

Activate env:
`conda activate <name>`

Get credentials for the Early Access Program site by sending an email to:
project.debater@il.ibm.com

Login to the Project Debater Early Access Program web site:
https://early-access-program.debater.res.ibm.com/

Download and install the Python SDK according to the instructions in:
https://early-access-program.debater.res.ibm.com/download_sdk.html

## Run the tutorial

Clone the tutorial repository:
`git clone https://github.com/IBM/debater-eap-tutorial.git`

Install the required packages:

`cd debater-eap-tutorial`

`pip install -r requirements.txt`

Run Jupyter notebook. replace the APIKEY_PLACE_HOLDER string with your APIKEY. You can get your APIKEY by clicking the API_KEY tab located at the upper bar of the Project Debater Early Access Program website.

`env DEBATER_API_KEY=APIKEY_PLACE_HOLDER jupyter notebook`

Open the tutorial (e.g. click `survey usecase` and the `austin_demo.ipynb`).
