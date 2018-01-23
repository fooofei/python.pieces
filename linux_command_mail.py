# coding=utf-8

'''
the file shows how to use linux command `mail` to send html content
linux mail command usage

# 多行书写
$ mail -s "Hello World" someone@example.com
Cc:
Hi Peter
How are you
I am fine
Good Bye
<Ctrl+D>

# 一行书写
$ mail -s "This is the subject" somebody@example.com <<< 'This is the message'

# 一行书写
$ echo "This is the body" | mail -s "Subject" -aFrom:Harry\<harry@gmail.com\> someone@example.com

# 通过文件发送
$ mail -s "Hello World" user@yourmaildomain.com < /home/user/mailcontent.txt

# 通过管道发送
$ echo "This is the message body" | mail -s "This is the subject" mail@example.com

# 多个接收人
$ mail -s "Hello World" user1@example.com,user2@example.com


# 发送 html 格式内容 标注内容编码 (注意双引号不需要转义)
echo "你好<br>是我" | mail  -s "$( echo -e "this is title\nContent-Type: text/html;charset=UTF-8 ")"  user1@example.com



# 发送 base64    base64(hello) = aGVsbG8=
# 格式 =?utf-8?<Q/B>?<content>?=   B 是 base64 的意思 Q 是 quoted-printable

    # 成功
    echo "aGVsbG8=" | mail  -s "$( echo -e "this is title\nContent-Transfer-Encoding: base64\r\nContent-Type: text/html;charset=UTF-8 ")"  user1@example.com

    # 带 html 标记的 base64 内容
    echo "aGVsbG88YnI+aGVsbG8=" | mail  -s "$( echo -e "this is title\nContent-Transfer-Encoding: base64\r\nContent-Type: text/html;charset=UTF-8 ")"  user1@example.com
    # 发送成功 邮件标题是 hello
    echo "aGVsbG88YnI+aGVsbG8=" | mail  -s "$( echo -e "=?utf-8?B?aGVsbG8=?=\nContent-Transfer-Encoding: base64\r\nContent-Type: text/html;charset=UTF-8 ")"  user1@example.com

    # 失败 看来只能解析原始的 base64
    echo "=?utf-8?B?aGVsbG8=?=" | mail  -s "$( echo -e "this is title\nContent-Transfer-Encoding: base64\r\nContent-Type: text/html;charset=UTF-8 ")"  user1@example.com

可以使用 python 解码
>>> from email.header import decode_header
>>> decode_header('=?iso-8859-1?q?p=F6stal?=')
[(b'p\xf6stal', 'iso-8859-1')]

'''


def linux_command_mail(content, subject, receiver):
  '''
  - 都要使用 unicode
  - 可以有中文
  '''
  import sh
  import base64

  mail = sh.mail
  echo = sh.echo

  content = content.encode('utf-8')
  content = base64.b64encode(content)
  subject = subject.encode('utf-8')
  subject = base64.b64encode(subject)
  subject = '=?utf-8?B?{0}?='.format(subject)

  mail(echo(content), '-s',
       '{0}\nContent-Transfer-Encoding: base64\r\nContent-Type: text/html;charset=UTF-8'.format(subject),
       receiver)


def entry():
  v = []
  v.append(u'测试1')
  v.append(u'测试2')
  v.append(u'测试3![]=')
  v.append(u'测试4![]=')

  v = u'<br/>'.join(v)

  linux_command_mail(
    v,
    u'测试标题',
    u'example@excample.com'
  )


if __name__ == '__main__':
  entry()
