# File to store constants

actions_movement = {'die' : 0, 'fall' : 0, 'hurt' : 0, 'idle' : 0, 'jump' : 1, 'run' : 1, 'slide' : 1, 'walk' : 1, 'say': 0}
#word2vec similarity between the incoming action vs the ones we have in list of actions and then set a threshold and execute the action based on it