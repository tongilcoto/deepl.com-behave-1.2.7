from behave import given, when, then
from sut.model.mainPage import MainPage
from utils.calculations import get_actual_lemma_info
from utils.constants import TEXT_ORIGINAL_LANGUAGE_LABEL
from utils.dataManager import get_random_data
from utils.dataManager import serialize_and_sort


@given('I open Deepl.com page with "{language}" language')
def step_open(context, language):
    context.current_page = context.main_page
    context.destination_language = "spanish" if language == "default" else language


@when('I inform a "{topic}" "{subtopic}" "{language}" word')
def step_inform_source_text(context, topic, subtopic, language):
    context.original_language = language
    context.test_data = get_random_data(language, topic, subtopic)
    context.main_page.input_source_text(context.test_data["input"])


@when('I inform a "{type}" "{language}" expression')
def step_inform_source_text(context, type, language):
    context.original_language = language
    context.test_data = get_random_data(language, "expressions", type)
    context.main_page.input_source_text(context.test_data["input"])


@then('the input is properly translated')
def step_properly_translated(context):
    translated_text = context.main_page.get_translated_text()
    assert translated_text == context.test_data["output"][context.destination_language]["result"]


@then('the original language is set to "{language}"')
def step_original_language_validation(context, language):
    original_language_label = context.main_page.get_original_language()
    assert original_language_label == TEXT_ORIGINAL_LANGUAGE_LABEL[context.destination_language][language]


@then('all word meanings are shown in the multiple meaning box')
def step_all_meanings_validation(context):
    actual_translation_meanings = []
    array_lemma_elements = context.main_page.get_translation_lemma_elements()
    for lemma_element in array_lemma_elements:
        actual_lemma_info = get_actual_lemma_info(context.main_page, lemma_element, context.test_data["input"])
        actual_translation_meanings.append(actual_lemma_info)

    assert serialize_and_sort(actual_translation_meanings) == serialize_and_sort(context.test_data["output"][context.destination_language]["meanings"])


@then("all alternatives are shown in the result box")
def step_all_alternatives_validation(context):
    if not context.config.userdata.get("mobile"):
        actual_translation_alternatives = context.main_page.get_translation_alternatives()
        assert serialize_and_sort(actual_translation_alternatives) == serialize_and_sort(context.test_data["output"][context.destination_language]["alternatives"])


@then("multiple meanings box is not present")
def step_no_lemma_meaning_is_present(context):
    assert len(context.main_page.get_translation_lemma_elements()) == 0
