version=1
print("GDbackMachine - Version "+str(version))
import requests,base64,hashlib,itertools,os,time
from time import gmtime, strftime
def xor(data, key):
        return "".join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, itertools.cycle(key)))
def chk(values: [int, str] = [], key: str = "", salt: str = "") -> str:
    values.append(salt)
    string = "".join(map(str,values))
    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor(hashed,key)
    final = base64.urlsafe_b64encode(xored.encode()).decode()
    return final
def commentCHK(*,username,comment,levelid,percentage,type):
    part1 = username + comment + levelid + str(percentage) + type + "xPT6iUrtws0J"
    return base64.b64encode(xor(hashlib.sha1(part1.encode()).hexdigest(),"29481").encode()).decode()
def useed(data: str, chars: int = 50) -> str:
    if len(data) < chars:
        return data
    step = len(data) // chars
    return data[::step][:chars]
def gjpEncrypt(data):
    return base64.b64encode(xor(data,"37526").encode()).decode()
def gjpDecrypt(data):
    return xor(base64.b64decode(data.encode()).decode(),"37526")
def getGJUsers(target):
    try:
        data = {
            "secret": "Wmfd2893gb7",
            "str": target
        }
        request = requests.post("http://www.boomlings.com/database/getGJUsers20.php",data=data,headers={"User-Agent": ""}).text.split(":")[1::2]
        username = request[0]
        accountid = request[10]
        return username,accountid
    except:
        return None
def uploadGJLevel(name,accid,passw,levelString,gjver,lvlName,desc,ver,length,audio,password,original,twoP,songID,objects,coins,reqStars,unlisted,ldm):
    try:
        data = {
            "gameVersion": gjver,
            "accountID": accid,
            "gjp": gjpEncrypt(passw),
            "userName": name,
            "levelID": 0,
            "levelName": lvlName,
            "levelDesc": base64.b64encode(desc.encode()).decode(),
            "levelVersion": int(ver),
            "levelLength": int(length),
            "audioTrack": int(audio),
            "auto": 0,
            "password": int(password),
            "original": int(original),
            "twoPlayer": int(twoP),
            "songID": int(songID),
            "objects": int(objects),
            "coins": int(coins),
            "requestedStars": int(reqStars),
            "unlisted": int(unlisted),
            "ldm": int(ldm),
            "levelString": levelString,
            "seed2": chk(key="41274",values=[useed(levelString)],salt="xI25fpAapCQg"),
            "secret": "Wmfd2893gb7"
        }
        return requests.post("http://www.boomlings.com/database/uploadGJLevel21.php", data=data, headers={"User-Agent":""}).text
    except:
        return None
def downloadGJLevel(lvl):
    data = {
        "levelID": lvl,
        "secret": "Wmfd2893gb7"
    }
    return requests.post("http://www.boomlings.com/database/downloadGJLevel22.php",data=data,headers={"User-Agent": ""}).text
def getGJMessages(accid,gjp):
    try:
        data = {
            "accountID": accid,
            "gjp": gjpEncrypt(gjp),
            "secret": "Wmfd2893gb7"
        }
        return requests.post("http://www.boomlings.com/database/getGJMessages20.php",data=data,headers={"User-Agent": ""}).text
    except:
        return 
def deleteGJMessages(accid,gjp,mid):
    try:
        data = {
            "accountID": accid,
            "gjp": gjpEncrypt(gjp),
            "messageID": mid,
            "secret": "Wmfd2893gb7"
        }
        return requests.post("http://www.boomlings.com/database/deleteGJMessages20.php",data=data,headers={"User-Agent": ""}).text
    except:
        return None
def parseMessages(usern,accid,passw):
    resp=getGJMessages(accid,passw)
    try:
        msgs=resp.split("|")
        for msg in msgs:
            mlist=msg.split(":")
            mname=mlist[1]
            mid=mlist[7]
            msubj=base64.b64decode(mlist[9]).decode()
            yield mname,mid,msubj
            deleteGJMessages(accid,passw,mid)
    except:
        return None
def uploadGJMessage(accid,passw,sendto,subject,message):
    try:
        data = {
            "accountID": accid,
            "gjp": gjpEncrypt(passw),
            "toAccountID": getGJUsers(sendto)[1],
            "subject": base64.b64encode(subject.encode()).decode(),
            "body": base64.urlsafe_b64encode(xor(message,"14251").encode()).decode(),
            "secret": "Wmfd2893gb7",
        }
        return requests.post('http://www.boomlings.com/database/uploadGJMessage20.php', data=data, headers={"User-Agent":""}).text
    except:
        return None
def uploadGJComment(name,accountid,passw,comment,level):
    try:
        gjp = gjpEncrypt(passw)
        c = base64.b64encode(comment.encode()).decode()
        chk = commentCHK(username=name,comment=c,levelid=str(level),percentage=0,type="0")
        data = {
            "secret":"Wmfd2893gb7",
            "accountID":accountid,
            "gjp":gjp,
            "userName":name,
            "comment":c,
            "levelID":level,
            "percent":0,
            "chk":chk
        }
        return requests.post("http://www.boomlings.com/database/uploadGJComment21.php",data=data,headers={"User-Agent": ""}).text
    except:
        return None
def archiveLevel(usern,accid,passw,level,rpname):
    download=downloadGJLevel(level).split(":")
    try:
        lvlid=int(download[1])
        name=download[3]
        string=download[7]
        pid=int(download[11])
        gur=getGJUsers(pid)
        pname=gur[0]
        paccid=int(gur[1])
        osong=int(download[19])
        csong=int(download[49])
        fname=name+" by "+pname+" ("+str(lvlid)+")"
        print("Archiver set to "+fname+".")
        resp=uploadGJLevel(usern,accid,passw,string,21,name,"Archived by "+rpname+" - Original by "+pname,version,0,osong,1,lvlid,0,csong,0,0,69,0,1)
        print("Level reuploaded to the servers ("+resp+").")
        ct=strftime("%Y/%m/%d %H:%M:%S",gmtime())
        uploadGJComment(usern,accid,passw,"This level has been archived by the Wayback Machine at "+ct,level)
        return resp
    except:
        print("The level specified ("+level+") does not exist.")
        return None
def main():
    usern="YourUsername"
    passw="YourPassword"
    accid=69420
    for msg in parseMessages(usern,accid,passw):
        resp=archiveLevel(usern,accid,passw,msg[2],msg[0])
        if resp == None:
            uploadGJMessage(accid,passw,msg[0],"Wayback Machine Request","Hello "+msg[0]+", your request to archive the level "+msg[2]+" failed because the level does not exist.")
        else:
            uploadGJMessage(accid,passw,msg[0],"Wayback Machine Request","Hello "+msg[0]+", your request to archive the level "+msg[2]+" is completed. Level ID: "+resp)
    time.sleep(5)
print("Bot started!")
while True:
    main()
