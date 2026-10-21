import random

def create_environment():
    environment = {
        "time": "day",
        "weather": random.choice(["rainy", "clear"])
    }

    return environment


def create_agent():
    attributes = {
        "name" : "Caine",
        "energy" : 60,
        "max_energy" : 100,
        "energy_loss" : 10,
        "location" : "Main Hall",
        "actions_taken" : 0,
        "possible_goals" : [
            "Explore",
            "Rest",
            "Observe"
        ],
        "goal" : "Explore",
        "memory" : [],
    }

    return attributes


def observe(environment):
    return environment


def update_energy(attributes, amount):
    attributes["energy"] += amount

    if attributes["energy"] > attributes["max_energy"]:
        attributes["energy"] = attributes["max_energy"]

    if attributes["energy"] < 0:
        attributes["energy"] = 0


def think(environment, attributes):

    memory = attributes["memory"]
    recent_memory = memory[-3:]

    if attributes["energy"] > 30:

        if environment["weather"] == "clear":

            attributes["goal"] = "Explore"

        elif environment["weather"] == "rainy":

            attributes["goal"] = "Observe"

    elif attributes["energy"] < 30:

        attributes["goal"] = "Rest"

    elif attributes["energy"] == 30:
        
        energy_check = random.randint(0,1)
        print(f"Energy check complete, result: {energy_check}")
        
        if energy_check == 1 and environment["weather"] == "clear":
            
            attributes["goal"] = "Explore"
            
        elif energy_check == 1 and environment["weather"] == "rainy":
            
            attributes["goal"] = "Observe"
        
        if energy_check == 0:
            
            attributes["goal"] = "Rest"
            
    if attributes["goal"] == "Rest":

        return "Rest"

    elif attributes["goal"] == "Observe":

        if recent_memory.count("Observed") < 2:

            return "Observe surroundings"
        
        else:
            
            return "Explore"
    

    elif attributes["goal"] == "Explore":

        if recent_memory.count("Explored") < 2:

            return "Explore"
        
        else:
            
            return "Observe surroundings"

    return "Do nothing"
        

def act(decision, attributes):
    print(f"{attributes['name']} decides: {decision}")

    memory = attributes["memory"]

    if decision == "Rest":
        update_energy(
            attributes,
            attributes["max_energy"] - attributes["energy"]
        )
        memory.append("Rested")
        attributes["actions_taken"] += 1
        print("Caine has rested and recovered his energy.")

    elif decision == "Explore":
        update_energy(attributes, -attributes["energy_loss"])
        memory.append("Explored")
        attributes["actions_taken"] += 1
        print(f"Energy: -{attributes['energy_loss']}")
        print("Caine goes out exploring outside.")

    elif decision == "Observe surroundings":
        update_energy(attributes, -attributes["energy_loss"]/2)
        memory.append("Observed")
        attributes["actions_taken"] += 1
        print(f"Energy: -{attributes['energy_loss']/2}")
        print("Caine looks around the Main Hall.")

    print(f"Energy remaining: {attributes['energy']}")
    print(f"Actions taken: {attributes['actions_taken']}")


# Initialize the environment and agent once
environment = create_environment()
attributes = create_agent()

# Main agent loop
while True:
    environment["weather"] = random.choice(["rainy", "clear"])
    current_environment = observe(environment)

    print("\n--- Current State ---")
    print("Environment:", current_environment)
    print("Agent:", attributes)

    decision = think(current_environment, attributes)

    act(decision, attributes)

    if attributes["actions_taken"] >= 25:
        print("\nExperiment finished: 25 actions completed.")
        break