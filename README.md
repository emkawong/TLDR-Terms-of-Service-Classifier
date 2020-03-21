# Too Long; Didn't Read
#### 

## Table of contents

This project can be broken down into two main sections: Classification and Generation, feel free to skip to the section that is most pertinent to your interests. 

1. [Introduction](#introduction)
2. [Data Preparation](#dataprep)
3. [Text Classification](#classification)
    1. [Validation](#validation)
    2. [Results](#results)
4. [Text Generation](#generation)
5. [Application](#application)
    1. [Data Visualization](#dataviz)
    2. [Website](#website)

## A Wall of Words: An Introduction <a name="introduction"></a>

The last time I read the full terms of service (TOS) for any of the product I use is - never - and I believe that I am not the only one. As our data becomes more and more valuable, it becomes more and more important that we know where that data goes and how it's being used. Below are two terms of service taken trom Terms of Service: Did Not Read, a website where contributors write brief summaries and label individual terms as good, neutral, bad, or blocker. The first is a TOS from youtube, the second from Google.

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/Youtube.png "Less Good")
![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/Google.png "Good")
<img src="https://github.com/emkawong/capstone2/blob/master/src/images/Google.png" width="200" height="200">

My mission was to take these individual TOS, take the labels that were provided, and build a model that could classify the TOS into good, bad, or neutral (blocker was grouped into bad as it was too small to classify). After classifying the terms and giving an explainable probability of "badness," I generate an abstractive summary of that term. 

## 1. TFIDF (TFiddy) or Count (VonCount): Thinking about Cleaning <a name="dataprep"></a>

The data from TOS;DR is easily accessible through their API and also available in their github in individually saved json files. After spending some time pulling and organizing data, I wrangled all of the information into one pandas dataframe. The "dirty" work can all be viewed in my notebook. From that dataframe, for this project I was only interested in two columns. The "document" column that contained all of the 2,549 TOS that were pulled from the website along with the "label" column that contained information on whether that TOS was "good","neutral", or "bad" from the perspective of the contributors to the TOS;DR website.

As is the case with all NLP projects, I had to parse and clean the text. Below is a picture of what that before and after looks like:

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/cleanup.png "Clean Text")

After parsing the text, I need to vectorize my words so that a model could cleanly intepret the words. I considered two options, a simple counter or a Term Frequency - Inverse Document Frequency (TF-IDF) weighted counter. When using words as features in a model, the words have to be transformed so that every word that appears in the entire corpus (corpus = all of my terms of service) is represented by a number. 

With a simple counter approach, that representative number would be how many times a word appears in that document. With TF-IDF, we want to also get a sense of the importantness of a word given how unusual it is in the corpus. 

To run through an example: If the word "arbitration" is used 1 time in a 20 word document, Term Frequency will be "low" at (1/20) and if it is used 10 times in a 20 word document the Term Frequencey will be "high" at (1/2). If "arbitration" is used in 19 documents within a 200 document corpus, the IDF will be higher at log(200/20) = 1 than if it is used 1 times within a 200 document corpus at log(200/2)= 2. So a high TF-IDF of 1 (1/2 * 2) would be if arbitration was used frequently in a document and if it was very rare.

My hypothesis going in was that the TF-IDF would be more useful for me because I was hoping that certain unique words would be better signals for my model and that hypothesis was correct! But only by a little (increase in accuracy of 2%), luckily voncount the count vectorizer will return later.

<img src="https://github.com/emkawong/capstone2/blob/master/src/VonCount.jpeg" alt="Sad_Count" style="width:300px;height:300px;">

A couple of other parameters I included: 
 - stopwords - all indications of the company as I felt that there may be some data leakage if all of one company's policies were bad - then the model would learn that "faceco" was a strong indication of a negative classification. 
 - an N-gram range of (1,2), so that phrases like "may retain" and "not retain" could be differentiated a little better. Surprisingly, this did not have a large effect, I hypothesize that the legalize from a company that wants to retain information will be very different from a company that does not - I explore this a little more later.

## 2. The Glass Slipper: Choosing a Model

The quick, go-to model for text classification is Naive Bayes. A model that is based on the "naive" assumption that each word is independent. In general, naive bayes is considered a good baseline but tends to not be the most accurate model. It works well with a small or a very large corpus, and as my corpus is relatively small, I hoped to get good results! I specifically used the multinomial Naive Bayes model as I was working with multiclass data.

Here is the Naive Bayes equation, it is simple but the equation can look a little messy:

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/MNB1.png "MNB1")
![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/MNB2.png "MNB2")

For that reason, I wrote out a simplified version that has helped me make sense of the different moving parts. Below is the equation for the probability that a document is good given all the words that are inside it. 

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/Good-Full%20Example.png "Good-Full Equation")

There are three main pieces here, that I've split up even further and color coded. To summarize, the probability of a specific document being good is the probability of any document being good multiplied by the probability that each word in that document is individually good. 

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/Good-Breakdown.png "Good-Breakdown")

After the probability is calculated for each class, the highest probability is chosen as the classifier. 

#### Results

Here's an example of a correctly calculated TOS (Acual:"Bad" & Predicted:"Bad")

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/AccuratePredict.png "Correct TOS")

Here's an example of an incorrectly calculated TOS (Acual:"Good" & Predicted:"Bad")

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/InaccuratePredict.png "Incorrect TOS")

For being a "naive" model, the results are pretty good! Below is the confusion matrix that calculates the number of Predicted vs. Actual documents for the three classes. The areas where I correctly predicted are darker. The area that I was the most concerned about is the portion that I've labeled the danger zone, for those are the ones that were labeled "bad" and I identified as "good" or "neutral".

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/ConfusionMatrix.png "Confusion Matrix")
 
This brings me to my AU-ROC curve that I calculated in the One Vs All method. Since ROC curves are plotted to show the tradeoff between the True Positive and True Negative Rate of two classes, I needed an approach that would allow me to plot my multiclass classifier. 

With One Vs All, what I've done is to train the model three times with Bad Vs Good&Neutral, Good Vs Bad&Neutral, and Neutral Vs Good&Bad. This is easier than classifying the data into three distinct classes so the AUC (Area Under Curve) turns out to be pretty high. 

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/MNBROC.png "MNB-ROC")

I experimented with Logistic Regression, Random Forests, and Gradient Boosting, but they all took longer and they were worse models. I've attached one more ROC plot for Random Forests which was one of the best in comparison, but still worse than Naive Bayes. 

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/RandomForestROC.png "RandomForest-ROC")

#### A Side Quest: Finding the Magic Words

VonCount returns! One obvious question that popped in my mind is to explore why Naive Bayes works well. Since it is a simple model that is completely dependent on words, then those words must be pretty important! I used the Count Vectorizer to create one more metric - distinctness. 

The formula is simple (and the original reference is posted below). Divide the number of times a word appears in a class (to the power of anything from 1 to 2 depending on how much very uncommon words should be penalized) divided by the total number of time that word appears. After doing so for each class, I have attached the top 15 words below. 

Good:

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/GoodWords.png "Good Words")

Neutral:

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/NeutralWords.png "Neutral Words")

Bad:

![alt text](https://github.com/emkawong/capstone2/blob/master/src/images/BadWords.png "Bad Words")


## 3. Explain The Terms Like I Am 5

So now I've classified the terms of service into good, neutral, 

## Resources:

Essential resources to help me with this project:

Resources for understanding:

https://web.stanford.edu/~jurafsky/slp3/slides/7_NB.pdf
https://web.stanford.edu/~jurafsky/slp3/5.pdf
https://www.cs.waikato.ac.nz/ml/publications/2004/kibriya_et_al_cr.pdf

Resources for translating understanding into code:

https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html


