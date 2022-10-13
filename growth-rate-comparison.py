# Map from growth rate to:
#   - fraction of the population cumulatively infected when 1% currently
#     infected
#   - fraction of the population currrently infected when 1% cumulatively
#     infected
#   - days until 1% current
#   - days until 1% cumulative

cumulative_fraction = 0.01
current_fraction = 0.01
infection_days = 14

population = 8000000000
print("growth\tcumulative when current=%.0f%%\tcurrent when cumulative=%.0f%%"
      "\tdays until current=%.0f%%\tdays until cumulative=%.0f%%" % (
          current_fraction*100, cumulative_fraction*100, 
          current_fraction*100, cumulative_fraction*100))

for growth_rate_pct in range(1,51):
    cumulative_when_current = None
    current_when_cumulative = None
    days_until_current = None
    days_until_cumulative = None
        
    growth_rate = growth_rate_pct / 100 + 1
    daily_new_infections = 1
    cumulative_infections = 1
    currently_infected = []    
    for day in range(1,100000):
        daily_new_infections *= growth_rate
        cumulative_infections += daily_new_infections

        currently_infected.append(daily_new_infections)
        if len(currently_infected) > infection_days:
            currently_infected.pop(0)

        n_currently_infected = sum(currently_infected)
        
        if not days_until_cumulative:
            if cumulative_infections / population >= cumulative_fraction:
                current_when_cumulative = n_currently_infected / population
                days_until_cumulative = day
        if not days_until_current:
            if n_currently_infected / population >= current_fraction:
                cumulative_when_current = cumulative_infections / population
                days_until_current = day

        if days_until_cumulative and days_until_current:
            break

    print("%s%%\t%.4f\t%.4f\t%s\t%s" % (
        growth_rate_pct,
        cumulative_when_current,
        current_when_cumulative,
        days_until_current,
        days_until_cumulative))
