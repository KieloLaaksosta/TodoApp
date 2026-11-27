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

User Can Edit Reference
    Go To Reference    testtitle

    Click    text=Edit

    Clear Field    bibtex_key
    Clear Field    author
    Clear Field    title
    Clear Field    year
    Clear Field    publisher

    Fill Field    bibtex_key      newkey
    Select Value  reference_type  book
    Fill Field    author          newauthor
    Fill Field    title           newtitle
    Fill Field    year            2025
    Fill Field    publisher       newpublisher
    
    Click    button >> text=Update reference

    Get Url    ==    ${HOME_URL}/reference/newkey

    Page Should Contain Text    newkey
    Page Should Contain Text    newpublisher
    Page Should Contain Text    newtitle

User Can Delete Reference
    Go To Reference    newtitle

    Handle Future Dialogs    action=accept
    Click    button >> text=Delete

    Get Url     ==    ${HOME_URL}/
    Page Should Contain Text    Reference 'newkey' was deleted.
    Page Should Not Contain Text    newtitle

*** Keywords ***
Go To Reference
    [Arguments]    ${title}
    Go To    ${HOME_URL}
    Click    text=${title}