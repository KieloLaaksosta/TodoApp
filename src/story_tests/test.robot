*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References


*** Test Cases ***
page loads and displays Reference helper
    Go To   ${HOME_URL}
    Page Should Contain Text   Reference helper

After adding a reference, there is one
    Go To  ${HOME_URL}
    Click  text=Add new reference
    Fill Text  [name="bibtex_key"]  Martin09
    Fill Text  [name="reference_type"]  book
    Fill Text  [name="author"]  Robert Martin
    Fill Text  [name="title"]  Clean Code: A Handbook of Agile Software Craftsmanship
    Fill Text  [name="year"]  2008
    Fill Text  [name="publisher"]  Prentice Hall
    Click  input[value="Add Reference"]
    Get Text  body  *=  Martin09
    Get Text  body  *=  Clean Code: A Handbook of Agile Software Craftsmanship