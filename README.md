# Project: Log Analysis

Backend SQL project for Udacity full stack nanodegree.

## Software Requirements

Python 3 is needed for this application 

## Installing the Application

Clone or download from github

## Running the Application

**To download the database schema:**

[Download and unzip this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

**Loading the data:**

cd into the log-analysis-project directory, if not already there.

Then run the following command:

`psql -d news -f newsdata.sql`

**To execute log_analysis.py**

from inside the log-analysis-project directory, run the following command:

If only python 3 is installed:

`python log_analysis.py`

If both python 2 and 3 are installed:

`python3 log_analysis.py`

