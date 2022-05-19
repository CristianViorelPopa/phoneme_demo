import streamlit as st
from metaphone import doublemetaphone
from g2p_en import G2p
g2p = G2p()


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
        first_phonetics = list(filter(len, doublemetaphone(first_input)))
        second_phonetics = list(filter(len, doublemetaphone(second_input)))

        first_phonetics_message = 'Phonetic transcription(s) of first text:\n'
        for idx, phonetic in enumerate(first_phonetics):
            first_phonetics_message += f'\t{idx + 1}. {phonetic}\n'
        st.write(first_phonetics_message)

        second_phonetics_message = 'Phonetic transcription(s) of first text:\n'
        for idx, phonetic in enumerate(second_phonetics):
            second_phonetics_message += f'\t{idx + 1}. {phonetic}\n'
        st.write(second_phonetics_message)
