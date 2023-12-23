# coding=utf-8


# 如何实现在 sleep 时，也能被打断，根据退出事件被打断？
# 一个疑问 b.is_set() =  b.wait(timeout=0) ? 

def raw_sleep(t):
    import time
    time.sleep(t)


from threading import Event

g_exit_event = Event()


def better_sleep(t):
    g_exit_event.wait(t)  # 当 g_exit_event 被 set() 后，这里就会直接 return True， 否则这里时间截止后会返回 False


if __name__ == '__main__':
    pass
