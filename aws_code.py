#!/usr/bin/env python
# coding: utf-8

# In[50]:


import requests
import json


# In[51]:


import os
import pandas as pd
import numpy as np


# In[52]:


abs_path = r"C:\Users\aknhom4471\Desktop\email_bot\test_data"


# In[58]:


test_data = pd.read_excel(os.path.join(abs_path, "accuracy_case_16092020.xlsx"))


# In[59]:


len(test_data)


# In[54]:


test_data.head()


# In[55]:


test_data['char_len'] = test_data['Sample mails'].str.len()


# In[56]:


len(test_data)


# In[57]:


len(test_data[test_data['char_len']<=256])


# In[11]:


test_data['direct_request'] = np.where(
    test_data['char_len']<=256,
    1,
    0
)


# In[28]:


test_data.to_csv(os.path.join(abs_path, "test_data.csv"), index= False, encoding = "utf-8")


# In[14]:


test_data[test_data['char_len']<=256]['Sample mails'][1]


# In[24]:


email = "Dear team Kindly update my email I'd in my max life insurance policy.my email id is UDAYR5621@GMAIL.COM MY CONTACT NUMBER IS -9129669288 Policy name is uday raj Address - siddhaur barabanki"


# In[25]:


url = "https://yff7hxzhi2.execute-api.ap-south-1.amazonaws.com/Prod/?email={}".format(email)


# In[28]:


import datetime as dt
from datetime import datetime
start = datetime.datetime.now()
response = requests.get(url)
print(datetime.datetime.now()-start)


# In[7]:


response.__dict__


# In[21]:


response_content = json.loads(response.content.decode("utf-8")) 


# In[22]:


response_content


# In[23]:


def get_intent_aws(row):
    email = row['Sample mails']
    url = "https://yff7hxzhi2.execute-api.ap-south-1.amazonaws.com/Prod/?email={}".format(email)
    response = requests.get(url)
    response_content = json.loads(response.content.decode("utf-8")) 
    return response_content['intent_predicted'], response_content['intent_confidnece']


# In[24]:


temp_test_data = test_data[test_data['char_len']<=256]


# In[25]:


temp_test_data[['intent_predicted', 'intent_confidence']] = temp_test_data.apply(get_intent_aws, axis=1, result_type = 'expand')


# In[38]:


temp_test_data['Category']=np.where(
    temp_test_data['Category'] == "finance/premium receipt/consolidated_premium_payment_request/soft_copy",
    "finance/premium_receipt/consolidated_premium_payment_request/soft_copy",
    temp_test_data['Category']
)


# In[40]:


temp_test_data['match'] = np.where(
    temp_test_data['Category'] == temp_test_data['intent_predicted'],
    1,
    0
)


# In[41]:


temp_test_data['match'].value_counts()


# In[47]:





# In[48]:


category = set(list(temp_test_data['Category']))


# In[49]:


predicted_intent = set(list(temp_test_data['intent_predicted']))


# In[50]:


len(category), len(predicted_intent)


# In[51]:


union = category.union(predicted_intent)


# In[52]:


len(union)


# In[ ]:





# In[42]:


temp_test_data.columns


# In[44]:


temp_test_data_grouped = temp_test_data.groupby('Category')['match'].agg(['count', 'sum']).reset_index()


# In[45]:


temp_test_data_grouped['accuracy'] =  temp_test_data_grouped['sum']*100.0/temp_test_data_grouped['count']


# In[46]:


temp_test_data_grouped


# In[6]:


temp_test_data.to_csv(os.path.join(abs_path, "temp_test_data.csv"), index= False, encoding = "utf-8")


# # temp test data analysis

# In[60]:


test_data = pd.read_excel(os.path.join(abs_path, "temp_test_data.xlsx"), sheet_name = "jupyter_read")


# In[9]:


test_data.columns


# In[12]:


test_data['Category'] = np.where(
    (test_data['validation'] ==3),
    test_data['intent_predicted'],
    test_data['Category']
)


# In[13]:


test_data['ground_truth'] = np.where(
    (test_data['validation'] ==1) | (test_data['validation'] ==3),
    test_data['intent_predicted'],
    np.where(
        test_data['validation'] ==0,
        test_data['Category'],
        test_data['ground_truth']
    )
)


# In[14]:


test_data = test_data[test_data['validation']!=2]


# In[19]:


test_data['ground_truth'].value_counts().reset_index()['ground_truth'].sum(), len(test_data['ground_truth'])


# In[20]:


test_data['match_sen_vs_dialog'] = np.where(
    test_data['Category'] == test_data['intent_predicted'],
    1,
    0
)
test_data['match_ground_vs_dialog'] = np.where(
    test_data['ground_truth'] == test_data['intent_predicted'],
    1,
    0
)
test_data['match_ground_vs_sen'] = np.where(
    test_data['Category'] == test_data['ground_truth'],
    1,
    0
)


# In[21]:


test_data.columns


# In[22]:


test_data['sense_sen_cnt'] = test_data.groupby('Category')['TicketID'].transform('count')


# In[27]:


test_data['sen_dialog_tp'] = test_data.groupby('Category')['match_sen_vs_dialog'].transform('sum')


# In[23]:


test_data['ground_sen_cnt'] = test_data.groupby('ground_truth')['TicketID'].transform('count')


# In[25]:


test_data['dialog_tp'] = test_data.groupby('ground_truth')['match_ground_vs_dialog'].transform('sum')
test_data['sen_tp'] = test_data.groupby('ground_truth')['match_ground_vs_sen'].transform('sum')


# In[28]:


test_data['sen_dialog_accuracy'] = test_data['sen_dialog_tp']*100/test_data['sense_sen_cnt']
test_data['dialog_accuracy'] = test_data['dialog_tp']*100/test_data['ground_sen_cnt']
test_data['sen_accuracy'] = test_data['sen_tp']*100/test_data['ground_sen_cnt']


# In[30]:


test_data.to_csv(os.path.join(abs_path, "validate.csv"), index = False)


# # sentence breaking

# In[47]:


import re


# In[61]:


chunk_path = r"C:\Users\aknhom4471\Desktop\email_bot\chunk"


# In[62]:


email_dataset = "senseforth_predicted.xlsx"


# In[ ]:



"""
objective: 
1) 256 max character
2) not too short ... yet to decide
3) meaningful 

algo:
1) split the sentence based on 256 character length as it is the pre-requisite
2) split the sentence based on punctuation
3) split the sentence based on conjuction and grammar word which helps in elongating the sentence and add
additional info
steps:
1) take all the emails and break the emails with 256 char and see how many excerpts are created on average
2) if the excerpt count is less than find the patterns else use the above algo
merge the sente

breaking the sentence with `and` & ` also is must even though we get the signle or very small word length


step 1 so first split the word with list of selected words and then iterate over the list and assign character length to them
 give priority to and over also

but splitting a sentence with full stop is not a good decision as it is generally used  with short forms and it is
possible that there is a space after it

 we can make a parsing logic that will delete all the extra space  and has split the sentence from sentence end and not
 from short forms
 
 but any sentence left after step 1 will use step 2
 
 
 to validate check the frequency of list of words given below and puntuations that in a single sentence how many of them comes 
 and then after splitting with step 1 how many sentences are left with string greated than 256
 
 
 afte this dialogflow modedl trarining must be done accoriding to this covering various scenarios and cleaning the data
 at the same time
 
 an additional sentence similarity logic must be written to remove unnecessary sentence from the training dataset
 
"""


# In[31]:


"""
if nothing works which is rare we can revers engineer the logic of senseforth sentence breaking which according to me
is not the best one either


create a intent name greeting or remove these set of words from string
"""


# In[ ]:


grammar_words = ['and', 'also', 'alongwith', 'along with', ]
extra_words = ['but', 'for', 'nor', 'so', 'yet', 'which', ]
punctuation = [",", ";", "."]


# In[34]:


temp_check = "split the sentence based on 256 character length as it is the pre-requisite"


# In[6]:


email_data = pd.read_excel(os.path.join(chunk_path,email_dataset))


# In[7]:


email_data.columns


# In[8]:


email_data = email_data.drop(['Datetime', 'Predicted_Intent', 'ticketID'], axis = 1)


# In[9]:


email_data = email_data.dropna(subset=['Email_body']).drop_duplicates()


# In[10]:


len(email_data)


# In[11]:


email_data.columns


# In[33]:


email_data_grouped = email_data.groupby('Email_body')['Excerpt'].apply(list).reset_index()


# In[34]:


email_data_grouped.head()


# In[189]:


import itertools

def sen_len(row):
    text_list = row['sentences']
    sentence_length = []
    for item in text_list:
        sentence_length.append(len(item))
    return sentence_length, len(text_list), max(sentence_length)

def remove_nesting(text_list):
    output = list(itertools.chain.from_iterable(text_list))
    return output

def split_lines(text):
    lower_text = text.lower()
    text_list = lower_text.splitlines()
    split_list = [i.split('and') for i in text_list]
    split_list = remove_nesting(split_list)
    split_list = [i.split('also') for i in split_list]
    split_list = remove_nesting(split_list)
    split_list = [i.split('alongwith') for i in split_list]
    split_list = remove_nesting(split_list)
    split_list = [i.split('along with') for i in split_list]
    output = remove_nesting(split_list)
    clean_list = [i for i in output if i]
    return clean_list

# def remove_greetings(text_list, greet_list):
#     """
#     check later
#     """
#     updated_list = []
#     for item in greet_list:
#         for check in text_list:
#             if item in check:
#                 break
#             else:
#                 updated_list.append(check)
#     return updated_list


# In[190]:


email_data_grouped['sentences'] = email_data_grouped['Email_body'].apply(split_lines)


# In[124]:


# email_data_grouped['sentences'] = email_data_grouped['Email_body'].str.split(pat='\n')


# In[191]:


email_data_grouped[['sentence_length', 'num_of_sentence', 'max_sent_len']] = email_data_grouped.apply(sen_len, axis=1, result_type = 'expand')


# In[135]:


email_data_grouped[email_data_grouped['max_sent_len']>=256].to_csv(os.path.join(chunk_path, "chunk_analysis.csv"), index = False)


# In[192]:


email_data_grouped[email_data_grouped['max_sent_len']<256].to_csv(os.path.join(chunk_path, "chunk_analysis_fine.csv"), index = False)


# In[194]:


len(None)


# In[132]:


email_data_grouped[email_data_grouped['max_sent_len']>=256]


# In[96]:


total_emails = len(email_data_grouped)


# In[134]:


10099/total_emails 


# In[89]:


total_emails


# In[18]:


temp_str = "\n\nHi,\nNo such request raised my me.\nPlease check and confirm\n"
greet_list = ["hi", 'dear']


# In[13]:


print(temp_str)


# In[ ]:


temp_str


# In[27]:


chunks = split_lines(temp_str)


# In[28]:


chunks


# In[29]:


clean_chunks = remove_greetings(chunks, greet_list)


# In[30]:


clean_chunks


# In[14]:


temp_str.l


# In[74]:



temp1 = """As required, I have uploaded all the necessary documents on the online portal. Please note that while I have submitted the details of the life term insurance policies that are active for me as of now in the online proposal, I was not able to submit the details of a some additional policies due to the fact that your online portal proposal form takes up only upto 5 entries. After having exhausted the 5 entries, I was unable to enter the other policy details which I am giving as under:- 1. Insurer name : HDFC Life Sum assured : 2.1 Crores Status. : Lapsed I did not make the payment Type : Life 2. Insurer Name : LIC Sum assured : 19.1 lacs spread over 2 policies Status : Active in force Type : Pension and Endowment 3. Insurer Name : HDFC Life Sum assured : 14.9 lacs Status : Active in force Type : ULIP 4. Insurer name : Bajaj Allianz Cover : 10 lacs Status : Active in force Type : Health floater for family, covers upto 10 lacs post the initial own spend of Rs 3 lacs Please consider the same when you are evaluating the insurance proposal for my self."""


# In[61]:


t1 = split_lines(temp1)


# In[75]:


text_list = temp1.lower().splitlines()


# In[76]:


text_list


# In[77]:


split_list = [i.split('and') for i in text_list]


# In[78]:


split_list


# In[79]:


output = remove_nesting(split_list)


# In[80]:


output


# In[140]:


import itertools

def sen_len(row):
    text_list = row
    sentence_length = []
    for item in text_list:
        sentence_length.append(len(item))
    return sentence_length, len(text_list), max(sentence_length)

def split_lines(text):
    lower_text = text.lower()
    text_list = lower_text.splitlines()
    split_list = [i.split('and') for i in text_list]
    split_list = remove_nesting(split_list)
    split_list = [i.split('also') for i in split_list]
    split_list = remove_nesting(split_list)
    split_list = [i.split('alongwith') for i in split_list]
    split_list = remove_nesting(split_list)
    split_list = [i.split('along with') for i in split_list]
    output = remove_nesting(split_list)
    clean_list = [i for i in output if i]
    return clean_list


# In[175]:


def further_split(text, splitter = '.'):
#     res_list = []
#     if len(text)<256:
#         res_list.append(text)
#     else:
    temp_res = text.split(splitter)
    for item in temp_res:
        if item.strip().isnumeric() or item.strip() == '':
#             print(item)
            temp_res.remove(item)
    return temp_res  


# In[ ]:





# In[170]:


t2 = "1.I would like to cancel my policy ; as I received illustration mail in this email ID anusuyajoseph312@gmail.com 2.Mailed for cancellation with in freelook period . 3.Since I got my posting in different city out of connectivity for some time 4.kindly accept my request for my policy cancellation . 5.ticket number 3057116. Requesting you to cancel my policy as soon as possible."


# In[182]:


t3 =  "257910802,257910828 Samita chauhan Respected sir this letter for my daughter policy please consider this letter as a request to cancel life insurance because I m not in india I want refund my money to my india account my dad is in india I will give authority to my father u can tell me how do process I call so many time agent they r not responding properly I realy thanking sir pls help me for this m calling him since 3 years That&#8217;s insurance my daughter after my husband died but I can&#8217;t give payments more so pls request for my fund."


# In[195]:


t4 = """\nMadam/ Dear Sir,\n\nCANCELLATION OF ECS MANDATE\nMAX LIFE INSURANCE POLICY\nNO.795314137  SHIKSHA PLUS-II \nREFUND OF CHARGES OF Rs.295/-\nLEVIED FOR FAILED ECS MANDATE\n\nI had the captioned Max Life Insurance Policy and same was surrendered/ closed on 28.09.2016. I had also applied for cancellation of ECS mandate on 28.09.2016. Now after 3 years of closure of my policy, my account has been debited for Rs.295/- on 15.07.2019 towards charges for failed ECS mandate, which may be incorrect. Kindly arrange to verify and refund of Rs.295/- which might be erroneously debited from my account. And also kindly arrange to cancel my ECS mandate, if it is not yet cancelled.\nKindly do the needful.\n\n\n\n"""


# In[196]:


excerpts = split_lines(t4)


# In[197]:


excerpts


# In[184]:


for sent in excerpts:
    if len(sent)<256:
        pass
    else:
        temp_sent = sent
        excerpts.remove(sent)
        excerpts.extend(further_split(temp_sent))


# In[185]:


excerpts


# In[186]:


_, _1, max_sen_len = sen_len(excerpts)


# In[187]:


max_sen_len


# In[ ]:


for 


# In[ ]:


if max_sen_len <=256:
    print("aws api call for all the sentences")
else:
    print("call further split")
    for sent in excerpts:
        if len(sen)<256:
            pass
        else:
            temp_sent = sent
            excerpts.remove(sent)
            excerpts.extend(further_split(temp_sent))


# In[ ]:





# cases found
# 
# 1) with punctuation (handled)
# 
# 3) with and and also type words (handled)
# 
# 3) without those words but with punctuation (handled)
# 
# 4) wihtout those words and without punctuation (logic made coding pending)
# 

# In[ ]:


"from last position start iterating till I, he, she, please, kindly occurs and 256 length not exceeded if exceeded split the
sentence from most recent detected index do this for all and add into list
"


# In[ ]:





# In[199]:


x = " we have just justinbeiber"


# In[211]:


x.split('just',3)


# In[215]:


import re
pattern = "^(.*just)(.*)$"
a = re.search(pattern, x)


# In[216]:


a.group(1)


# In[217]:


a.group(2)


# In[209]:


x.split('just')


# In[204]:


split_list


# In[8]:


response.__dict__


# In[ ]:


intent_response_excerpts [{excerpt: intent predicted confidence}, {excerpt: intent predicted confidence}]
intent_response_email	[{intent1: confidence}, {intent2: confidence}]
unparliamentary	{flag:1/0, words:[a,c,v]}
sentiment	category_name


# In[10]:


response_object = {
    "status_code":200,
    "headers":{
        "Content-Type":"application/json"
    },
    "content":""
}


# In[14]:


intent_predicted = "teleservicing/teleservicing/personal_update/email"
intent_confidence = 0.96017456054687
category_name = "general"


# In[15]:


intent_response_excerpts = [{"excerpt1": (intent_predicted, intent_confidence)}, {"excerpt2": (intent_predicted, intent_confidence)}]
intent_response_email= [{intent_predicted: intent_confidence}, {intent_predicted: intent_confidence}]
unparliamentary = {"flag":1, "words":["a","c","v"]}
sentiment = category_name


# In[34]:


res = {}


# In[35]:


res['intent_response_excerpts'] = intent_response_excerpts


# In[36]:


res['intent_response_email'] = intent_response_email


# In[37]:


res['unparliamentary'] = unparliamentary
res['sentiment'] = sentiment


# In[42]:


response_object['content'] = json.dumps(res)


# In[44]:


response_object['content'] = res


# In[45]:


response_object


# In[49]:


with open(os.path.join(chunk_path, "response.txt"), 'w') as fout:
    json_dum_str = json.dumps(response_object, indent = 4)
    print(json_dum_str, file =fout)


# needs to be discussed with media agility team the info that needs to be stored in db and how
