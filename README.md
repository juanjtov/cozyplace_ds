![](https://i.imgur.com/jvR9cyz.png)
# Cozy Place - Data Science

Platform where you can upload recommendations of places to visit and experiences to explore. As well as, look for the activities you wanna do in your next vacations.

## About the API 
- The goal of this REST API  is to scrape different travel companies and get the most popular acitivties to do in COLOMBIA and MEXICO.
-  The backend make the requests to the API through the end points and the API give a JSON response to it including every detail for each activity.


## Settings
- Clone the current repository through the following command:
       git clone https://github.com/juanjtov/cozyplace_ds.git

- You will need  create the venv:
        python3 -m venv dsenv

- Activate the environment:
		source activate venv/bin/activate	
- Install the required libraries:
		pip install -r requirements.txt	

## DEPLOYMENT
- To deploy the API locally:
		uvicorn main:app --reload	
- The API was deployed using APP ENGINE from GCloud in the following link:
**http://cozyplace-294100.wl.r.appspot.com/
**

## API Documentation
You can find [HERE](http://cozyplace-294100.wl.r.appspot.com/docs#/) the documentation for every endpoint in the API.

## LICENSE
This project has the [MIT](https://choosealicense.com/licenses/mit/) license.




                
----
