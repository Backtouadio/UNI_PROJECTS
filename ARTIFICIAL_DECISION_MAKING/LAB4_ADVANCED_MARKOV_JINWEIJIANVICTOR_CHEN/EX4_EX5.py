import numpy as np
from hmmlearn import hmm

# Define an HMM with 3 hidden states: S = { s_0= alone, s_1=acoompanied, s_2=interacting }
# Categorical HMM used for categorical discrete observations
model = hmm.CategoricalHMM(n_components=3) #number of states

# Initial hidden state probabilities, maybe because the entry points are mostly alone floors
model.startprob_ = np.array([0.8, 0.1, 0.1])

# Transition probabilities
model.transmat_ = np.array([
    [0.3, 0.5, 0.2],  # alone -> [alone, acoompanied, interacting]
    [0.3, 0.2, 0.5],  # acoompanied -> [alone, acoompanied, interacting]
    [0.3, 0.5, 0.2]   # interacting -> [alone, acoompanied, interacting]
])

# Possible observations are combinations of body face and voice detected
# O_body = {yes,no}
# O_face= {yes,no}
# O_voice = {yes,no}
# Encoding multiple discrete observations (O_body x O_face x O_voice):
# O_0 = {body_yes,face_yes,voice_yes}--> state 3 (interacting)
# O_1 = {body_yes,face_yes,voice_no}--> state 2 (accompanied)
# O_2 = {body_yes,face_no,voice_yes}--> state 3 (interacting)
# O_3 = {body_yes,face_no,voice_no}--> state 2 (accompanied)
# O_4 = {body_no,face_yes,voice_yes}--> state 1 (alone) it's impossible
# O_5 = {body_no,face_yes,voice_no}--> state 1 (alone) it's impossible
# O_6 = {body_no,face_no,voice_yes}--> state 1 (alone) it's impossible
# O_7 = {body_no,face_no,voice_no}--> state 1 (alone) 


# Emission probabilities
model.emissionprob_ = np.array([
    [0.02,0.08,0.02, 0.08, 0.2, 0.2, 0.2, 0.2],  # alone -> [O_0, O_1, O_2, O_3, O_4, O_5, O_6, O_7]
    [0.15,0.3,0.15, 0.3, 0.025, 0.025, 0.025, 0.025], # acoompanied -> [O_0, O_1, O_2, O_3, O_4, O_5, O_6, O_7]
    [0.4,0.05,0.4, 0.05, 0.025, 0.025, 0.025, 0.025]       # interacting -> [O_0, O_1, O_2, O_3, O_4,O_5, O_6, O_7]
])

observations = np.array([[4,7,1,3,2,1,6,7]]).T #number can be defined by you
log_prob = model.score(observations)
print(f"log_prob: {log_prob}")
post_prob = model.predict_proba(observations)
print(f"post_prob: \n{post_prob}")
seq = model.predict(observations)
# Output the predicted sequence of hidden states
#print(f"sequences: \n{seq}")
