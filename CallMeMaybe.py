Project : 


                                                                Call Me Maybe ??


---------------------------------------------
Human text
   ↓
Tokenizer
   ↓
Token IDs (numbers)
   ↓
Vectors (embeddings)
   ↓
Neural network computations
   ↓
Token IDs
   ↓
Tokenizer
   ↓
Human text
-------------------------------------------


1) What is an llm

        1) data + Architicture + Training
           Text +   Attention  +  Changing Parametters until gave the good result.


2) What are weights:

    they are the responsible of gaving the next word using training,and in training we keep changing the Parametters until we get the good result.




3) What are the steps the llm uses to decide the next word:
        Text → Tokens → Embeddings(Vectors) → Attention & Transformations → Probabilities → Next Token → Repeat.


4) What are Embeddings
    it is to encode all the tokens to became a Matrix contain vectors that each vector represent the token.

5) How the tokenizor works
        Break text to tokens -> convert tokens to IDs -> convert IDs back into text when the model gener3ate answer.



6) What is Neural network?



What is a tensor 
What are transformers what are layers
What's the difference between ai agent and an llm

AI vs machine learning vs deep learning 
neural network
how to train ur deep learning model 
(, layers , logits, activation functions, weighted sum , loss function  )


what is generative AI
what is llm vs nlp 
what is transformer and self attention
(what is tokenization, embedding)


what is constrained decoding 



step 1 run the model (let it generate normally )



dont run the method of get_logits more often (only use it when necessary )


The flow of GPT:  is everty thing is about the transformer ?


                    Transformer

 1) input: Hello.
 2) the input broken to tokens, it could be word , subword or char's depending on the vocabulary of the model
 3) Embedding : each token will be encoded and becames a vector , in the end we do have a matrix (tensor) of vectors .
 
 4) attention block. the vectors communecate whit each other to understad the meaning of each word depennding
  on the context.
 
 5) Multilayer Perceptron. in this step vectors they do not talk to each othere why just pass in the same process of answering some questions which will change the values of the numbers in the vector's depending on the answer.
 6) repeating the 4 & 5 steps mutiple time untill the last vector will be close to gave us the next word.



