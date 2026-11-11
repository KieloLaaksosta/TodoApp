*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
page loads and displays Hello World
    Go To   ${HOME_URL}
    Page Should Contain Hellow World