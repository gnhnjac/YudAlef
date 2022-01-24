import requests

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Length': '313',
'Content-Type': 'application/x-www-form-urlencoded',
'Cookie': 'JSESSIONID=72B2DD9D6EA7B0359360F0E485B2CE20',
'Host': 'www.022.co.il',
'Origin': 'https://www.022.co.il',
'Referer': 'https://www.022.co.il/BRPortal/br/P004.jsp?vhost=www.2011.herzog.hs.ksedu.co.il&key=fpbJVBzCezOejD5rr79r1599049293256&tm=1599049293256&hijkses=false',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

payload = {
'username1': 'dummy-user1',
'username2': 'dummy-user2',
'password1': 'dummy-password1',
'password2': 'dummy-password2',
'form1:name': '215013400',
'form1:password': '361617',
'com_sun_rave_web_ui_appbase_renderer_CommandLinkRendererer': 'form1:enter',
'clickedby': '?',
'current_page_url': '?',
'form1_hidden': 'form1_hidden',
'com.sun.faces.VIEW': '_id5956:_id5957'}

session = requests.Session()

res = session.post("https://www.022.co.il/BRPortal/br/P004.jsp?vhost=www.2011.herzog.hs.ksedu.co.il&key=JyAGRzxx297NBf4MAkew1599048953141&tm=1599048953141&hijkses=false", headers=headers, data=payload)

print(res.status_code)