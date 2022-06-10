# A way to evaluate RuleAgentChromosome
# The objective of this class is that it could easily be extended 
# into a genentic algorithm engine to improve chromosomes.
# M. Fairbank. October 2021.
import sys
from hanabi_learning_environment import rl_env
from rule_agent_chromosome import MyAgent
import os, contextlib
import random
import numpy as np



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

def del_mutation(chromosome):
    chromosome.remove(random.choice(chromosome))
    while (len(chromosome)) < 7:
        num = random.randint(0, 12)
        if num not in chromosome:
            chromosome.append(num)
    return chromosome

def swap_mutation(chromosome):
    pos_a, pos_b = random.randint(0, len(chromosome) - 1), random.randint(0, len(chromosome) - 1)
    chromosome[pos_a], chromosome[pos_b] = chromosome[pos_b], chromosome[pos_a]
    while (len(chromosome)) < 7:
        num = random.randint(0, 12)
        if num not in chromosome:
            chromosome.append(num)
    return  chromosome



if __name__=="__main__":

    num_players=4
    population = [random.sample(range(0, 12), 9) for i in range(200)]
    best_chromosomes={}
    next_population=[]
    parents=[]
    highest_score=[]
    score=[]
    outputs=[]
    iterations = 100
    best_fitness = 0

    for generation in range(iterations):
        print("generation - ", generation)
        parents_for_crossover = []
        parents = []
        highest_score_for_generation = 0
        score = []
        total_reward = 0.0
        if next_population:
            population=next_population.copy()
            next_population=[]
        # evaluate the chromosomes...
        for i in range(len(population)):
            chromosome=population[i]
            if 5 and 6 not in chromosome:
                chromosome[random.randint(0,len(chromosome)-1)], chromosome[random.randint(0,len(chromosome)-1)] = 5, 6
            # result = run(20, num_players, chromosome)
            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stdout(devnull):
                    result=run(25,num_players,chromosome)
            print("chromosome",chromosome,"fitness",result)

            total_reward += result

            if result>highest_score_for_generation:
                highest_score_for_generation = result

            if result>=best_fitness:
                best_fitness=result
                best_chromosomes={}
                best_chromosomes[result]=chromosome

            parents.append(chromosome)
            score.append(result)

        highest_score.append(highest_score_for_generation)

        parents_for_crossover = list(zip(score, parents))
        parents_for_crossover = sorted(parents_for_crossover, reverse=True)
        next_population = list(list(zip(*parents_for_crossover))[1][:4])

        # continue with the rest of parents for the crossover...
        parents_for_crossover = list(list(zip(*parents_for_crossover))[1][5:])
        outputs.append(total_reward/len(population))
        if generation != iterations:
            # select two parents for crossover...
            for p in range(31):
                selected_parents = random.sample(parents_for_crossover, 2)
                # crossover
                crossover_part1 = selected_parents[0][:int(len(selected_parents[0]) / 2) + 1]
                crossover_part2 = selected_parents[1][int(len(selected_parents[0]) / 2):]
                first_child = crossover_part1 + crossover_part2
                first_child = [i for n, i in enumerate(first_child) if i not in first_child[:n]]

                # The below functions will be called on the chromosome randomly but with equal probability (only one gets called per chromosome).
                action = np.random.choice([1, 2], p=[1/2, 1/2])
                if action == 1:
                    first_child = del_mutation(first_child)
                else:
                    first_child = swap_mutation(first_child)

                # move the individual to the next generation
                next_population.append(first_child)

    print("best chromosome", best_chromosomes)


    import matplotlib.pyplot

    matplotlib.pyplot.plot(outputs)
    matplotlib.pyplot.xlabel("Iteration")
    matplotlib.pyplot.ylabel("Avg Fitness")
    # matplotlib.pyplot.show()
    matplotlib.pyplot.savefig('AvgFitness.png')

    matplotlib.pyplot.plot(highest_score)
    matplotlib.pyplot.xlabel("Iteration")
    matplotlib.pyplot.ylabel("Highest Score")
    # matplotlib.pyplot.show()
    matplotlib.pyplot.savefig('HighestScore.png')











