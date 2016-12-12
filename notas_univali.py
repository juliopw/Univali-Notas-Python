#	 _______________________________________________________________________________
#	|	 		Old version of the script. May work with some changes.				|
# 	|	 Versão antiga do script. Pode ser que funcione com algumas modificações.	|
#	|								-	Python 2.7	-								|
#	| 	 	Simula um navegador acessando a página da Univali, recolhendo as		|
# 	|					informações de notas e mostrando na tela.					|
#	|_______________________________________________________________________________|
#

# -*- coding: cp1252 -*-
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup 
import html2text
import json

# Navegador
br = mechanize.Browser()

# Cookies
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Opcoes do navegador
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36')]

# Abre a url para que sejam preenchidas as informacoes de login
br.open('https://intranet.univali.br/intranet/')

# Seleciona o segundo formulario (indice 0) o primeiro é uma caixa de busca
br.select_form(nr=1)

# Credenciais do usuario
br.form['ca_usuario'] = 'usuario'
br.form['ca_senha'] = 'password'

# Login
br.submit()

req = br.click_link(text='Portal do Aluno (Acadêmico/Financeiro)')

soup = BeautifulSoup(br.open(req))

links_html = soup.find('table',attrs={'class':'formtable'})

links = [None] * len(links_html.findAll('a', href=True))

for i,link in enumerate(links_html.findAll('a', href=True)):
    print i, link.text.strip().title().replace("  ", "")
    links[i] = link['href']

x = raw_input('\n\tCurso: ')

link = links[int(x)]

print link

br.open(link)


soup = BeautifulSoup(br.open(link))
link = soup.find('span',attrs={'id':'W0007MNUNOTAS'}).find('a', href=True)
link = '//fiaiweb01.univali.br/portal3/' + link['href']


soup = BeautifulSoup(br.open(link))
json_data = soup.find('input',attrs={'name':'GridnotasContainerDataV_0001'})
json_data = json_data['value']

Medias = json.loads(json_data)

# Estrutura do Medias:

#  Medias[0][0]		        Link M1
#  Medias[0][1]		        Link M2
#  Medias[0][2]		        Link M3
#  Medias[0][7]		        Codigo da disciplina
#  Medias[0][8]		        Nome da disciplina
#  Medias[0][9]		        Nota	M1
#  Medias[0][10]		Faltas	M1
#  Medias[0][11]		Nota	M2
#  Medias[0][12]		Faltas	M2
#  Medias[0][13]		Nota	M3
#  Medias[0][14]		Faltas	M3
#  Medias[0][21]		Frequencia [S/N]
#  Medias[0][22]		Media Final
#  Medias[0][24]		Situacao [Em aberto/Aprovado/Reprovado]

avaliacoes = []
avaliacoesPorM = []

for index in range(len(Medias)):
    for i in range(0,3):
        link = '//fiaiweb01.univali.br/portal3/' + Medias[index][i]
        soup = BeautifulSoup(br.open(link))
        json_data = soup.find('input',attrs={'name':'Subfile1ContainerDataV'})
        json_data = json_data['value']
        avaliacoesPorM.append(json.loads(json_data))
    avaliacoes.append(avaliacoesPorM)
    avaliacoesPorM = []

# Estrutura do avaliacoes:

#  avaliacoes[Materia][Mx][Atividade][0]	        Data da avaliação/trabalho
#  avaliacoes[Materia][Mx][Atividade][1]	        Devolução oficial
#  avaliacoes[Materia][Mx][Atividade][2]	        Tipo
#  avaliacoes[Materia][Mx][Atividade][3]	        Avaliação
#  avaliacoes[Materia][Mx][Atividade][4]	        Peso
#  avaliacoes[Materia][Mx][Atividade][5]	        Nota
#  avaliacoes[Materia][Mx][Atividade][10]	        Código da disciplina
#  avaliacoes[Materia][Mx][Atividade][11]	        Código do curso

for index in range(len(Medias)):
    print('\n\n' + Medias[index][8].strip().title())
    
    print('\n\tM1 - ' + Medias[index][9].strip())
    for i in range(len(avaliacoes[index][0])):
        print('\t\t- ' + avaliacoes[index][0][i][3].strip().title()
              + '\n\t\t\tPeso: ' + avaliacoes[index][0][i][4].strip()
              + '\tNota: ' + avaliacoes[index][0][i][5].strip())
        
    print('\n\tM2 - ' + Medias[index][11].strip())
    for i in range(len(avaliacoes[index][1])):
        print('\t\t- ' + avaliacoes[index][1][i][3].strip().title()
              + '\n\t\t\tPeso: ' + avaliacoes[index][1][i][4].strip()
              + '\tNota: ' + avaliacoes[index][1][i][5].strip())
        
    print('\n\tM3 - ' + Medias[index][13].strip())
    for i in range(len(avaliacoes[index][2])):
        print('\t\t- ' + avaliacoes[index][2][i][3].strip().title()
              + '\n\t\t\tPeso: ' + avaliacoes[index][2][i][4].strip()
              + '\tNota: ' + avaliacoes[index][2][i][5].strip())
    



f = open('workfile.json', 'w')

f.write(json_data.encode('utf8'))

f.close()
