#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas
import re
import itertools


# In[2]:


delimiters = [".", ",", ";", ":"]
word_splitters = ['and', 'also']
remove_delimiter = [" mr. ", " rs. ", ".com ", " etc. "]
conjunctions = ['and', "also"]


# In[3]:


test1 ="\nRespected Sir/Madam,\nI would like to draw your kind attention towards the malpractices and  customer mishandling  going on at AXIS Bank Katwa Branch  UTIB0000320  with full knowledge of the Bank Official.\nOn the last week of March 2019, my Father-in-Law Mr Swapan Kumar Ghosh holding\nAccount Number: 903010044558545  approached the Bank Manager on the request of Opening a Tax Saving Fixed Deposit of Rs. 1,50,000/-.\nThe Bank Manager forwarded him to an Agent for doing so who is not an Bank Employee , I suppose.\nThe Agent was probably from Max Life Insurance,  this agent then Visited my home and tried to brainwash my father, and successfully created a Life Insurance Policy of Max Life Insurance of Rs 1,50,000/ but not on the PAN of Mr Swapan Kr Ghosh, but on the PAN of his son Mr. Ashutosh Ghosh  since he is young in age and he will get better commissions  ,\nHe got signed all the copies on the pretext that Mr Ashutosh Ghosh will be nominee but did all sorts of games.\n\n15 days later when the policy copy came, we realized what he has done.\n\nNow the actual purpose of Mr Swapan Kr Ghosh  tax saving  complete failed and hence he will have to pay additional tax, over and above he has now been given a burden to pay Rs 1,50,000 every year now.\n\nIs Axis Bank an agent of Max Life Insurance? Why is this kind of handling done with customer who are not highly financially educated.\n\nPlease look into the issue with urgency, we are really worried about Axis Bank Now, and we have no further faith in your services.\n\n"


# In[4]:


test2 = "I wish to convey my Sincere Appreciation for the service and commitment shown by Mr Chaitanya Chitkar of Max life insurance New Delhi. I was in a lot of distress as my insurance policy had lapsed due to an error in account change from NRIi to NRO due to the inefficiency of the axis bank NRI team, and the customer service at max life was unable to send me the remaining funds amounting to Rs 65000, for over 2.5 years . They claimed to have mailed 2 cheques to Canada however I did not receive any mail..which is unlikely as I get all my bank cards etc from Indian banks without issue via courier. I hav already lost over Rs 30,000 of my investment due to the errors. This march I decided to visit the Max life office in Yusuf Sarai and was Introduced to Chaitanya through Mr. Tyagi the Operations Manager. That seems to have made a lot of difference as Chaitanya followed through with his promise , he tried twice to deposit through NEFT. However, Axis bank did not allow the transfer due to RBI regulations. Then he made a special request to issue a cheque , personally deposited the cheque in the branch at Yusuf Sarai along with necessary documents to allow a speedy credit. Unsuccessful again! as The cheque was sitting in the Axis bank for over 3 weeks as no one there knew what had to be done, next Chaitanya on his own initiate tracked it down at the branch and ensured I received the credit with the interest added. NRI depend on efficiency to do our business / investments in India as the time difference and regulations are difficult to navigate. This was all on his own initiative and outside the job description. The Axis bank made no attempt to help me and if it wasn&#8217;t for the determination and sincerity of Chaitanya , I would still be waiting for the credit. Max life should make these examples known to inspire other young employees to go above and beyond for a great customer experience . It is people like Chaitanya who work with passion and sincerity that succeed in life.. any job can be made exciting and fulfilling , it depends on how we approach it. wishes to Chaitanya for a wonderful career ahead. Anuradha Mallick"


# In[5]:


test3 = "and...........................afgn,:dsafsadfasdkjkj asdf':, and"


# In[6]:


test4 = "asdfffffffffffasdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf  asdfasdlkladkfh  asdhaksdflsahjdhadf a sdf asdfjhas asdf aasdfffffffffffasdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf asdf  asdfasdlkladkfh  asdhaksdflsahjdhadf a sdf asdfjhas asdf a, asdfafdf asdf,jhjf  fjhgjh"


# In[7]:


test5 = "\nDear Sir,\n\nI would like to inform you that I had purchased a Policy No.  dated 13th December 2013 in Axis Bank Cuttack branch. Forever Young Pension Plan  by convincing me that you can pay one time for one time and withdraw after five years with a good returns, after investing after one year I received a call stating for premium to be paid, I approached your local branch in Visakhapatnam and enquired about this issue, they had suggested me that you have to pay for minimum 5 years locking period then only you can withdraw this amount, So I started continuing this policy and paid ever year till 2017 and in 2018 I was not able to pay the premium due to some financial crunch, But still I through not to discontinue this policy, So I kept this policy in force saying that will pay once I am financially  up to mark,\n\nLast month I received a AXIS Bank tale online call stating that to pay the due premium and active the policy, So I issued a cheque no.244503  for Rs.200000/- in favour of same policy and submitted in our local branch Visakhapatnam, Now I got a call from MAXLIFE stating that this policy is converted in Pension plan and it cannot be continued, My plan is for 10 years and how it can be converted to pension plan without any pre information or hard copy signature collected by me.\n\nAlso note I was joined as an Advisor / AAP Agent code 584434  in Max life in the year 2016 with a good track record and received lot of felicitations in short period by generating a good business. I do have my own existing policy&#8217;s as below  which some of them term completed and some of them are in force.\n\n1\n876747163\n26.2.2013\nTerm Complete\n113674\n2\n856203070\n24-03-2012\nTerm Complete\n56386\n3\n823721345\n29-11-2010\nTerm Complete\n29997\n4\n410902787\n13-12-2013\nIN Force\n200000\n5\n105209332\n31-03-2016\nIN Force\n100000\n6\n105209480\n31-03-2016\nIN Force\n100000\n7\n105170997\n25-05-2016\nIN Force\n20000\n8\n518683651\n17-03-2018\nIN Force\n200000\n9\n518684121\n17-03-2018\nIN Force\n15003\n\nPlease note being a valuable customer and  working as an Adviser I am in trouble for above issue means what I can expect and explain my clints for further investments,  Sorry to say that  I am not interested to convert the policy Sl. No.4  which you are insisting for,  If I don&#8217;t get a suitable solution for this issue I have to approach legally for justice, So Once again I request your to  Please allow me to continue this policy or transfer the funds by investing in new policy, or switching, Redirect, or withdraw and close the policy.\n\nHope your kind cooperation and needful&#8230;.\n\nAwaiting for your immediate reply&#8230;.\n\n--\n\nWith "


# In[8]:


email = test5


# In[9]:


email = email.lower()


# In[10]:


print(email)


# In[11]:


def remove_nesting(text_list):
    output = list(itertools.chain.from_iterable(text_list))
    return output


# In[12]:


def sen_len(row):
    text_list = row
    sentence_length = []
    for item in text_list:
        sentence_length.append(len(item))
    return sentence_length, len(text_list), max(sentence_length)


# In[13]:


def get_punc_split_indices(delimiter_indices):
    delimiter_diff = [j - i for i, j in zip(delimiter_indices[: -1], delimiter_indices[1 :])] 
    i = 0
    max_len = len(delimiter_diff)
    char_sum = 0
    split_indices = []
    while(i<max_len):
        while(1):
            if char_sum<255 and i!=max_len:
                char_sum += delimiter_diff[i]
                prev_i = i
                i+=1
            else:
                split_indices.append(delimiter_indices[prev_i])
                if i!=max_len:
                    i = prev_i
                char_sum = 0
                break;
    return split_indices


# In[14]:


def get_delimiter_indice(email, delimiters):
    delimiter_indices =[0]
    for i, char in enumerate(email):
        if char in delimiters:
            delimiter_indices.append(i)
    return delimiter_indices


# In[15]:


def get_line_splitter(email):
    excerpts = list(set(email.splitlines()))
    if '' in excerpts:
        excerpts.remove('')
    return excerpts


# In[16]:


def find_word_indices(word, sentence):
    indices = []
    index =0
    while(1):
        adjuster = index
        index = sentence.find(word)
        if index == -1:
            break;
        else:
            indices.append(adjuster+index+2)
            sentence= sentence[index+3:]
    return indices


# In[17]:


def get_unwanted_delimiter(sentence, remove_delimiter):
    remove_delimiters_indices = []
    for item in remove_delimiter:
        if item in [" mr. ", " rs. "]:
            select_indice = 3
        elif item =='.com ':
            select_indice = 0
        elif item ==' etc. ':
            select_indice = 4
        temp_indices = [i.start() for i in re.finditer(item, email)]
        temp_indices = [i + select_indice for i in temp_indices]
        remove_delimiters_indices.extend(temp_indices)
    remove_delimiters_indices.extend(find_word_indices('no.', sentence))
    return remove_delimiters_indices


# In[18]:


def get_splitted_sentence(sent):
    if len(sent) < 255:
        res = [sent]
    else:
        delimiter_indices = get_delimiter_indice(sent, delimiters)
        unwanted_indices = get_unwanted_delimiter(sent, remove_delimiter)
        final_indices = list(set(delimiter_indices)- set(unwanted_indices))
        final_indices.sort()
        split_indices = get_punc_split_indices(final_indices)
        res = [sent[i:j] for i,j in zip(split_indices, split_indices[1:]+[None])]
    return res


# In[19]:


def remove_redundant_sent(excerpts, sen_len=2):
    res = []
    for item in excerpts:
        if len(item.split(' '))<=sen_len:
            pass
        else:
            res.append(item)
    return res


# In[20]:


def get_excerpts(email):
    excerpts = []
    sentences = get_line_splitter(email)
    for item in sentences:
        excerpts.extend(get_splitted_sentence(item))
    excerpts_clean = remove_redundant_sent(excerpts)
    return excerpts_clean


# In[21]:


def conjunction_splitter():
#     based on conjunctions
    pass


# In[22]:


def final_splitter():
#     based on space
    pass


# In[23]:


excerpts = get_excerpts(email)
excerpts


# In[24]:


sen_len(excerpts)


# In[77]:


sentence = ", so i started continuing this policy and paid ever year till 2017 and in 2018 i was not able to pay the premium due to some financial crunch, but still i through not to discontinue this policy"


# In[203]:


sent = email


# In[204]:


sent


# In[205]:


delimiter_indices = get_delimiter_indice(sent, delimiters)


# In[206]:


delimiter_indices


# In[207]:


unwanted_indices = get_unwanted_delimiter(sent, remove_delimiter)


# In[208]:


unwanted_indices


# In[209]:


final_indices = list(set(delimiter_indices)- set(unwanted_indices))
final_indices.sort()


# In[210]:


final_indices


# In[211]:


delimiter_diff = [j - i for i, j in zip(delimiter_indices[: -1], delimiter_indices[1 :])] 


# In[212]:


delimiter_diff


# In[214]:


i = 0
max_len = len(delimiter_diff)
char_sum = 0
split_indices = []


# In[215]:


max_len


# In[216]:


while(i<max_len):
    while(1):
        if char_sum<255 and i!=max_len:
            char_sum += delimiter_diff[i]
            prev_i = i
            i+=1
        else:
            split_indices.append(delimiter_indices[prev_i])
            if i!=max_len:
                i = prev_i
            char_sum = 0
            break;


# In[198]:


while(i<max_len):
    if char_sum<255 and i!=max_len:
        char_sum += delimiter_diff[i]
        prev_i = i
        i+=1
    else:
        split_indices.append(delimiter_indices[prev_i])
        if i!=max_len:
            i = prev_i
        char_sum = 0
        break;


# In[197]:


split_indices


# In[192]:


while(i<max_len):
    if delimiter_diff[i]>=255:
        split_indices.append(delimiter_indices[i+1])
        i+=1
    elif char_sum<255 and i!=max_len:
        char_sum += delimiter_diff[i]
        prev_i = i
        i+=1
        print("in char sum", char_sum, prev_i, i)
    else:
        print("in else part")
        split_indices.append(delimiter_indices[prev_i])
        if i!=max_len:
            i = prev_i
        char_sum = 0


# In[193]:


split_indices


# In[117]:


res = [sent[i:j] for i,j in zip(split_indices, split_indices[1:]+[None])]


# In[78]:


for 
find_word_indices("and", sentence)


# In[60]:


re.findall(r'^[a-zA-Z]*$', '17-03-2018')


# In[62]:


re.findall('^[a-zA-Z]*$', 'ow i')


# In[ ]:





# any number .
# 
# any number . number

# In[ ]:





# In[ ]:





# In[ ]:





# In[120]:


sent = email


# In[133]:


sent_list = []
prev_index = 0
i = 1
char_sum = 1
delimiter_indice = -1
start_split = 0 
delimiter_flag = 0


# In[134]:


while(i<len(sent)):
    if sent[i] in delimiters:
        print("in delimiter")
        prev_indice = delimiter_indice
        delimiter_indice = i
        delimiter_flag = 1
    print("in charsum")
    char_sum += 1
    if char_sum>255 and delimiter_flag = 1:
        
    else:
        print("in else")
        end_split = delimiter_indice
        sent_list.append(sent[start_split:end_split])
        char_sum = 0
        i = delimiter_indice+1
        start_split = i
    print(i, sent[i], delimiter_indice)


# In[ ]:


while(i<len(sent)):
    if sent[i] in delimiters:
        print("in delimiter")
        prev_indice = delimiter_indice
        delimiter_indice = i
        delimiter_flag = 1
    if char_sum<255 and delimiter_flag!=0:
        print("in charsum")
        char_sum += 1
        i+=1
    else:
        print("in else")
        end_split = delimiter_indice
        sent_list.append(sent[start_split:end_split])
        char_sum = 0
        i = delimiter_indice+1
        start_split = i
    print(i, sent[i], delimiter_indice)


# In[126]:


sent[0:-1]

