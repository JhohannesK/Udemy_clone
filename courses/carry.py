def get_time(length:float, type:str='long'):
    h = length // 3600
    m = length % 3600 // 60 
    s = length % 3600 % 60 
    
    if type == 'short':
        return f"{h}h {f'0{m}' if m < 10 else m}m"