'''This script conducts an election using the Instant Runoff Voting system. The test data used is the set of ballots from the Pollokshields ward
   in the 2017 Glasgow City Council Election. 
'''

import numpy as np
import ballot_data as bd

def update_ballots(ballots, to_eliminate = 3):
    if isinstance(ballots,np.ndarray):
        updated_ballots = ballots.tolist() # Want to use list methods for this copy of "ballots"
    else: 
        updated_ballots = ballots
    for ballot in updated_ballots:
        for candi in ballot:
            # For each ballot in the list of ballots and for each candidate on the ballot...
            if candi == to_eliminate:
                ballot.remove(candi)
                ballot.append(0)
    return updated_ballots


def vote_transfers(previous_ballots, updated_ballots):
    
    # We want to compute the difference between previous and updated ballots in first place votes for each candidate
    # So we may first compute the number of first place votes for each candidate in each set of ballots
    candidates, original_first_place_votes =  bd.count_votes(np.array(previous_ballots), preference=0, sort_by='candidate')
    updated_first_place_votes = bd.count_votes(ballots=np.array(updated_ballots), preference=0, sort_by='candidate')[1]
    vote_diffs = np.array(updated_first_place_votes) - np.array(original_first_place_votes) 

    # Next, we count the number of discarded ballots post-update
    # This is equivalent to counting the number of entries in updated_ballots that are equal to [0,0,...,0,0],
    # where the length is equal to the number of candidates
    discarded_diff = 0
    discardable_ballot = np.zeros(len(updated_ballots[0]))
    for ballot in updated_ballots:
        if (np.array(ballot) == discardable_ballot).all():
            discarded_diff += 1

    return candidates, vote_diffs, discarded_diff


def eliminate_next(ballots, already_eliminated = np.array([])): 
    """ This function determines which candidate to eliminate for a given set of ballots.
        When called in the run_election() function, this functions need to remember which
        candidate was previously eliminated. This is given by the second argument, which
        gets updated by each run of this function inside run_election().
    """
    # Initialise a while loop to keep going until ties are resolved.
    i = 0
    ties = True
    relevant_candidates = np.setdiff1d(np.arange(ballots[0].size), already_eliminated) # REMARK: Could have written the function with this as boolean.
                                                     # Logic would have been slightly different but it is an alternative.
    
    while ties == True:

        # On each iteration of this loop, extract votes of all candidates at preference i
        votes = np.array(bd.count_votes(np.array(ballots), preference=i, sort_by='candidate')[1])

        # Update the relevant_candidates with those who are tied at the current preference
        # Only compare the votes at preference i for the candidates who were tied at the (i-1)th preference,
        # and update relevant_candidates with any entries that were already there on the previous run
        relevant_candidates = np.intersect1d(np.where(votes == np.min(votes[relevant_candidates]))[0], relevant_candidates)

        if relevant_candidates.size > 1: # Condition for ties at a given stage
            if i == np.size(votes) - 1:
                print('That is unlikely!')
                return relevant_candidates[0] + 1 # On the off-chance that all there are candidates with equal votes at all preferences,
                                        # the candidate to be eliminated is the one with smallest index.
            i += 1

        else: # No ties, which means relevant_candidates has one unique entry
            ties = False 
            return relevant_candidates[0]+1
    


def run_election(ballots, display = False):
    """For a given set of ballots, this function runs the election until a single candidate is declared the winner based on instant run-off voting (IRV)."""

    eliminated = np.array([])
    run = 1

    while np.size(eliminated) < len(ballots[0]) - 1: # Keep going as long as there are candidates to eliminate
        
        to_eliminate_next = eliminate_next(ballots, already_eliminated = eliminated-1) # For each set of ballots and given some eliminated candidates, find out whom to eliminate next
        eliminated = np.append(eliminated, to_eliminate_next) # Modify the list of already eliminated candidates

        new_ballots = np.array(update_ballots(ballots, to_eliminate=to_eliminate_next)) 
        
        if display == True:
            candidates, vote_diffs, discarded_diff = vote_transfers(ballots, new_ballots)
            print(f'For run {run}, the difference in first-place votes sorted by candidate is: {vote_diffs}. {discarded_diff} votes were discarded.')
   
        ballots = new_ballots # Update ballots variable for the next run
        run += 1
    winner = np.setdiff1d(candidates, eliminated)

    if display == True:
        print(f'The winner of this election is: {winner}. Candidates {eliminated} were eliminated.')

    return winner, eliminated 


# Run the election using the ballots from the Pollokshields ward in the 2017 Glasgow City Council Election 
# The candidates are numbered by integers in this script and correspond to the original candidates as follows:
# 3: Macleod (SNP)
# 4: Conservative
# 6: Raja (Labour)
# 5: Green
# 7: Riaz (SNP)
# 8: Thomas (Labour)
# 2: Lib Dem
# 1: UKIP
test_ballots = np.loadtxt('pollokshields_2017.txt', dtype=int)
winner, eliminated = run_election(test_ballots, display=True)

