import streamlit as st
import numpy as np
import sys
import jsonpickle
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
from pydot import Dot, Edge, Node
import cv2
from PIL import Image

#Defining the DFA
def dfa_definer():
    dfa_list={}

    #Adding number of states
    state_list = []
    with col1:
        noOfStates=st.number_input("Enter no. of states in DFA",min_value=0)
        for i in range(int(noOfStates)):
            state_list.append('q'+str(i))
        dfa_list['states']=state_list

    #Defining the characters
    with col1:
        characters=st.text_area("Enter characters in alphabet")
        if characters is not None: 
            alphabet_list=characters.splitlines()
        dfa_list['alphabets']=alphabet_list
    
    #Initial state
    with col1:
        initialState=st.selectbox("Select the initial state",options=np.array(state_list))
        dfa_list['initialState']=initialState
    
    #Final states
    with col1:
        finalStates=[]
        finalStates=st.multiselect("Select the final state/states",options=np.array(state_list))
        dfa_list['finalStates']=finalStates

    #Defining the transitions rules 
    with col2:
        st.write('Define the transition of each alphabet for each state')
        transition={}
        for state in state_list:
            transition[state]={}
            for character in alphabet_list:
                s= '\u03B4 ('+state+' , '+character + ') -> '
                transition[state][character]=st.selectbox(label=s,options=np.array(state_list))
        dfa_list['transitions']=transition

    return dfa_list,alphabet_list
    

#Checking whether a string belong to DFA or not
def dfa_checker(dfa_list,string):
    currentState = dfa_list['initialState']
    for ch in string:
        if ch not in dfa_list['alphabets']:
            return False
        currentState = dfa_list['transitions'][currentState][ch] 
    if currentState in dfa_list['finalStates']:
        return True
    else:
        return False


#Main function
st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center; color: maroon;'>Welcome to DFA Checker!</h1>", unsafe_allow_html=True)
menu=["Upload file", "Enter parameters"]
choice=st.sidebar.selectbox("Menu",menu)
# dfa_list=[]
string=""
col1, col2 = st.columns(2)
dfa_exists = False
if(choice=="Upload file"):
    dfa_file = st.file_uploader("Upload the DFA file", type=["txt"])
    if dfa_file is not None:
        raw_text = str(dfa_file.read(),"utf-8")
        dfa_list=jsonpickle.decode(raw_text)
        dfa_exists = True
elif(choice=="Enter parameters"):
    col1.header("DFA Parameters")
    col2.header("DFA transition rules")
    dfa_list,alphabet_list=dfa_definer()
    dfa_exists = True
if dfa_exists == True and dfa_list['states']!=[]:
    dfa = DFA(states=set(dfa_list['states']),
        input_symbols=set(dfa_list['alphabets']),
        transitions=dfa_list['transitions'],
        initial_state=dfa_list['initialState'],
        final_states=set(dfa_list['finalStates']),
    )
    new_dfa=VisualDFA(dfa)
    dot=new_dfa.show_diagram()
    dot.format='png'
    dfa_image=dot.render('dfa_diagram')
    col1, col2= st.columns(2)
    img_dfa = Image.open('dfa_diagram.png')
    img_dfa = np.array(img_dfa)
    # img_dfa_resize = cv2.resize(img_dfa, None, fx= 2, fy=2, interpolation= cv2.INTER_AREA)
    st.image(img_dfa, caption='DFA')
    string=st.text_input("Enter a string to check whether it is accepted by the DFA")
if string!="":
    # dfa = DFA(
    #     states=set(dfa_list['states']),
    #     input_symbols=set(dfa_list['alphabets']),
    #     transitions=dfa_list['transitions'],
    #     initial_state=dfa_list['initialState'],
    #     final_states=set(dfa_list['finalStates']),
    #     )
    # new_dfa=VisualDFA(dfa)
    # dot=new_dfa.show_diagram()
    # dot.format='png'
    # dfa_image=dot.render('dfa_diagram')
    # col1, col2= st.columns(2)
    # img_dfa = Image.open('dfa_diagram.png')
    # img_dfa = np.array(img_dfa)
    # img_dfa_resize = cv2.resize(img_dfa, None, fx= 2, fy=2, interpolation= cv2.INTER_AREA)
    # with col1:
    #     st.image(img_dfa_resize, caption='DFA')
    flag=0
    for ch in string:
        if ch not in dfa_list['alphabets']:
            st.header('"'+string + '" contains alphabets undefined by DFA!! Please enter again..')
            flag=1
            break
    if(flag==0):
        dot_string=new_dfa.show_diagram(string)
        dot_string.format='png'
        dfa_string_image=dot_string.render('dfa_diagram_string')
        img_dfa_string = Image.open('dfa_diagram_string.png')
        img_dfa_string = np.array(img_dfa_string)
        # img_dfa_string_resize = cv2.resize(img_dfa_string, None, fx= 2, fy=1.1, interpolation= cv2.INTER_AREA)
        st.image(img_dfa_string, caption='DFA for the string')
        if dfa_checker(dfa_list,string):
            st.header(u'\u2713 "' + string + '" is in the language defined by the DFA.')
        else:
            st.header( u'\u2717 "' + string + '" is NOT in the language defined by the DFA.')

