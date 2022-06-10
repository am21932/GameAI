# A way to evaluate RuleAgentChromosome
# The objective of this class is that it could easily be extended 
# into a genentic algorithm engine to improve chromosomes.
# M. Fairbank. October 2021.
import sys
from hanabi_learning_environment import rl_env
from rule_agent_chromosome import MyAgent
import os, contextlib
import random



def run(num_episodes, num_players, chromosome, verbose=False):
    """Run episodes."""
    environment=rl_env.make('Hanabi-Full', num_players=num_players)
    game_scores = []
    for episode in range(num_episodes):
        observations = environment.reset()
        agents = [MyAgent({'players': num_players},chromosome) for _ in range(num_players)]
        done = False
        episode_reward = 0
        while not done:
            for agent_id, agent in enumerate(agents):
                observation = observations['player_observations'][agent_id]
                action = agent.act(observation)
                if observation['current_player'] == agent_id:
                    assert action is not None   
                    current_player_action = action
                    if verbose:
                        print("Player",agent_id,"to play")
                        print("Player",agent_id,"View of cards",observation["observed_hands"])
                        print("Fireworks",observation["fireworks"])
                        print("Player",agent_id,"chose action",action)
                        print()
                else:
                    assert action is None
            # Make an environment step.
            observations, reward, done, unused_info = environment.step(current_player_action)
            if reward<0:
                reward=0 # we're changing the rules so that losing all lives does not result in the score being zeroed.
            episode_reward += reward
            
        if verbose:
            print("Game over.  Fireworks",observation["fireworks"],"Score=",episode_reward)
        game_scores.append(episode_reward)
    return sum(game_scores)/len(game_scores)



def swap_mutation(chromosome, num_players, fitness, iterations, all_results):
    best_fitness = fitness
    best_chromosome = chromosome.copy()
    for i in range(iterations):
        pos1 = random.randint(0, len(chromosome)-1)
        pos2 = random.randint(0, len(chromosome)-1)
        if pos1!=pos2:
            val = chromosome[pos1]
            chromosome[pos1] = chromosome[pos2]
            chromosome[pos2] = val
            result = run(40, num_players, chromosome)
            if result > best_fitness:
                best_fitness = result
                best_chromosome = chromosome
            print("iterations - ", i, "result - ", result, "chromosome - ", chromosome)
            all_results.append(result)
    return best_fitness, best_chromosome, all_results





if __name__=="__main__":

    num_players=4
    parent_chromosome=[10, 2, 4, 12, 5, 9, 6, 1]
    all_results=[]

    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stdout(devnull):
            result = run(40, num_players, parent_chromosome)
    print("chromosome", parent_chromosome, "fitness", result)

    all_results.append(result)
    iterations = 100
    fitness = result
    best_fitness, best_chromosome, all_results = swap_mutation(parent_chromosome, num_players, fitness, iterations, all_results)
    print("best fitness", best_fitness, "best chromosome", best_chromosome)

    import matplotlib.pyplot

    matplotlib.pyplot.plot(all_results)
    matplotlib.pyplot.xlabel("Iteration")
    matplotlib.pyplot.ylabel("Score")
    # matplotlib.pyplot.show()
    matplotlib.pyplot.savefig('Score.png')






