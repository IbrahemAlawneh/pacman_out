from mazegenerator import MazeGenerator

gen= MazeGenerator((3,3))



from configuration_files.config_validation import load_config


con = load_config("config.json")

print(con)
self.config["ghost_speed"] = max(40, min(self.config.get("ghost_speed", 50), 100))
            self.config["pacman_speed"] = max(40, min(self.config.get("pacman_speed", 50), 100))
            self.config["width"] = max(5, min(self.config("width", 10), 20))
            self.config["height"] = max(5, min(self.config("height", 10), 20))