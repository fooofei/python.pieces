
import gdb


class cc(gdb.Command):
    # cc is our new gdb command 
    def __init__(self):
        super(self.__class__, self).__init__("cc", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv)!=1:
            print('error args count, should be 2')
            return
        value = argv[0]
        cnt = 0
        with open("/data/logs/xxxx.log","wb") as fw:
            while True:
                cmd = "((struct svr_client_session_s *){0})->age_prev".format(value)
                # cannot execute command direct, need to add call before expr
                #v = gdb.execute("call "+cmd,False,True)
                v = gdb.parse_and_eval(cmd)
                if v ==0:
                    print("v=0 cnt={0}".format(cnt))
                    break
                value = v
                cmd = "p ((struct svr_client_session_s *){0})[0]".format(value)
                out = gdb.execute(cmd,False, True)
                fw.write("cnt={0} {1}={2}\n".format(cnt,cmd,out))
                cnt += 1
                if cnt > 10000:
                    print("cnt over")
                    break
            print("break while")

cc()
