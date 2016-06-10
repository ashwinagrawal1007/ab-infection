import random

user_base = {}
infected = []
to_be_infected = []
sub_graphs = [[]]

#infects single disjoint subgraph for total_infection
def total_infection_pass():
    global to_be_infected
    select_user_to_start()
    while len(to_be_infected) > 0:
        node = to_be_infected.pop(0)
        infect(node)
        to_be_infected = to_be_infected + [user for user in user_base[node] if not is_infected(user) and user not in to_be_infected]

#infect a user, this logic is replacable
def infect(user):
    infected.append(user)

#checks if a user is infected, this logic depends on how the infection is implemented
def is_infected(user):
    if user in infected:
        return True
    return False

#selects a random user from potential ones to start the infection
def select_user_to_start():
    user_to_start_with = random.choice([user for user in user_base.keys() if not is_infected(user)])
    to_be_infected.append(user_to_start_with)

#infects a disjoint subgraph in a pass and proceeds as specified, also can infect 100% users if full_infection is passed as True
def total_infection(full_infection = False):
    print "------------Total Infection-----------------"
    while len(infected) != len(user_base):
        total_infection_pass()
        if len(infected) != len(user_base):
            if not full_infection:
                proceed = raw_input("infected " + str(len(infected)) + " users, left with " + str(len(user_base) - len(infected)) + " more users, proceed furthur? [yes/no] ")
                if proceed == "no":
                    break
    print "infected " + str(len(infected) * 100.0/len(user_base)) + "%" + " users in total after total_infection"
    return len(infected)

#derives a disjoint subgraph from the user base, and is used by limited_infection
def get_a_sub_graph():
    ret = []
    to_be_added = []
    potential_nodes = [node for node in user_base.keys() if node not in to_be_added and not exists_in_subgraph(node)]
    node_to_start_with = random.choice(potential_nodes)
    to_be_added.append(node_to_start_with)
    while len(to_be_added) > 0:
        node = to_be_added.pop(0)
        ret.append(node)
        to_be_added = to_be_added + [user for user in user_base[node] if user not in ret and user not in to_be_added]
    return ret

#checks if a user is a part of any already derived subgraph
def exists_in_subgraph(node):
    for sub_graph in sub_graphs:
        if node in sub_graph:
            return True
    return False

#checks if the complete user base is represented with the list of disjoint subgraphs
def sub_graphs_completed():
    num_of_nodes = 0
    for sub_graph in sub_graphs:
        num_of_nodes += len(sub_graph)
    if num_of_nodes == len(user_base):
        return True
    return False

#selects the graph to infect, returns the one with users closest to specified number of users to infect
def get_sub_graph_to_infect(num_of_users):
    diff = float("inf")
    ret = []
    for sub_graph in sub_graphs:
        if abs(len(sub_graph) - num_of_users) < diff:
            diff = abs(len(sub_graph) - num_of_users)
            ret = sub_graph
    return ret

#limited_infection infects users closest to the number of users specified and if strict is set True infects only if the number of users in the subgraph selected to infect is exactly equal to specified 
def limited_infection(num_of_users, strict = False):
    print "------------Limited Infection---------------"
    while not sub_graphs_completed():
        sub_graphs.append(get_a_sub_graph())
    infection_completed = False
    while not infection_completed:
        sub_graph_to_infect = get_sub_graph_to_infect(num_of_users)
        if not sub_graph_to_infect or (strict and len(sub_graph_to_infect) != num_of_users):
            break
        for idx, user in enumerate(sub_graph_to_infect):
            if is_infected(user):
                sub_graphs.remove(sub_graph_to_infect)
                break
            else:
                infect(user)
                if idx == len(sub_graph_to_infect) -1:
                    infection_completed = True
    print "infected " + str(len(infected) * 100.0/len(user_base)) + "%" + " users in total after limited_infection"
    return len(infected)