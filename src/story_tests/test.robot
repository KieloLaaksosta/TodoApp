*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
page loads and displays Reference helper
    Go To   ${HOME_URL}
    Page Should Contain Text   Reference helper