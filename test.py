from mazegenerator import MazeGenerator

gen= MazeGenerator((3,3))



from configuration_files.config_validation import load_config


con = load_config("config.json")

print(con)
con["ghost_speed"] = max(40, min(con.get("ghost_speed", 50), 100))
con["pacman_speed"] = max(40, min(con.get("pacman_speed", 50), 100))
con["width"] = max(5, min(con.get("width", 10), 20))
con["height"] = max(5, min(con.get("height", 10), 20))