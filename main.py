import code
import requests
from lxml import html
from getpass import getpass
import operator


username = None
while not username:
    username = input("Digite seu usuário: ")
    if not username:
        print("Eu realmente preciso saber o seu usuário \nPressione Ctrl+C para cancelar e sair")

password = None
while not password:
    password = getpass("Digite sua senha: ")
    if not password:
        print(
            "Eu realmente preciso saber o sua senha \nPressione Ctrl+C para cancelar e sair")

session = requests.Session()
data = {'username': username, 'password': password}
print("Realizando Login")
login_response = session.post(
    "https://on.fiap.com.br/fiaplogin/index.php", data=data)


parsed_login_body = html.fromstring(login_response.text)
main_divs_xpath = '//div[@class="conteudo-digital-list"]//div[contains(@class, "is-realizado")]'
main_divs = parsed_login_body.xpath(main_divs_xpath)

links = []
for div in main_divs:
    if "avaliado" in div.text_content():
        link = div.findall(".//a[@href]")[0].get("href")
        links.append(link)

print("Buscando atividades avaliadas")
grades = []
for link in links:
    response = session.get(link)
    parsed_response = html.fromstring(response.text)
    activity_name = parsed_response.find('.//h2').text
    feedback_el = parsed_response.find('.//div[@class="feedback"]')
    activity_id = int(activity_name.split(" - ")[0].split("Cap ")[-1])
    grades.append({
        'atividade': activity_name,
        'feedback': feedback_el.text_content(),
        'id': activity_id
    })

grades.sort(key=operator.itemgetter('id'))
for grade in grades:
    print(" = = = = = = = = = = = = = = = = = =")
    print(grade['atividade'])
    print(grade['feedback'])
