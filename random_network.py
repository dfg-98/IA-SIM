def get_random_network(tree_edges, number_of_vertex):
    maximun_edges_n = (number_of_vertex*(number_of_vertex - 1))/2 #A complete graph have n(n-1)/2 edges 
    edges_to_add = maximun_edges_n - (number_of_vertex - 1) #A tree have n-1 edges 

    while edges_to_add > 0:
        
