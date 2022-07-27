# Product Currency Helper

This is a project created during the "SFWRTECH 4SA3: Software Architecture" course in McMaster.
Only the code in folder `/server/` has comments that document the most important implementation for grading.
Use access token `jinyao.ma,001433428` to try the application while `http://localhost:8080` is running.

## Environment Requirement

- Node.js with npm (I was using Node.js version 14.18.1 with npm v8)
- Python with pip (I was using Python version 3.9.13 with pip v21)

## Setup Manual

1. Download the source code [master.zip](https://github.com/jinyaoMa/product-currency-helper/archive/refs/heads/master.zip).
2. Extract `master.zip` and open folder `/product-currency-helper-master/` in command line.
   - use command like `cd product-currency-helper-master`.
3. Run command `npm run setup:server` to install dependencies for server.
4. Run command `npm run setup:client` to install dependencies for client.

## Run the application in development mode

1. Open 2 command line windows.
2. Change the current directory for the 2 command line to the project root folder `/product-currency-helper-master/`.
3. Run command `npm run run:server` in one of the 2 command line to start up the server.
4. Run command `npm run run:client` in another command line to start up the client.
5. Open a latest modern browser, such as Google Chrome, and browse with URL `http://localhost:8080`.
