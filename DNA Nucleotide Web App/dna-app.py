import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

image=Image.open('dna.jpg')

st.image(image, use_column_width=True)
st.write("""
# DNA Nucleotide App

This App counts the nucleotide composition

***
""")

#Input Text Box
st.header("Enter the DNA Sequence")
sequence_input= ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence= st.text_area("Sequence input", sequence_input, height=250)
sequence=sequence.splitlines()
sequence=sequence[1:]
sequence=''.join(sequence)

st.write("""
***""")

st.header('Input DNA')
sequence

#Nucleotide count
st.header('Output DNA')
st.subheader("1. Print Dictionary")
def DNA_nucleotide_count(seq):
    d=dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C')),
    ])
    return d

X=DNA_nucleotide_count(sequence)
X_label=list(X)
X_values=list(X.values())

X

#Print Text
st.subheader("2. Print Text")
st.write("There are " + str(X['A']) +  " adenine(A)")
st.write("There are " + str(X['T']) +  " Thymine(T)")
st.write("There are " + str(X['G']) +  " Guanine(G)")
st.write("There are " + str(X['C']) +  " Cytosine(C)")

#Display dataframe
st.subheader("3. Dataframe")
df=pd.DataFrame.from_dict(X, orient='index')
df=df.rename({0:'count'}, axis='columns')
df.reset_index(inplace=True)
df=df.rename(columns={'index':'nucleotide'})
st.write(df)

#Display Bar Chart
st.subheader("Visualization")
p=alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p=p.properties(
    width=alt.Step(80)
)
st.write(p)

