*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser And Create Test Reference
Suite Teardown   Close Browser

*** Test Cases ***
BibTex Loads on BibTex Page
    Click    text=Generate BibTex
    Page Should Contain Text    @book{testkey,
    Page Should Contain Text    author = "testauthor"
    Page Should Contain Text    title = "testtitle"
    Page Should Contain Text    year = "2026"
    Page Should Contain Text    publisher = "testpublisher"
    Page Should Contain Text    }