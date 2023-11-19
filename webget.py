from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup
import sys
from datetime import datetime





class WebPage(QWebEngineView):
    def __init__(self,name):
        super().__init__()
        self.ur=""
        self.name=name
        

        self.t = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_contagem)
          # Timer dispara o sinal a cada 1000 milissegundos (1 segundo)
        self.contagem = 1
        self.peoples=[]

        self.timer2= QTimer(self)
        self.timer2.timeout.connect(lambda:self.page().toHtml(self.process_html))


        self.save = QTimer(self)
        self.save.timeout.connect(lambda:self.savee())





    def set(self,url):
        self.ur=url
        self.load(QUrl(url))
        self.show()
        self.loadFinished.connect(lambda: self.check())


    def click_div_with_id_prefix(self):
        script = f'''
            var elements = document.querySelectorAll("div[id^='see_prev'] > a");
            if (elements.length > 0) {{
                elements[0].click();
            }} else {{
                console.error("Element not found");
            }}
        '''
        self.page().runJavaScript(script)

        # Verificação do elemento após o clique
        self.check_element_after_click()


    def check_element_after_click(self):
        def check():
            self.page().toHtml(self.CheckOpenComment)
        # Agendar a verificação após um intervalo de tempo
        QTimer.singleShot(500, check)  # Intervalo de 5 segundos (5000 milissegundos)


    def check(self):
        url=self.url().toString()
        if self.ur==url:
            self.click_div_with_id_prefix()
        else:
            self.atualizar_contagem()


    def CheckOpenComment(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all('div', id=lambda x: x and x.startswith("see_prev"))
        if len(elements)!=0:
            self.click_div_with_id_prefix()
        else:
            self.OpenResponses()
            

    def OpenResponses(self):  

        script = f'''
            var links = document.querySelectorAll("div._2b1h > a");
            for (var i = 0; i < links.length; i++) {{
                links[i].click();
            }}
        '''
        self.page().runJavaScript(script)
        self.timer2.start(1000)
        

    def process_html_strong(self, html): 
        soup = BeautifulSoup(html, 'html.parser')
        strong_tags = soup.find_all('strong')
        coment={}
        for strong_tag in strong_tags:
            p = strong_tag.text
            if p in coment:
                coment[p]+=1
            else:
                coment[p]=1
        self.peoples.append(coment)


    def process_html(self, html):
        self.timer2.stop()
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', class_='_45m8')
        for link in links:
            texto_do_link = link.text

            url_do_link = link.get('href')
            url_do_link = "https://mcdonaldspt.m.workplace.com" + url_do_link

            self.t.append(url_do_link)


        links = soup.find_all('a', class_='_14v8 _4edm')
        for link in links:
            texto_do_link = link.text

            url_do_link = link.get('href')
            url_do_link = "https://mcdonaldspt.m.workplace.com" + url_do_link
            self.t.append(url_do_link)

        self.page().load(QUrl(self.t[0]))
        #self.timer.start(1500)

    def savee(self):
        try:
            f = open(self.name+".txt","a")
            f.write(str(self.peoples)+"\n"+str(self.ur)+"\n")
            f.close()
            self.peoples=[]
            self.save.stop()
            self.page().deleteLater()
            self.close()

        except:
            print("Erro")

    def atualizar_contagem(self):
        if self.contagem>len(self.t)-1:
            print("Save")
            self.page().toHtml(self.process_html_strong)
            print(self.peoples)

            self.t=[]
            self.contagem=1
            

            #print(self.peoples,"\n",len(self.peoples),"\n")
            self.timer.stop()
            self.save.start(1000)
            return

        self.page().toHtml(self.process_html_strong)
        self.page().load(QUrl(self.t[self.contagem]))
        self.contagem+=1


def main(urls):
    horario_atual = datetime.now()

    # Formata o horário de acordo com suas necessidades
    formato = "%Y-%m-%d %H:%M:%S"
    horario_formatado = horario_atual.strftime(formato)

    print("Horário atual:", horario_formatado)
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Joshua's Browser")

    for i in range(len(urls)):

        web_page = WebPage("teste")
        web_page.set(urls[i])
        app.exec_()
        print(i)
    horario_atual = datetime.now()

    # Formata o horário de acordo com suas necessidades
    formato = "%Y-%m-%d %H:%M:%S"
    horario_formatado = horario_atual.strftime(formato)

    print("Horário atual:", horario_formatado)



