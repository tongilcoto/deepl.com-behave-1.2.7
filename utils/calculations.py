
def get_actual_lemma_info(main_page, lemma_element, label):
    assert main_page.get_translation_lemma_label(lemma_element) == label
    actual_lemma_info = {
        "type": main_page.get_translation_lemma_wordtype(lemma_element),
        "meanings": main_page.get_translation_lemma_meanings_label(lemma_element)
    }
    actual_lemma_usages = main_page.get_translation_lemma_usages(lemma_element)
    if len(actual_lemma_usages) > 0:
        actual_lemma_info["subtypes"] = actual_lemma_usages

    return actual_lemma_info
