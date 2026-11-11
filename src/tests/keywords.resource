*** Settings ***
Library    Browser

*** Keywords ***
Connect Browser To URL
    [Arguments]    ${url}
    New Browser    browser=chromium    headless=False
    New Page       ${url}

Page Should Contain Text
    [Arguments]    ${expected_text}
    Get Text       body    contains    ${expected_text}

Close Browser Session
    Close Browser