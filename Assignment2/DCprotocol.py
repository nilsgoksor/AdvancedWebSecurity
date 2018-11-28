# SET INPUT
case_1 = False
case_2 = True
testQuiz = True

if case_1:
    SA = '0C73'
    SB = '80C1'
    DA= 'A2A9'
    DB = '92F5'
    M = '9B57'
    b = 0
if case_2:
    SA= '27C2'
    SB= '0879'
    DA= '35F6'
    DB= '1A4D'
    M='27BC'
    b= 1
if testQuiz:
    SA='BF0D'
    SB='3C99'
    DA='186F'
    DB='2EAD'
    M='62AB'
    b=0

# CONVERT TO BINARY
SA_binary  = bin(int(SA, 16))[2:].zfill(16)
SB_binary = bin(int(SB, 16))[2:].zfill(16)
DA_binary = bin(int(DA, 16))[2:].zfill(16)
DB_binary = bin(int(DB, 16))[2:].zfill(16)
M_binary = bin(int(M, 16))[2:].zfill(16)

# XOR alice and bob secret
xor_secret_alice_bob = int(SA_binary,2) ^ int(SB_binary,2)
xor_secret_alice_box_hex = hex(int(xor_secret_alice_bob))[2:].zfill(4).upper()

# If b = 0, your broadcasted data in hex format, immediately followed by the anonymous message
# sent by some other party (0000 if no anonymous message was sent).
# If b = 1, your 16-bit broadcasted data in hexadecimal format.
if b==1:
    broadcasted_data = xor_secret_alice_bob ^ int(M_binary,2)
    broadcasted_data_hex = hex(int(broadcasted_data))[2:].zfill(4).upper()
    print("Message to send:",broadcasted_data_hex)
else:
    xor_data_alice_bob = int(DA_binary,2) ^ int(DB_binary,2)    
    
    #if not xor_data_alice_bob: xor_data_alice_bob = '0000'
    
    broadcasted_data = xor_secret_alice_bob ^ xor_data_alice_bob
    broadcasted_data_hex = hex(int(broadcasted_data))[2:].zfill(4).upper()

    concatinated_output_hex = xor_secret_alice_box_hex + broadcasted_data_hex
    print("Message to send:",concatinated_output_hex)
