""" the tester for agent pack"""

from vanilla_agent.AgentPack import AgentTeam
import numpy as np

def main():
    #params
    init_states = [np.array([[1],[2]]),
                   np.array([[2],[3]]),
                   np.array([[3],[4]])]
    aNum = 3

    #init agent teams
    agent_team1 = AgentTeam(init_states=init_states, aNum=aNum)
    print("agent_group_tester ran")


if __name__ == '__main__':
    main()

