#!/usr/bin/env python3

import subprocess, re, sys, os.path

debugV1 = False
debugV2 = False
debugV3 = False

def run_and_return(params):
    res = subprocess.run(params, capture_output=True, text=True)
    if debugV1 or debugV3:
        print("[DEBUG] {} retcode = {}".format(' '.join(params).strip(), res.returncode))
    if debugV2 or debugV3:
        if res.stdout == "": print("[DEBUG] {} No Output".format(' '.join(params).strip()))
        else: print("[DEBUG] {}".format(res.stdout.strip()))
    return res.stdout, res.returncode

def regex(haystack, needle):
   return re.search(needle,haystack)

def do_print(msg, success=True):
    if success: print("[+] {} successful".format(msg))
    else:print("[!] {} failed".format(msg))
    if debugV1 or debugV2 or debugV3:print()

def do_password_complexity_testing():
    password = {
        "Minimum length check": ("minlen",8), 
        "Lowercase limit check": ("lcredit",-1),
        "Uppercase limit check": ("ucredit",-1),
        "Digit limit check": ("dcredit",-1),
        "Symbol limit check": ("ocredit",-1),
        }


    data, retval = run_and_return(["grep","-m","1","pam_cracklib.so","/etc/pam.d/common-password"])
    if retval!=0:
        for k in password:do_print(k, False)
        return

    for k in password:
        v = password[k]
        if regex(data,"{}\s*=\s*{}".format(v[0],v[1])):do_print(k)
        else: do_print(k, False)

def do_password_age_testing():

    age = {
        "Maximum Password age": ("PASS_MAX_DAYS",45),
        "Minimum Password age": ("PASS_MIN_DAYS",3),
        "Password Expiry Notification": ("PASS_WARN_AGE",10),
    }

    for k in age:
        v = age[k]
        out, _ = run_and_return(["grep","-m","1","^"+v[0],"/etc/login.defs"])
        if regex(out,"{}\s+{}".format(v[0],v[1])):do_print(k)
        else: do_print(k, False)

def do_password_remember_testing():
    line, retval = run_and_return(["grep","-m","1","pam_unix.so","/etc/pam.d/common-password"])
    if retval != 0:
        do_print("Password History Remember Check", False)
        return
    if retval == 0 and regex(line,"\sremember\s*=\s*5"):
        do_print("Password History Remember Check")
        return
    
    do_print("Password History Remember Check", False)
    
    
    # if regex(run_and_return(["grep","pam_unix.so","/etc/pam.d/common-password"], debug=True),"{}\s+{}".format(v[0],v[1])):do_print(k)
    # else: do_print(k, False)

def extract_ssh_value(param):
    line, code = run_and_return(["grep","-m","1","^"+param,"/etc/ssh/sshd_config"])
    if code != 0 : return ""
    return " ".join(line.strip().split()[1:])
    
def ssh_value_set(p, value):
    if extract_ssh_value(p).lower()==value.lower():return True
    return False


def check_ssh_inactivity(value):
    ClientAliveInterval = 0
    ClientAliveCountMax = 0

    da = extract_ssh_value("ClientAliveInterval")
    if da != "":ClientAliveInterval = int(da)

    da = extract_ssh_value("ClientAliveCountMax")
    if da != "":ClientAliveCountMax = int(da)

    if debugV1 or debugV2 or debugV3:print("[DEBUG] Timeout is set to {}".format(ClientAliveCountMax*ClientAliveInterval))
    
    if ClientAliveCountMax*ClientAliveInterval == value:do_print("Inactivity timeout check")
    else: do_print("Inactivity timeout check", False)


def check_ssh_parameters():

    params = {
        "Restrict Root Login": ("PermitRootLogin","No"),
        "SSH Protocol 2": ("Protocol","2"),
        "Logging of login and logout": ("LogLevel","INFO"),
        "Disable X11 Forwarding": ("X11Forwarding","No"),
        "Diable .rhosts file": ("IgnoreRhosts","Yes"),
        "Set SSH HostbasedAuthentication to NO": ("HostbasedAuthentication","No"),
        "Set SSH PermitEmptyPasswords to NO":("PermitEmptyPasswords","No"),
        "Do not allow users to set environment options":("PermitUserEnvironment","No"),
        "Set Login Grace time to 60 seconds":("LoginGraceTime","60"),
        "Enable StrictModes":("StrictModes","Yes"),
        "Restrict SSH from setting up TCP Port forwarding":("AllowTcpForwarding","No"),
        "Enable Privilege Separation": ("UsePrivilegeSeparation","Yes")
    }

    for k in params:
        v = params[k]
        if ssh_value_set(v[0],v[1]):do_print(k)
        else:do_print(k,False)

def do_ssh_banner_testing(banner):
    val, ret = run_and_return(["cat",extract_ssh_value("Banner")])
    if ret == 0 and val == banner:
        do_print("Login Banner Check")
        return
    do_print("Login Banner Check", False)

def do_private_key_testing():
    val, ret = run_and_return(["cat",os.path.join(os.path.expanduser('~'),'.ssh','authorized_keys')])
    if ret != 0:
        do_print("Allow access on through provided private key",False)
        return
    keys = val.strip().split('\n')
    if len(keys) != 1:
        do_print("Allow access on through provided private key",False)
        return
    keys = keys[0]
    if keys=="ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHwo4zbsPfi+4EhKsCi9on33ppfmVaJ0e2e53t9yVYcbOr0qZgIzTL1lLcQqYWup/vFQTokiyBMV/ZCt22+/ZUI= user@Nationals":do_print("Allow access on through provided private key")
    else: do_print("Allow access on through provided private key", False)

if __name__ == "__main__":
    if len(sys.argv)>1:
        verbose = sys.argv[1][1:]
        if verbose=='dc':debugV1 = True
        elif verbose=='do':debugV2 = True
        elif verbose=='da':debugV3 = True

    do_password_age_testing()
    do_password_complexity_testing()
    do_password_remember_testing()
    do_private_key_testing()
    do_ssh_banner_testing("Unauthorized Access is prohibited!")
    check_ssh_inactivity(600)
    check_ssh_parameters()