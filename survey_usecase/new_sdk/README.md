# Key Point Analysis (KPS) tutorials
## Introduction
When you have a large collection of texts representing people’s opinions (such as product reviews, survey answers or posts from social media), it is difficult to understand the key issues that come up in the data. Going over thousands of comments is prohibitively expensive. Existing automated approaches are often limited to identifying recurring phrases or concepts and the overall sentiment toward them, but do not provide detailed or actionable insights.

In this tutorial you will gain hands-on experience in using KPS for analyzing and deriving insights from open-ended answers. The data we will use is a community survey conducted in the city of Austin in the years 2016 and 2017.

## Prerequisites
To follow this tutorial, you first need to receive credentials for KPS APIs by sending a request email to: `yoavka@il.ibm.com`
We also assume you have conda package managment system (https://docs.conda.io/en/latest/) available and basic knowladge in Python.


## Estimated time
It should take about 1 hour to complete the `survey_usecase` tutorial.

## Environment setup
In order to run the tutorials, you need an Python Anaconda environment with the Early Access Program SDK installed on it and a Jupyter notebook.

* Create a conda env:<br />
`conda create --name <name> python=3.11`

* Activate env:<br />
`conda activate <name>`

* Install KPS's Python SDK:<br />
`pip install debater-python-api`
https://pypi.org/project/debater-python-api/

* Install Jupyter Notebook:<br />
`pip install notebook`
https://pypi.org/project/debater-python-api/

* Get an API key for KPS by sending an email to:<br />
`yoavka@il.ibm.com`


## Run the tutorial

* Clone the tutorial repository:<br />
`git clone https://github.com/IBM/debater-eap-tutorial.git`

* Run Jupyter Notebook (use the api-key from the site):<br />
`env KPS_API_KEY=<API_KEY> jupyter notebook`


* Open `survey_usecase/kpa_quick_start_tutorial.ipynb` notebook for a simple quick-start tutorial or `survey_usecase/kpa_quick_start_tutorial-with_results.ipynb` for a version with results.

* The tutorial is self-explanatory, and demonstrates how to use Key Point Summarization and its key features.

* Feel free to contact us if you face problems or have questions at: <br />`yoavka@il.ibm.com`