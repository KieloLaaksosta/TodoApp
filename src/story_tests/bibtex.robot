*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser And Create Test Reference And Go To BibTex Page
Suite Teardown   Close Browser

*** Test Cases ***
BibTex Loads on BibTex Page
    Page Should Contain Text    @book{testkey,
    Page Should Contain Text    author = "testauthor"
    Page Should Contain Text    title = "testtitle"
    Page Should Contain Text    year = "2026"
    Page Should Contain Text    publisher = "testpublisher"
    Page Should Contain Text    }

BibTex File Generates
    Click    text=Download as .bib file
    File Should Exist    ./src/instance/references.bib
    File Should Contain Text    ./src/instance/references.bib   @book{testkey,
    File Should Contain Text    ./src/instance/references.bib    author = "testauthor"
    File Should Contain Text    ./src/instance/references.bib    title = "testtitle"
    File Should Contain Text    ./src/instance/references.bib    year = "2026"
    File Should Contain Text    ./src/instance/references.bib    publisher = "testpublisher"
    File Should Contain Text    ./src/instance/references.bib    }

*** Keywords ***
Open And Configure Browser And Create Test Reference And Go To BibTex Page
    Open And Configure Browser And Create Test Reference
    Click    text=Generate Bibtex

File Should Contain Text
    [arguments]    ${PATH}    ${TEXT}
    Grep File    ${PATH}    ${TEXT}