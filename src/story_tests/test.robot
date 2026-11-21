*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Page Loads And Displays Reference Helper
    Go To   ${HOME_URL}
    Page Should Contain Text   Reference helper

User Can Add A New Reference
    Go To    ${HOME_URL}
    Click    text=Add new reference
    
    Fill Field    bibtex_key      meikalainen123
    Select Value  reference_type  book
    Fill Field    author          Matti Meikäläinen
    Fill Field    title           Kokeilupainos
    Fill Field    year            2026
    Fill Field    publisher       Tylsätkirjat
    
    Click    text=Add Reference
    
    Get Url    ==    ${HOME_URL}/
    Page Should Contain Text    meikalainen123
    Page Should Contain Text    Matti Meikäläinen
    Page Should Contain Text    Kokeilupainos
    Page Should Contain Text    2026
    Page Should Contain Text    Tylsätkirjat

User Can Navigate To BibTex Page
    Go To    ${HOME_URL}
    Click    text=Generate BibTex
    Page Should Contain Text    Download