# Database Final Project -- Harrison, Porter, and Josh

## Setting Up:

Install the sole dependency by running:

`pip install termcolor`

Because this is a console/terminal-based app, we used this library to add color to print text.

## Config

The `config.py` contains the file path to the database should it for whatever reason be different on your machine.

## Navigating the App

Navigation is done by simple text-based menu interaction. 

Upon launching the app, users are prompted to login with their University of Saint Thomas email. No password is required. Signing in will only work if the "username" is 8 characters long (i.e. john1234) and the domain name is "@stthomas.edu".

Upon signing in, users are displayed with several options. Instructions for selecting options or going back are made clear for the page that the user is on. Input a number or letter that corresponds with the options displayed and press enter to bounce between menus.

Typically, as displayed on the screen when available, pressing Q will take the user back to the previous menu. If the user enters an option that is not displayed, they will receive a soft error message.
