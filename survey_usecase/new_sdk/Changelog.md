# Changelog

All notable changes to the KPS service starting from 2023-June-26 will be documented in this file.

## 2023-June-26
SDK version upgraded.
The current backend version supports both new and old versions of the SDK, so for now you can keep using the old one.
In a month (26.7) the legacy version will no longer be supported.

Install the new version by:<br />
`pip install debater-python-api`

Install the old version by:<br />
`pip install debater-python-api==4.3.2`


A link to the full tutorial of the new SDK is available here: https://github.com/IBM/debater-eap-tutorial/blob/main/survey_usecase/new_sdk/kpa_quick_start_tutorial-with_results.ipynb

A link to a lecture covering the tutorial is available here: https://ibm.box.com/s/61kwk9s8d7sm510kd2yz16g8hloufini

The new SDK has all the capabilities of the legacy SDK and more, with many (but mostly straight forward) API changes.
Our main goals were to simplify the API as much as possible while still allowing flexibility for advanced users, and to allow more analysis options over the results.

The main changes are:
* KPA is now called KPS.
* The results are now kept as a KpsResult object, that can be saved and loaded to a json file, and allows for more analysis options. The same reports as before can be generated from this object, and they are organized better and contain more information.
* The run_params and domain_params lists have been modified and shortened. We wanted to let you decide on the final required results, without having to deal with guessing numerical thresholds and other internal parameters which are now tuned internally. The updated lists are available in: https://github.com/IBM/debater-eap-tutorial/blob/main/survey_usecase/new_sdk/kps_parameters.pdf .
* Stance handling is different and simpler: we’re now supporting two stances: Pro (positive sentences) and Con (negative sentences and suggestion). It’s also possible to run without stance or to let the system to run on each stance separately and provide the merged results. You can still see the category of each sentence (pos/neg/sug/neut) in the full results.
* Supporting different running modes: by default, the system now runs in a synchronous manner. It’s also possible to run in an asynchronous manner as before, or to run end to end by only providing the comments (without caching and customization).


