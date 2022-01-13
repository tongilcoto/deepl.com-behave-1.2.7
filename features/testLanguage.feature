Feature: Deepl.com Different text original language
  Assuming
  - Spanish language web set up
  - Hardcoded lists containing text to be translated and its translated expected result. The item will be selected randomly
  - General page behaviour is tested in another features, so these scenarios only test multiple meanings box
  - Page features are tested by layers, going deeper with every test assuming the previous one is passed

  Scenario Outline: Test language detection for simple common word with default web desired language
    Given I open Deepl.com page with "default" language
    When I inform a "common" "ordinary" "<originalLanguage>" word
    Then the input is translated
    And the original language is set to "<originalLanguage>"
    And all word meanings are shown in the multiple meaning box

    Examples:
    | originalLanguage  |
    | FRENCH            |
    | GERMAN            |
    | ITALIAN           |


  Scenario Outline: Test language selection for simple common word with default web desired language
    Given I open Deepl.com page with "default" language
    And I select "<originalLanguage>" language in "original" language selector
    And I select "<destinationLanguage>" language in "destination" language selector
    When I inform a "common" "ordinary" "<originalLanguage>" word
    Then the input is translated
    And all word meanings are shown in the multiple meaning box

    Examples:
    | originalLanguage  | destinationLanguage |
    | FRENCH            | ENGLISH             |
    | GERMAN            | FRENCH              |
    | ITALIAN           | GERMAN              |