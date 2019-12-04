from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn import svm
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
import codecs
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
#from skmultilearn.problem_transform import ClassifierChain

def loadData(fname,tag,reviews,labels):
    f=open(fname,encoding='utf8',errors='ignore')
    for line in f:
        review=line.strip().lower().split('\t')
        if len(review)<2: continue
        if review[1]=='na' or len(review[1])==0:
            #print(review)
            continue 
        reviews.append(review[1].lower())    
        labels.append(tag)
    f.close()
    
def loadAbs2(fname,reviews,labels):
    f=open(fname,encoding='utf8',errors='ignore')
    for line in f:
        review=line.strip().lower().split('\t')
        #print(review)
        if len(review)<2: continue
        if review[1]=='na' or len(review[1])==0: continue 
        reviews.append(review[1].lower())    
        labels.append(review[5].lower())
    f.close()

def findmax(vote):
    tmpx=''
    maxv=0
    for x in vote:
        if vote[x]>maxv:
            tmpx=x
            maxv=vote[x]
    return tmpx

reviews=[]
labels=[]
loadData('cse_train.txt','cse',reviews,labels)
loadData('siggraph_train.txt','siggraph',reviews,labels)
loadData('sigir_train.txt','sigir',reviews,labels)
loadData('www_train.txt','www',reviews,labels)
loadData('chi_train.txt','chi',reviews,labels)
loadData('cikm_train.txt','cikm',reviews,labels)
loadData('kdd_train.txt','kdd',reviews,labels)


rev_test=[]
labels_test=[]
loadData('cse_test.txt','cse',rev_test,labels_test)
loadData('siggraph_test.txt','siggraph',rev_test,labels_test)
loadData('sigir_test.txt','sigir',rev_test,labels_test)
loadData('www_test.txt','www',rev_test,labels_test)
loadData('chi_test.txt','chi',rev_test,labels_test)
loadData('cikm_test.txt','cikm',rev_test,labels_test)
loadData('kdd_test.txt','kdd',rev_test,labels_test)

#print(labels_test)
counter = CountVectorizer(stop_words='english')
counter.fit(reviews)

#print(counter)
counts_train = counter.transform(reviews)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

tfidf_transformer  = TfidfTransformer(use_idf=False).fit(counts_train)
X_train_tfidf = tfidf_transformer.fit_transform(counts_train)
X_test_tfidf = tfidf_transformer.fit_transform(counts_test)

print('X_train_tfidf',X_train_tfidf)
print('X_test_tfidf',X_test_tfidf)

mb = MultiLabelBinarizer()
labels_train = mb.fit_transform(labels)
labels_test = mb.fit_transform(labels_test)

clf = OneVsRestClassifier(LogisticRegression(),n_jobs=-1)
clf.fit(counts_train,labels_train)
pred = clf.predict(counts_test)

s=accuracy_score(pred,labels_test)
print (s)