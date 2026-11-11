*** Settings ***
Documentation     A test suite checking if a web page loads and displays text.
Resource          keywords.resource
Default Tags      positive
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser


*** Test Cases ***
The Page Displays
    Go To  ${HOME_URL}
    Page Should Contain Text    Hello World