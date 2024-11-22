from common import *

us='''
* Complex US

   As a:  Member
 I want:  To view all pinned messages in a specific channel 
So That:  I can I can view important messages 
'''

print(us)

def list_pinned_messages():

    cols = 'm.message_id m.message_content c.channel_id u.user_id u.user_name'

    tmpl =  f'''
SELECT {c(cols)}
  FROM Messages as m
       JOIN Channel as c ON m.channel_id = c.channel_id
       JOIN Users as u ON m.user_id = u.user_id
 WHERE m.is_pinned = True 
'''
    cmd = cur.mogrify(tmpl, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    # pp(rows)
    show_table( rows, cols )

list_pinned_messages()    
