def init():
    # set localhost status
    from hostdetails import localhost

    global global_values
    global_values = {
        'localhost': localhost
    }
