from player import Bot
from game import State
import random


class JrPluto(Bot):
    
    def select(self, players, count):
        playerToSelect=""
        if self.game.turn==1:
            #We do not have any suspects in the first turn, hence we select Trickerton to be on our team as he has the best record in the first turn
            playerToSelect="Trickerton"
        elif self.game.turn==2:
            #Before the start of second turn, we can at max have 2 suspects as in the first turn we only play with 2 players
            if self.suspects_on_failed_mission["Logicalton"]=="No":
                playerToSelect="Logicalton"
            elif self.suspects_on_failed_mission["Trickerton"]=="No":
                playerToSelect="Trickerton"
            else:
                #If both Logicalton and Trickerton are suspects, we select Bounder to be on our team and the second player can be chosen at random from the others.
                playerToSelect="Bounder"
        elif self.game.turn==3:
            #By turn 3, Bounder really picks up and is quite tough to beat; Also by the time turn 3 starts, all the available players can be suspects at max.
            if self.suspects_on_failed_mission["Bounder"]=="No":
                playerToSelect="Bounder"
            elif self.suspects_on_failed_mission["Trickerton"]=="No":
                playerToSelect="Trickerton"
            elif self.suspects_on_failed_mission["Logicalton"]=="No":
                playerToSelect="Logicalton"
            elif self.suspects_on_failed_mission["Simpleton"]=="No":
                playerToSelect="Simpleton"
            #The below condition will select Bounder to play for us if all the players are on the suspected list
            else:
                playerToSelect="Bounder"
            
        elif self.game.turn==4:
            #Our best chance to win on round 4 is by selecting Logicalton on our team if he is not a suspect.
            if self.suspects_on_failed_mission["Logicalton"]=="No":
                playerToSelect="Logicalton"
            elif self.suspects_on_failed_mission["Bounder"]=="No":
                playerToSelect="Bounder"
            elif self.suspects_on_failed_mission["Trickerton"]=="No":
                playerToSelect="Trickerton"
            elif self.suspects_on_failed_mission["Simpleton"]=="No":
                playerToSelect="Simpleton"
            #If all the players are under suspection, then Logicalton is still our best hope
            else:
                playerToSelect="Logicalton"
        else:
            #Bounder really picks up his game by the last round and is at its best, Simpleton also improves his game by the last round but is still not really outperforming others.
            #Trickerton, who is a rockstar in the first couple of rounds looks tired by the last round.
            if self.suspects_on_failed_mission["Bounder"]=="No":
                playerToSelect="Bounder"
            elif self.suspects_on_failed_mission["Logicalton"]=="No":
                playerToSelect="Logicalton"
            elif self.suspects_on_failed_mission["Simpleton"]=="No":
                playerToSelect="Simpleton"
            elif self.suspects_on_failed_mission["Trickerton"]=="No":
                playerToSelect="Trickerton"
            else:
                playerToSelect="Bounder"
        for item in players:    
            if item.name == playerToSelect:
                self.keyPlayer=item
        return [self] + [self.keyPlayer] + random.sample(self.getanotherplayer(), count - 2)

    def getanotherplayer(self):
        return [p for p in self.game.players if p != self and p != self.keyPlayer]

    def vote(self, team):
        
        return True

    def sabotage(self):
        
        return True
    
    
    def onMissionFailed(self, leader, team):
        """Callback once a vote did not reach majority, failing the mission.
        @param leader       The player responsible for selection.
        @param team         The list of players chosen for the mission.
        """
        
        pass 
        

    def onVoteComplete(self, votes):
        """Callback once the whole team has voted.
        @param votes Boolean votes for each player"""
        """ Players with count of more than 0 in failed missions been on dictionary are to be treated as suspects """
        
        pass
        
        

    def onGameRevealed(self, players, spies):
        
        """This function will be called to list all the players, and if you're a spy,
        the spies too -- including others and yourself.
        @param players List of all players in the game including you.
        @param spies List of all players that are spies, or an empty list."""

        self.suspects_on_failed_mission={}
        for i in players:
            self.suspects_on_failed_mission[i.name]="No"
    
        

        
    def onMissionComplete(self, num_sabotages):
        """Callback once the players have been chosen.
        @param num_sabotages    Integer how many times the mission was sabotaged.
        """
        if(num_sabotages!=0):
            #print("num_sabotages - ", num_sabotages)
            #print("self.game.team - ", self.game.team)
            for r in self.game.team:
                if r.name in self.suspects_on_failed_mission:
                    self.suspects_on_failed_mission[r.name]="Yes"
           
        

    def onGameComplete(self, win, spies):
        """Callback once the game is complete, and everything is revealed.
        @param win          Boolean true if the Resistance won.
        @param spies        List of only the spies in the game.
        """
        pass

    
