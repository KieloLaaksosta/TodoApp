*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser And Reset Database And Create Test Reference
Suite teardown    Close Browser

*** Test Cases ***
User Can Navigate To Reference Page
    Go To Reference    testtitle
    Page Should Contain Text    testtitle

User Can See Data About The Reference
    Go To Reference    testtitle
    Page Should Contain Text    testtitle
    Page Should Contain Text    testauthor
    Page Should Contain Text    2026
    Page Should Contain Text    testkey
    Page Should Contain Text    testpublisher
    Page Should Contain Text    book

*** Keywords ***
Go To Reference
    [Arguments]    ${title}
    Go To    ${HOME_URL}
    Click    text=${title}