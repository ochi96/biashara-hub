
def years():
    valid_years=[]
    for year in range(1933,2000):
        valid_years.append(year)
        year=year+1
    x=valid_years
    y=[]
    for x in valid_years:
        k=[]
        z=str(x)
        k.append(z)
        k.append(z)
        y.append(tuple(k))
    print (y)

years()

