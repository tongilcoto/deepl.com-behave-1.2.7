Feature: Deepl.com Different text topics
  Assuming
  - Spanish language web set up
  - Hardcoded lists containing text to be translated and its translated expected result. The item will be selected randomly
  - General page behaviour is tested in another features, so these scenarios only test multiple meanings box
  - Page features are tested by layers, going deeper with every test assuming the previous one is passed

  Scenario Outline: Test simple english common word with default web desired language
    Given I open Deepl.com page with "default" language
    When I inform a "<topic>" "<subtopic>" "english" word
    Then the input is translated
    And the original language is set to "english"
    And all word meanings are shown in the multiple meaning box

    Examples:
    | topic       | subtopic |
    | legal       | mortgage |
    | engineering | software |
