def get_fault_connection(fault):

    fault_map = {
        "Normal": None,
        "Overload": ("Salem", "Coimbatore"),
        "Overvoltage": ("Chennai", "Salem"),
        "Undervoltage": ("Madurai", "Tirunelveli"),
        "Line Break": ("Tiruchirappalli", "Madurai")
    }

    return fault_map.get(fault)