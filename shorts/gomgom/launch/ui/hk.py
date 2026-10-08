import sys
CHO="rRseEfaqQtTdwWczxvg"; JUNG=["k","o","i","O","j","p","u","P","h","hk","ho","hl","y","n","nj","np","nl","b","m","ml","l"]
JONG=["","r","R","rt","s","sw","sg","e","f","fr","fa","fq","ft","fx","fv","fg","a","q","qt","t","T","d","w","c","z","x","v","g"]
out=""
for ch in sys.argv[1]:
    c=ord(ch)
    if 0xAC00<=c<=0xD7A3:
        i=c-0xAC00; out+=CHO[i//588]+JUNG[(i%588)//28]+JONG[i%28]
    elif ch in "+^%~(){}[]": out+="{"+ch+"}"
    else: out+=ch
print(out)
