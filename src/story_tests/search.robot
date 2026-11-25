*** Settings ***
Resource          resource.robot
Suite Setup       Open And Configure Browser And Create Test References
Suite Teardown    Close Browser
Test Setup        Go To    ${HOME_URL}

*** Test Cases ***
No search returns all
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    dawkins2009
    Page Should Contain Text    harjulehto2023
    Page Should Contain Text    meikalainen123

Search finds full match in key
    Fill Field    search    harjulehto2023
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    harjulehto2023
    Page Should Contain Text    Petteri Harjulehto
    Page Should Not Contain Text    dawkins2009

Search finds partial match in key
    Fill Field    search    meikalainen
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    meikalainen123
    Page Should Contain Text    Matti Meikäläinen
    Page Should Contain Text    Kokeilupainos
    Page Should Contain Text    2026
    Page Should Contain Text    Tylsätkirjat
    Page Should Not Contain Text    dawkins2009

Search finds partial match in title
    Fill Field    search    Show on Earth
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    dawkins2009
    Page Should Contain Text    The Greatest Show on Earth: The Evidence for Evolution
    Page Should Not Contain Text    harjulehto2023

Search finds partial match in type
    Fill Field    search    book
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    meikalainen123
    Page Should Contain Text    dawkins2009
    Page Should Contain Text    harjulehto2023

Search finds partial match in year
    Fill Field    search    202
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    harjulehto2023
    Page Should Contain Text    meikalainen123
    Page Should Not Contain Text    dawkins2009

Displays all matches
    Fill Field    search    book
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Contain Text    dawkins2009
    Page Should Contain Text    harjulehto2023
    Page Should Contain Text    meikalainen123

No matches displays nothing
    Fill Field    search    nonexistent999
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/?
    Page Should Not Contain Text    dawkins2009
    Page Should Not Contain Text    harjulehto2023
    Page Should Not Contain Text    meikalainen123

Non matching not displayed
    Fill Field    search    Gaudeamus
    Click    text=Filter
    Get Url    ^=    ${HOME_URL}/
    Page Should Contain Text    harjulehto2023
    Page Should Not Contain Text    dawkins2009
    Page Should Not Contain Text    meikalainen123

*** Keywords ***
Open And Configure Browser And Create Test References
    Open And Configure Browser
    Reset Database
    Create Reference    dawkins2009    book    Richard Dawkins    The Greatest Show on Earth: The Evidence for Evolution    2009    Free Press
    Create Reference    harjulehto2023    book    Petteri Harjulehto    Analyysiä reaaliluvuilla    2023    Gaudeamus
    Create Reference    meikalainen123    book    Matti Meikäläinen    Kokeilupainos    2026    Tylsätkirjat