def get_line_color(fault):

    if fault == "Normal":
        return "lime"

    elif fault == "Overload":
        return "yellow"

    elif fault == "Overvoltage":
        return "orange"

    elif fault == "Undervoltage":
        return "deepskyblue"

    elif fault == "Line Break":
        return "red"

    else:
        return "gray"