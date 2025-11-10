def tracker():
    
    dailyLimit = int(input('Whats your daily target:'))
    
    data = []
    while True:
        name = input('Enter the name of the food:')
        calorie = int(input('Ente the amount of calorie:'))
        
        data.append({
            'name': name,
            'calorie': calorie
        })
         
        moreData = input('Would you like to add more data (y or n):')
        if moreData != 'y':
            break
    
    Total = 0 
    for key, value in data:
        Total += calorie
        
    if Total >= dailyLimit:
        print(f'You are above your daily limit {Total} calories')
    
    else:
        print(f'You are under your daily limit {Total} calories')

tracker()