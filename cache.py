#!/usr/bin/python3

import webapp
import urllib

class CacheApp (webapp.webApp):
    contNav = 0
    contSer = 0
    contApp = 0
    dicNav = {}
    dicSer = {}
    dicApp = {}


    def parse(self, request):
        self.dicNav[self.contNav] = request
        self.contNav = self.contNav + 1
        try:
        	resource = request.split(' ', 2)[1][1:] # quita tambien la barra
        except IndexError:
        	resource = ''

        return resource

    def process(self, resource):
        #Primero me quedo con la pagina que piden
        #try:
        recurso = resource.split('/')[0]
        print ("TROCEO")
        if recurso == "reload":
            resource = resource.split('/')[1]
            print ("RECARGO")
        #except IndexError:

			#print("Error al intentar quedarme con la pagina")
        url = 'http://' + resource

        if resource == "HeaderNav":
            httpCode = "200 Ok"
            htmlBody = str(self.dicNav.items())
        elif resource == "HeaderServ":
            httpCode = "200 Ok"
            htmlBody = str(self.dicSer.items())
        elif resource == "HeaderApp":
            httpCode = "200 Ok"
            htmlBody = str(self.dicApp.items())
        else:
            try:
                pagina = urllib.urlopen(url)
                self.dicSer[self.contSer] = pagina.info().headers
                self.contSer = self.contSer + 1
                cuerpo = pagina.read()
                primero = cuerpo.find("<body")
                segundo = cuerpo.find(">", primero)
                enlaces = "<a href=" + url + "> Original Webpage </a>" \
                        + "<a href=/reload/" + resource + "> Refresh </a>" \
                        + "<a href=/HeaderNav> Client-to-App-Side HTTP </a>" \
                        + "<a href=/HeaderApp> App-to-Client-Side HTTP </a>" \
                        + "<a href=/HeaderServ> Server-to-App-Side HTTP </a>" \
        				+ "\n" + "</br></br"
                cuerpo = cuerpo[:segundo+1] + enlaces + cuerpo[segundo+1:]

                httpCode = str(pagina.getcode())
                htmlBody = cuerpo
            except:
                htmlBody = "Could not connect"
                httpCode = "404 Not Found"
            self.dicApp[self.contApp] = httpCode
            self.contApp = self.contApp + 1

        print ("el contador de App2Nav va -> " + str(self.contApp) + "\n")
        print ("el contador de Nav2App va -> " + str(self.contNav) + "\n")
        print ("el contador de Ser2App va -> " + str(self.contSer) + "\n")

        return (httpCode, htmlBody)

if __name__=="__main__":
    testCacheApp = CacheApp("localhost", 1234)
