def find_lan_party_password(input_file: str) -> int:
    all_connections = read_in_connections(input_file)
    check_connections = [set(con.split('-')) for con in all_connections]
    next_connections = [1,2,3]
    while len(next_connections) > 1:
        next_connections = []
        for connection_set in check_connections:
            con_to_find = copy.deepcopy(connection_set)
            con_to_find.pop()
            mutual_connections = {list(con - con_to_find)[0] for con in check_connections if con_to_find.issubset(con)}
            for con_to_remove in connection_set:
                con_to_find = connection_set - {con_to_remove}
                mutual_connections &= {list(con - con_to_find)[0] for con in check_connections if con_to_find.issubset(con)}
            for connection in mutual_connections:
                if (new_connection := connection_set | {connection}) not in next_connections:
                    next_connections.append(new_connection)
        check_connections = next_connections
        print(len(next_connections))
        print(next_connections)
    return next_connections