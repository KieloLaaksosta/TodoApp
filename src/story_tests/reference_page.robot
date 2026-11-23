*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser And Reset Database And Create Test Reference
Suite teardown    Close Browser

*** Test Cases ***
User Can Navigate To Reference Page
    Go To    ${HOME_URL}
    Click    text=testtitle
    Page Should Contain Text    testauthor

