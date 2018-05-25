"""
Title: events.py

Author: Ashley Williams

Description: Extract event instances from text.

This module is called by init, so there is no need to import this module
specifically.
"""
from coast_core.resources.external_libs import timex
from coast_core import lang_utils as utils
import nltk

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


def get_timex_events(text):
    """
    Given a body of text, returns a list of Timex events.

    :param text:  The text to operate on
    :return: return the timex events
    """
    timex_events = timex.tag(text)
    return timex_events


def get_verb_events(text):
    """
    Given a body of text, returns a list of verb events.
        VB - Verb, base form
        VBD - Verb, past tense
        VBG - Verb, gerund or present participle
        VBN - Verb, past participle - n
        VBP - Verb, non-3rd person singular present - n
        VBZ - Verb, 3rd person singular present - n

    :param text: The text to analyse.
    :return: The list of verb events.
    """
    verb_events = []
    verb_list = ['VB', 'VBD', 'VBG']
    verb_events = utils.penn_treebank_filter(text, verb_list)
    return verb_events


def get_iverb_bigrams(text):
    """
    Split a text into bigrams, following the pattern ("i", <<verb>>).
        VB - Verb, base form
        VBD - Verb, past tense
        VBG - Verb, gerund or present participle
        VBN - Verb, past participle - n
        VBP - Verb, non-3rd person singular present - n
        VBZ - Verb, 3rd person singular present - n

    :param text: The text to analyse
    :return: A dictionary containing 'I verb' bigrams and the total number of 'I verb' events.
    """
    bigrams = utils.get_ngrams(text, 2)

    iverb_dict = {
        "total": 0,
        "events": []
    }

    for bigram in bigrams:
        if bigram[0].lower() == "i":
            # Verbs
            iverb_list = ['VBD', 'VBN']
            iverb_events = utils.penn_treebank_filter(bigram[1], iverb_list)

            if len(iverb_events) > 0:
                iverb_dict['total'] += 1
                iverb_dict['events'].append({
                    "bigram": bigram,
                    "verb": iverb_events[0]
                })
    return iverb_dict


def run_all_event_analysis(article_text):
    """
    Run all event analysis for all articles.

    :param article_text: The text to analyse.
    :return: An object containing timex events, verb events and iverb bigrams
    """
    timex = get_timex_events(article_text)
    verbs = get_verb_events(article_text)
    iverbs = get_iverb_bigrams(article_text)

    return {
        "timex_events": timex,
        "verb_events": verbs,
        "iverb_bigrams": iverbs
    }