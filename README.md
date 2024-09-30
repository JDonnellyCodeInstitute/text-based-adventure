BUG: FIXED// Call to adventure being called twice in case of restart with same character - Removed the redundant call to call_to_adventure in restart_game when restarting with the same character. Ensured intro() only calls call_to_adventure on new character creation.
BUG: FIXED// NoneType exception occurring between the intro and call_to_adventure methods. Return of 'player' added to intro function
BUG: FIXED// Bet maximum validation updated to ensure user can't bet if their gold is less than their minimum bet.

RPS Guidance: https://www.youtube.com/watch?v=fn68QNcatfo

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
