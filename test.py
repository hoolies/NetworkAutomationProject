Networks = {
    'corp': {  
        'hosts': [
            'corp-1', 
            'corp-2'], 
        'subnet': '192.168.1.0/24'
        }, 
    'dmz': { 
        'hosts': [
            'dmz-1', 
            'dmz-2'], 
        'subnet': '172.16.0.0/12'
    }
}

for k,v in Networks.items():
    print("Your hosts are:", v['hosts'])
    print("Your IP is:", v['subnet'])
