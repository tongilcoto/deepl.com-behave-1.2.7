Feature: Deepl.com Different multiple meanings box
  Assuming
  - Spanish language web set up
  - Hardcoded lists containing text to be translated and its translated expected result. The item will be selected randomly
  - General page behaviour is tested in another features, so these scenarios only test multiple meanings box
  - Page features are tested by layers, going deeper with every test assuming the previous one is passed

  Scenario: Test multiple meanings - different number of word types
    Given I open Deepl.com page with "default" language
    When I inform a "common" "ordinary" "english" word
    Then all word types are shown in multiple meanings box


  Scenario: Test multiple meanings - different number of meanings for word type
    Given I open Deepl.com page with "default" language
    When I inform a "common" "ordinary" "english" word being "multiple" word-type
    Then all word type meanings are shown in multiple meanings box
