# Database Final Project -- Harrison, Porter, and Josh

## Setting up:

Install the sole dependency by running:

`pip install termcolor`

Because this is a console/terminal-based app, we used this library to add color to print text.

## Navigating the app

Navigating this app is done by simple text-based menu interaction. 

Upon launching the app, users are prompted to login with their University of Saint Thomas email. No password is required. Signing in will only work if the "username" is 8 characters long (i.e. john1234) and the domain name is "@stthomas.edu".

Upon signing in, users are displayed several options. Instructions are for selecting options or going back are made clear for the page that the user is on. Enter a number or letter that corresponds with the options displayed.

Typically, as displayed on the screen when available, pressing Q will take the user "back" to the previous menu. If the user enters an option that is not displayed, they will receive a soft error message.
