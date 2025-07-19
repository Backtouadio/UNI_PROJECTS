import numpy as np
from hmmlearn import hmm

# Define an HMM with 3 hidden states: S = { s_0=smooth, s_1=rough, s_2=slippery }
# Categorical HMM used for categorical discrete observations
model = hmm.CategoricalHMM(n_components=3)

# Initial hidden state probabilities, maybe because the entry points are mostly smooth floors
model.startprob_ = np.array([0.8, 0.1, 0.1])

# Transition probabilities
model.transmat_ = np.array([
    [0.7, 0.2, 0.1],  # smooth -> [smooth, rough, slippery]
    [0.3, 0.4, 0.3],  # rough -> [smooth, rough, slippery]
    [0.2, 0.3, 0.5]   # slippery -> [smooth, rough, slippery]
])

# Possible observations are combinations of slip rate and vibrations
# O_slip = {low slip rate, medium slip rate, high slip rate}
# O_vibrations = {low vibrations, high vibrations}
# Encoding multiple discrete observations (O_slip x O_vibrations):
# O_0 = (low slip rate, low vibrations) -> 0
# O_1 = (low slip rate, high vibrations) -> 1
# O_2 = (medium slip rate, low vibrations) -> 2
# O_3 = (medium slip rate, high vibrations) -> 3
# O_4 = (high slip rate, low vibrations) -> 4
# O_5 = (high slip rate, high vibrations) -> 5

# Emission probabilities
model.emissionprob_ = np.array([
    [0.2, 0.05, 0.6, 0.05, 0.05, 0.05],  # smooth -> [O_0, O_1, O_2, O_3, O_4, O_5]
    [0.04, 0.5, 0.03, 0.25, 0.03, 0.15], # rough -> [O_0, O_1, O_2, O_3, O_4, O_5]
    [0.0, 0.0, 0.1, 0.1, 0.4, 0.4]       # slippery -> [O_0, O_1, O_2, O_3, O_4, O_5]
])

observations = np.array([[0,0,0,0,0,0,0]]).T
log_prob = model.score(observations)
print(log_prob)