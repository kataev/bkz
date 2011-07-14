import MySQLdb
from whs.agents.models import agent

def FetchOneAssoc(cursor) :
    data = cursor.fetchall()
    if data == None :
        return None
    desc = cursor.description

    d = []
    print len(data)
    for row in data:

        dict = {}
        for (name, value) in zip(desc, row) :
            dict[name[0]] = value
#        print dict['name']
        d.append(dict)

    return d


def agents():
    db= MySQLdb.connect('localhost','disp','disp','disp',use_unicode=True,charset='UTF8')
    cursor = db.cursor()
    cursor.execute("select * from agent order by id;")
    row = FetchOneAssoc(cursor)
    
    for r in row:
#        print r['id']
        name = r['name'].split(',')[0].replace(r"'\'",' ').replace('  ',' ').strip()
        form=''
        try:
            form =  r['name'].split(',')[1].strip()
        except :
            pass

        a = agent(pk=int(r['id']),name=name,form=form,type=0,address=r['address'],inn=r['inn'],account=r['schet'],phone=r['phone'],bank=r['bank'])
        print a.name
        a.save()

    db.close()
        
        

agents()