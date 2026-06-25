import numpy as np


def generate_ballots(votes=100, total_candidates=5, target_results=[32, 28, 21, 13, 6]):
    '''
    Generate random ballot data given a total number of ballots (votes),
    a total number of candidates, and a target probability distribution
    of preferences.
    The probabilities are randomly attributed to each candidate for each
    level of preference.
    
    Returns a NumPy array with shape (votes, candidates), where each row
    is one ranked-choice ballot for one voter, and each column corresponds
    to one candidate.
    '''
    # Initialise a random number generator
    rng = np.random.default_rng()
    
    # Set target probabilities for each stage (normalised)
    prob = np.array(target_results, dtype=float)
    prob = np.tile(prob, (total_candidates, 1))
    # shuffle probabilities so they're applied differently for each rank; add some noise too
    prob = np.abs(rng.permuted(prob, axis=1) + rng.normal(scale=2, size=prob.shape))
    
    # Create an empty array to store the ballots
    ballots = np.zeros((votes, total_candidates), dtype=int)
    
    # Create each ballot one after the other
    for v in range(votes):
        # Voter ranks at most "total_candidates" candidates; introduce "stages" for clarity
        stages = total_candidates
        for r in range(stages):
            
            # Generates rth preference for an arbitrary candidate (use normalised probabilities)
            chosen_candidate = rng.choice(total_candidates, p=prob[r, :]/prob[r, :].sum()) + 1
            
            if chosen_candidate in ballots[v]:
                # Arbitrarily decide that voter is done if they choose the same candidate twice,
                # i.e. if chosen_candidate has already been placed in row v
                break
            else:
                # If they hadn't previously chosen that candidate, choose it as rth preference (r indexes from 0)
                ballots[v, r] = chosen_candidate
    
    return ballots


def ballot_selector(ballots, candidate, preference=0):
    '''
    Returns a selector for all ballots which have ranked a given candidate at a given preference.
    '''
    return ballots[:, preference] == candidate


def count_votes(ballots, preference, sort_by = 'count'):
    candidates_votes_dict = {}
    for candidate in range(len(ballots[0])):
        candidate_selector = ballot_selector(ballots, candidate+1, preference) # Selector for current candidate being in the given preference
        candidates_votes_dict.update({candidate + 1: len(ballots[candidate_selector])}) # Count the number of votes that the current candidate got for the given preference, and add these into a dictionary
    
    # Actually, I could have done this using numpy arrays and the argsort method. Oh well.
    if sort_by == 'count': # If we are sorting by the number of votes, we must sort the dictionary values
        sorted_candidates_vote_dict = {k: v for k, v in sorted(candidates_votes_dict.items(), key=lambda item: item[1])}
        candidates = list(sorted_candidates_vote_dict.keys())
        count_votes = list(sorted_candidates_vote_dict.values())
        
    elif sort_by == 'candidate': # If we are sorting by the candidate number, we must sort the dictionary keys
        candidates = sorted(candidates_votes_dict)
        count_votes = [candidates_votes_dict[i] for i in sorted(candidates_votes_dict)]

    return candidates, count_votes








         
        
