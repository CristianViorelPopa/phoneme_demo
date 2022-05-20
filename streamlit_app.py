import numpy as np
import streamlit as st

from Levenshtein import distance as lev

from metaphone import doublemetaphone
from g2p_en import G2p
g2p = G2p()


def lev_arrays(s1, s2):
    if len(s1) < len(s2):
        return lev_arrays(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


st.title('Grapheme to Phoneme and Metaphone Demo')

algo = st.selectbox('Algorithm for phonetic transcription of text',
                    [
                        'Grapheme to Phoneme',
                        'Double Metaphone'
                    ])

first_input = st.text_input('First input phrase or sentence')
second_input = st.text_input('Second input phrase or sentence')

transcribe_button = st.button('Transcribe!')

if transcribe_button:
    if algo == 'Grapheme to Phoneme':
        first_phonetic = g2p(first_input)
        second_phonetic = g2p(second_input)

        st.write(f'Phonetic transcription of first text: {first_phonetic}')
        st.write(f'Phonetic transcription of second text: {second_phonetic}')

        dist = lev_arrays(first_phonetic, second_phonetic)
        st.write(f'Levenshtein distance (applied on the phonemes): {dist}')
        st.write(f'Average percentage error: {dist / np.average([len(first_phonetic), len(second_phonetic)]) * 100}%')

    elif algo == 'Double Metaphone':
        first_phonetics = list(filter(len, doublemetaphone(first_input)))
        second_phonetics = list(filter(len, doublemetaphone(second_input)))

        st.write('Phonetic transcription(s) of the first text:')
        for idx, phonetic in enumerate(first_phonetics):
            st.write(f'{idx + 1}. {phonetic}')

        st.write('Phonetic transcription(s) of the second text:')
        for idx, phonetic in enumerate(second_phonetics):
            st.write(f'{idx + 1}. {phonetic}')

        min_error = 999_999
        chosen_first_phonetic = first_phonetics[0]
        chosen_second_phonetic = second_phonetics[0]
        for phonetic1 in first_phonetics:
            for phonetic2 in second_phonetics:
                dist = lev(phonetic1, phonetic2)
                if dist < min_error:
                    min_error = dist
                    chosen_first_phonetic = phonetic1
                    chosen_second_phonetic = phonetic2

        st.write(f'Chosen phonetic transcriptions for a minimum Levenshtein distance of {min_error}: {chosen_first_phonetic} and {chosen_second_phonetic}')
        st.write(f'Average percentage error: {min_error / np.average([len(chosen_first_phonetic), len(chosen_second_phonetic)]) * 100}%')

    else:
        raise RuntimeError('Algorithm not yet implemented.')
