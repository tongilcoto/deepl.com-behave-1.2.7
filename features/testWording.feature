Feature: Deepl.com Different input text wording
  Assuming
  - Spanish language web set up
  - Hardcoded lists containing text to be translated and its translated expected result. The item will be selected randomly
    - Ideally this approach would be substituted by data provider service, based on the different text classification
    - Ideally complex translations results should be validated by a Natural Language Processor engineer, who will be responsible for data provider service data set, both input and output
    - Ideally translation algorithm tests could be performed using APIs tests, this approach will avoid wasting time in front end framework
  - Parameter values such as "common", "ordinary", "multiple-options", etc should be changed to more appropriated ones following business ordinary terminology

  Scenario: Test simple english common word with default web desired language translation
    Given I open Deepl.com page with "default" language
    When I inform a "common" "ordinary" "english" word
    Then the input is properly translated
    And the original language is set to "english"
    And all word meanings are shown in the multiple meaning box


  Scenario: Test simple english common word with default web desired language translation
    Given I open Deepl.com page with "default" language
    When I inform a "common" "multiple-options" "english" word
    Then the input is properly translated
    And the original language is set to "english"
    And all word meanings are shown in the multiple meaning box
    And all alternatives are shown in the result box


  Scenario: Test english short phrases with default web desired language translation
    Given I open Deepl.com page with "default" language
    When I inform a "short" "english" expression
    Then the input is properly translated
    And the original language is set to "english"
    And all alternatives are shown in the result box


  Scenario: Test english complex phrases with default web desired language translation
    Given I open Deepl.com page with "default" language
    When I inform a "complex" "english" expression
    Then the input is properly translated
    And the original language is set to "english"
    And all alternatives are shown in the result box


  Scenario: Test english unknown word with default web desired language best-effort-translation
    Given I open Deepl.com page with "default" language
    When I inform a "common" "unknown" "english" word
    Then the input is properly translated
    And the original language is set to "english"
    And all alternatives are shown in the result box
    And multiple meanings box is not present
