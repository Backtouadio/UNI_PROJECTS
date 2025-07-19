def prepare_for_env(filepath):
    print("[INFO]: Preparing map for env")
    try:
        print("[INFO]: Loading map data from file")
        with open(filepath, "r") as map_data:
            mapping = map_data.readlines()
    
    except FileNotFoundError:
        raise Exception("Specified file does not exist")
    
    # Initialize variables for start and goal positions
    start_position = None
    goal_position = None

    for i, row in enumerate(mapping):
        new_row = row.replace("\n", "")
        mapping[i] = new_row
        # Find the positions of 'S' and 'G'
        if 'S' in new_row:
            start_position = (i, new_row.index('S'))  # (row_index, column_index)
        if 'G' in new_row:
            goal_position = (i, new_row.index('G'))  # (row_index, column_index)

    if start_position is None or goal_position is None:
        raise Exception("Map must contain 'S' for start and 'G' for goal.")
    
    print("[DEBUG]: Map prepared for env")
    return mapping, start_position, goal_position
