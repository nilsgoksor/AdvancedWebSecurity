import base64

def int_to_bits(our_bits, chars=0):
    return "{0:b}".format(our_bits).zfill(chars)


def der_encode(integer, ldf=True):
    T = "02"
    V = ""
    # Pad V so it becomes even octets
    V = hex(integer)[2:]
    bitVector = "0" + int_to_bits(int(V,16))
    if len(bitVector) % 8 != 0:
        charsMissing = 8 - (len(bitVector) % 8)
        bitVector = "0" * charsMissing + bitVector

    V_length = int(len(bitVector) / 8)
    V = hex(int(bitVector,2))[2:]
    while V_length > len(V)/2:
        V = "0" + V
    
    # Create L
    # 0-128 octets - normal
    if V_length <= 127:
        L = hex(V_length)[2:]
        if len(L) % 2 == 1:
            L = "0" + str(L)
        else:
            L = str(L)
    # >128 octets - long definite form
    else:
        if ldf:
            L = longDefiniteForm(V)
        else:
            L = "10000000"
            V += "0" * 8 * 2
    
    return T + L + V

def longDefiniteForm(V):
    V_int = int(len(V) / 2)
    V_hex = hex(V_int)[2:]

    # Add padding, we want full octets
    if len(V_hex) % 2 != 0:
        V_hex = "0" + V_hex

    if len(V_hex) > 2 or int_to_bits(V_int, 8)[0] == "1":
        L_int = int(len(V_hex) / 2)
        L_bits = int_to_bits(L_int, 7)
        L_bits = "1" + L_bits
        L_hex = hex(int(L_bits, 2))[2:]
        L = L_hex + V_hex
    else:
        L = V_hex

    return L

def base64_encode(p, q):
    e = 65537
    version = 0
    n = p * q
    d = modularMultiplicativeInverse(e, (p - 1) * (q - 1))
    exp1 = d % (p - 1)
    exp2 = d % (q - 1)
    coeff = modularMultiplicativeInverse(q, p)

    der = der_encode(version) + der_encode(n) + der_encode(e) + der_encode(d) + der_encode(p) + der_encode(q) + der_encode(exp1) + der_encode(exp2) + der_encode(coeff)
    
    rsa_priv_key = "30" + der_encode(int(der, 16))[2:]
    encoded_rsa_priv_key = base64.b64encode(bytearray.fromhex(rsa_priv_key))
    return encoded_rsa_priv_key

# extended great common divisor
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modularMultiplicativeInverse(a, m):
    g, x, y = egcd(a, m)
    if g == 1:
        return x % m
    else:
        return "no inverse"


#TEST-data
#p = 139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763
#q = 141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719
#test = 161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741

#NILS TEST
der_decode = 148700129342364405620892147229907426881246463222054844483132467349937188056634654362041588770292787587186166927263749165534406696821499859200202235053015371521639102614190814932099853050836332465199405428020035784049490284120934011304859372717164102740438900317742151812993802304503432731806447014557244080921
p = 97334696808044737745619471749642021207104353055190530251003070099294623473372062389445613330131781595852600285989522817678993949554158916119072700378763356466238655091001451757200605853585886343032260664754715988168953539222102856979561221526004993782785348973097090478337138425275301246222220490261352295571
q = 149310765878644468580737212120210471225065969134634846853161289498651769610058419030714915934140866701189693487584790498915328404844562008068420164318965198130159928109682708071091009880819472120886301841692292786403177183178836405130229887101611923796350665326657612413114574353997570939347622547286423924549

print("ANSWER")
print("------------------------------")
#print("DER:", der_encode(der_decode))
print()
print()
print("Base64:", base64_encode(p,q))
print("------------------------------")

