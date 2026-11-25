*** Settings ***
Library    Browser
Library    OperatingSystem
Library    ${CURDIR}/../db_helper.py

*** Variables ***
${SERVER}     127.0.0.1:5001
${DELAY}      500ms
${HOME_URL}   http://${SERVER}
${BROWSER}    chromium
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}    headless=True
    ELSE
        New Browser  browser=${BROWSER}    headless=False    slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Reset Database
    Reset Db

Page Should Contain Text
    [Arguments]    ${expected_text}
    Get Text       body    contains    ${expected_text}

Page Should Not Contain Text
    [Arguments]    ${unexpected_text}
    ${page_text}=    Get Text    body
    Should Not Contain    ${page_text}    ${unexpected_text}

Fill Field
    [Arguments]    ${field_id}    ${field_text}
    Fill Text    id=${field_id}    ${field_text}

Clear Field
    [Arguments]    ${field_id}
    Clear Text    id=${field_id}

Select Value
    [Arguments]    ${dropdown_id}    ${value}
    Select Options By    id=${dropdown_id}    value    ${value}

Create Reference
    [Arguments]    ${key}    ${type}    ${author}    ${title}    ${year}    ${publisher}
    Go To    ${HOME_URL}
    Click    text=Add new reference
    
    Fill Field    bibtex_key      ${key}
    Select Value  reference_type  ${type}
    Fill Field    author          ${author}
    Fill Field    title           ${title}
    Fill Field    year            ${year}
    Fill Field    publisher       ${publisher}
    
    Click    text=Add Reference

Open And Configure Browser And Reset Database And Create Test Reference
    Open And Configure Browser
    Reset Database
    Create Reference    testkey    book    testauthor    testtitle    2026    testpublisher
