import poplib

#email = raw_input('pqy_edu@163.com')
#password = raw_input('109291ac')
#pop3_server = raw_input('pop3.163.com')

email = '1697675111@qq.com'
password = '109291ac'
pop3_server = 'pop.qq.com'

server = poplib.POP3_SSL(pop3_server)

print(server.getwelcome())

server.user(email)
server.pass_(password)
print(server.stat())
