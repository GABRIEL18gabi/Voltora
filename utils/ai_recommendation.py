def get_ai_recommendation(disaster):

    if disaster == "Cyclone":

        return {
            "level": "HIGH",
            "action": [
                "Shutdown affected feeder",
                "Switch to backup feeder",
                "Notify Control Room",
                "Dispatch maintenance team"
            ]
        }

    elif disaster == "Flood":

        return {
            "level": "HIGH",
            "action": [
                "Protect transformers",
                "Monitor substations",
                "Reduce feeder load",
                "Issue warning"
            ]
        }

    elif disaster == "Heatwave":

        return {
            "level": "MEDIUM",
            "action": [
                "Monitor transformer temperature",
                "Reduce heavy load",
                "Increase cooling inspection"
            ]
        }

    elif disaster == "Heavy Rain":

        return {
            "level": "MEDIUM",
            "action": [
                "Inspect overhead lines",
                "Prepare repair crew",
                "Monitor voltage fluctuations"
            ]
        }

    else:

        return {
            "level": "LOW",
            "action": [
                "Grid operating normally"
            ]
        }