from gui import test

webo = test()
print(webo[3])
hostIp = webo[0]
hostIp = str(hostIp)
hostPort = webo[1]
target_path = webo[2]
target_ip = webo[3]
server_address = [hostIp,hostPort]
print("revisar=",hostIp,hostPort,target_ip,target_path)
directory = target_path
baseUrl = hostIp + ':' + str(hostPort) + '/'
file_list_payload = baseUrl + quote(os.path.basename(target_path))
file_list_payloadBytes = file_list_payload.encode('ascii')

print(hostIp)