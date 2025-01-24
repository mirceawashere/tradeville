# TRADEVILLE API TO GOOGLE SHEETS

## the idea behind time. why?

I wanted an overview of my investments from Tradeville in a Google spreadsheet. The problem is that Google App Script cannot directly connect using websockets (and Tradeville API only allows websockets). So using my limited knowledge what I thought about doing was to set up a Flask sever to get the value from the Tradeville API and return the value (using its own API) to Google App Script. 

## overview

So what I did was:
1. write a [PY script](https://github.com/mirceawashere/tradeville/blob/main/tradeville.py) to connect to the [Tradeville API](https://api.tradeville.ro/) to provide the portfolio value.
   While I could have made it more complex, I was only honestly interested in the first asset's total value, that’s why I used `[0]` + at the end of the day, I wanted a numbered value to populate a cell sheet with.
2. use that PY script in conjunction with a Flask server running on the free version from [render](https://render.com/) 
   The idea was for my PY script to connect to the Tradeville API and for the Google App Script to extract the value from my own API, running on the Flask server. 
3. made a [JS script](https://github.com/mirceawashere/tradeville/blob/main/google_script.js) and uploaded it in Google App Script that connected to my Flask server

that’s about it. 

## things to keep in mind

### render - settings

you need to set up the following **environment variables**: 
```
FLASK_APP= {name of PY script}
TRADEVILLE_PASSWORD= you get it
TRADEVILLE_USER= ...
```

- **build command**: `pip install -r requirements.txt` - you can get the file/contents from [here](https://github.com/mirceawashere/tradeville/blob/main/requirements.txt) 
- **start command**: `gunicorn {name of your PY script}:app`


