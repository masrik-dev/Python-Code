def computepay(h,r):
    p = h*r
    return p

hrs = input("Enter Hours:")
h = float(hrs)
rph = input("Enter rate per hour:")
r = float(rph)

if h<=40:
    p = computepay(h,r)
    print("Pay", p)
elif h>=40:
    h = float(h-40)
    a = float(r*1.5*h)
    b = computepay(40,r)
    total_pay = a+b
    print("Pay", total_pay)