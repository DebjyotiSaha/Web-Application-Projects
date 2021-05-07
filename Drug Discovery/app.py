import mols2grid
import pandas as pd 
import streamlit as st 
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem.Descriptors import ExactMolWt, MolLogP, NumHDonors, NumHAcceptors

st.title('Filtration of FDA Aprroved Drugs')
st.markdown("""
    - App modified by Debjyoti Saha
    """)

@st.cache(allow_output_mutation=True)
def download_dataset():
    df=pd.read_csv("https://www.cureffi.org/wp-content/uploads/2013/10/drugs.txt", sep="\t").dropna()
    return df

#Calculate descriptors
def calc_mw(smiles_string):
    mol=Chem.MolFromSmiles(smiles_string)
    return ExactMolWt(mol)

def calc_logp(smiles_string):
    mol=Chem.MolFromSmiles(smiles_string)
    return MolLogP(mol)

def calc_NumHDonors(smiles_string):
    mol=Chem.MolFromSmiles(smiles_string)
    return NumHDonors(mol)

def calc_NumHAcceptors(smiles_string):
    mol=Chem.MolFromSmiles(smiles_string)
    return NumHAcceptors(mol)

#Copying the dataset
df=download_dataset().copy()
df["MW"]=df.apply(lambda x: calc_mw(c["smiles"]), axis=1)
df["LogP"]=df.apply(lambda x: calc_logp(x["smiles"]), axis=1)
df["NumHDonors"]=df.apply(lambda x: calc_NumHDonors(x["smiles"]), axis=1)
df["NumHAcceptors"]=df.apply(lambda x: calc_NumHAcceptors(x["smiles"]), axis=1)

#Sidebar Panel
st.sidebar.header('Parameters')
st.sidebar.write('Display compunds having values less than the following Thresholds')
weight_cutoff= st.sidebar.slider(
    label="Molecular weight",
    min_value=0,
    max_value=1000,
    value=500,
    step=10,
)
logp_cutoff=st.sidebar.slider(
    label="LogP",
    min_value=-10,
    max_value=10,
    value=5,
    step=1,
)
NumHDonors_cutoff=st.sidebar.slider(
    label="NumHDonors",
    min_value=0,
    max_value=15,
    value=5,
    step=10,
)
NumHAcceptors_cutoff=st.sidebar.slider(
    label="NumHAcceptors",
    min_value=0,
    max_value=20,
    value=10,
    step=1,
)
df_result=df[df["MW"]<weight_cutoff]
df_result2=df_result[df_result["LogP"]< logp_cutoff]
df_result3=df_result2[df_result2["NumHDonors"]< NumHDonors_cutoff]
df_result4=df_result3[df_result3["NumHAcceptors"]< NumHAcceptors_cutoff]

st.write(df_result4.shape)
st.write(df_result4)

raw_html=mols2grid.display(df_result4,
    subset=["Name", "img", "MW", "LogP", "NumHDonors", "NumHacceptors"],
    mapping={"smiles": "SMILES", "generic_name": "Name"})._repr_html()
components.html(raw_html, width=900, height=1100, scrolling=False)
