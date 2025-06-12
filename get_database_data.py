import psycopg2
import xml.etree.ElementTree as ET
from livereload import Server
from decouple import config
# ——————————————————————————————  
# 1. Fetch from DB & build HTML  
# ——————————————————————————————

#  ————————————————————————————————————————————————————————————  
#    check the .env folder(importing variable from the .env)
#  ———————————————————————————————————————————————————————————— 
DB_HOST = config('DB_HOST', default='localhost')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')


def build_html():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME,
        user=DB_USER, password=DB_PASS

    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM module_one_note;")
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()

    root = ET.Element('html')
    head = ET.SubElement(root, 'head')
    ET.SubElement(head, 'meta', charset='utf-8')
    ET.SubElement(head, 'title').text = 'Module One Notes'
    style = ET.SubElement(head, 'style')
    style.text = """
    table {border-collapse: collapse; width: 100%;}
    th, td {border: 1px solid #ddd; padding: 8px;}
    th {background-color: #f4f4f4;}
    """
    body = ET.SubElement(root, 'body')
    ET.SubElement(body, 'h1').text = 'Module One Notes'
    table = ET.SubElement(body, 'table')
    hdr_row = ET.SubElement(table, 'tr')
    for h in headers:
        ET.SubElement(hdr_row, 'th').text = h

    for row in rows:
        tr = ET.SubElement(table, 'tr')
        for cell in row:
            ET.SubElement(tr, 'td').text = str(cell)

    ET.indent(root, space='  ')  # prettify

    html_str = ET.tostring(root, encoding='unicode', method='html')
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_str)

# ——————————————————————————————  
# 2. Serve with auto-reload  
# ——————————————————————————————
def serve():
    build_html()
    server = Server()
    server.watch('generate_and_serve.py', build_html)
    server.watch('output.html')  # trigger reload
    server.serve(root='.', port=8000, open_url_delay=1)

if __name__ == '__main__':
    serve()
