# Def 6: Tolerable disruption
def disruption(S, tau, epsilon, current_task, current_goal):

    for d in S:
        if tau.get((d, current_task), 0) == 2 or epsilon.get((d, current_goal), 0) == 2:
            #print("Critical component in S")
            return 0
    return 1


# Def 7: monotonic degradation function
def monotonic_degradation(S, tau, epsilon, current_task, current_goal, alpha_crit, alpha_base):
    value = 1
    for d in S:

        level = max(
            tau.get((d, current_task), 0), 
            epsilon.get((d, current_goal), 0)
        )
        if level == 2:
            value = value - alpha_crit
        elif level == 1:
            value = value - alpha_base
    
    #print(f'Psi value {max(value,0)}')
    return max(value, 0)


# Def 7: Tolerable Degradation
def degradation(S, tau, epsilon, current_task, current_goal, theta_crit, theta_base, alpha_crit, alpha_base):

    psi = monotonic_degradation(S, tau, epsilon, current_task, current_goal, alpha_crit, alpha_base)

    for d in S:
        level = max(
            tau.get((d, current_task), 0), 
            epsilon.get((d, current_goal), 0)
        )
        if level == 2:
            theta = theta_crit # theta_crit
        elif level == 1:
            theta = theta_base
        else:
            continue

        if psi < theta:
            return 0
    return 1


