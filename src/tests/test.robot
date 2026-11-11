*** Settings ***
Documentation     A test suite checking if a web page loads and displays text.
Resource          keywords.resource
Default Tags      positive


*** Test Cases ***
The Page Displays
    Connect Browser To URL    http://127.0.0.1:5001
    Page Should Contain Text    Hello World
    Close Browser Session