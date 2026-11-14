*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
page loads and displays Reference helper
    Go To   ${HOME_URL}
    Page Should Contain Text   Reference helper

user can add a new reference
    Go To    ${HOME_URL}
    Click    text=Add new reference
    
    Fill Field    bibtex_key      meikäläinen123
    Fill Field    reference_type  book
    Fill Field    author          Matti Meikäläinen
    Fill Field    title           Kokeilupainos
    Fill Field    year            2026
    Fill Field    publisher       Tylsätkirjat
    
    Click    text=Add Reference
    
    Get Url    ==    ${HOME_URL}/
    Page Should Contain Text    meikäläinen123
    Page Should Contain Text    Matti Meikäläinen
    Page Should Contain Text    Kokeilupainos
    Page Should Contain Text    2026
    Page Should Contain Text    Tylsätkirjat