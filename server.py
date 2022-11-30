#!/usr/bin/env python3
"""
By Gregory Kupershmidt


Very simple HTTP server in python for logging requests
https://gist.github.com/bradmontgomery/2219997
https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
Usage::
    ./server.py -h
# ver 3 from http.server import BaseHTTPRequestHandler as HTTPRequestHandler
#  from http.server import HTTPServer
#

TBD:
    1. Add examples of server start parameters and curl usage example.
    2. Remove external openssl dependancy
    3. IMprove execution responce - wait and return all execution stdout and stderr to requester

    4. use threads or processes as described here https://pymotw.com/3/http.server
"""
#### uncomment bellow for multithreaded version
from socketserver import ThreadingMixIn, ForkingMixIn

#from SimpleHTTPServer import SimpleHTTPRequestHandler as HTTPRequestHandler
#from BaseHTTPServer import HTTPServer
import os
import sys
import ssl
import base64
import json
#import StringIO
#from cStringIO import StringIO
#import ipdb

ver=int(sys.version[0])

if ver==2:
    from SimpleHTTPServer import SimpleHTTPRequestHandler as HTTPRequestHandler
    from BaseHTTPServer import HTTPServer
    from cStringIO import StringIO
elif ver==3:
    from http.server import BaseHTTPRequestHandler as HTTPRequestHandler
    from http.server import HTTPServer
#    from http.server import ThreadingHTTPServer as ThreadingSimpleServer
    from io import StringIO
else:
    printf('can not run')
    exit(1)

class ThreadingSimpleServer (ThreadingMixIn,HTTPServer):
    """Handle requests in a separate thread."""

def printf(text):
    sys.stdout.flush ( )
    print("%s\n\r" % text)
    sys.stdout.flush ( )
    
    #if str(type(text))=="<class 'bytes'>":
    #    localtext=text.decode('utf-8')
    #else:
    #    localtext=text
    #print(localtext, flush=True)


class S ( HTTPRequestHandler ):
    DefaultHeader={'Content-type':'text/html'}
    Headers={}
    Headers.update(DefaultHeader)

    def IsAuthorized(self):

        global myargs, myauthvalue
        if (myargs['require_auth'] == False):
            return True
        else:
            gotauthvalue = self.headers.get ( 'Authorization','' )
            if (gotauthvalue == myauthvalue):
                # print "authotized"
                return True
            else:
                # print "Not authotized"
                return False

    def myresponse(self, err, text):
        # response, headers, content
        #global ResponseText
        #printf(self.Headers)
        reply_body=text.encode('utf-8')
        self.send_response ( err )

        # if (err==200):
        #   self.send_header('Content-type', 'text/html')
        if (err == 401):
            self.send_header ( 'WWW-Authenticate', 'Basic realm=\"You have to authenticate to get this\"' )
        else:
            for key in self.Headers:
                self.send_header ( key, self.Headers[key] )

        self.send_header ( 'Content-Length', str ( len ( ( reply_body ) ) ) )
        self.end_headers ( )
        #self.wfile.write ( u"{}\n\r".format ( ResponseText ).encode ( 'utf-8' ) )
        self.wfile.write(reply_body)

    def deal_err(self):
        errno=410
        temparr = self.path.split ( "/" )
        errstr = temparr[len ( temparr ) - 1]
        try:
            errno = int ( errstr )
        except:
            errno = 405 # default error
        self.myresponse(errno, '')


    def do_PUT(self):
        # curl -sS -X PUT --upload-file /etc/passwd  "${URL}" -v
        # wget -O- --method=PUT --body-file=somefile.txt -v "${URL}"

        if self.IsAuthorized ( ):
            filename = os.path.basename(self.path)
            if ("conflict").lower() in (os.path.dirname(self.path)):
                self.myresponse (409, "file %s already exist !!!\n" % filename)
            else:
                self.myresponse (201, "file %s stored succesfully\n" % filename)

            #self.myresponse(201,u'---OK---')
        else:
            self.myresponse(401,u'{"err": "Not Autorized"}')


    def do_GET(self):
        if self.IsAuthorized ( ):
            if (self.path.startswith("/err/")):
                self.deal_err()
            else:
                self.myresponse(200,"GET %s" % self.path)       
        else:
            self.myresponse(401,u'{"err": "Not Autorized"}')

    def do_POST(self):
        if self.IsAuthorized ( ):
            global ResponseText
            ResponseText = ''

            content_length = int ( self.headers['Content-Length'] )  # <--- Gets the size of data
            post_data = self.rfile.read ( content_length )  # <--- Gets the data itself

            if (self.path == '/raw'):
                printf ( post_data.decode ( 'utf-8' ) )
                self.myresponse(200,'\n')
            
            elif (self.path == '/pyexec'):
                code = base64.b64decode ( post_data.decode ( 'utf-8' ) )
                printf ( "Executing python code :::\n%s" % code.decode() )

                ResponseText = u'Executing python code: \n\r{}\n\r'.format ( code.decode() )
                mystderr = ''

                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                try:
                    exec (code)
                    pyerr=200
                except Exception as inst:
                    mystderr = str ( inst )
                    pyerr=409
                finally:
                    sys.stdout = old_stdout

                mystdout=redirected_output.getvalue()

                #ResponseText = u"%s--- output ---\n\r%s------8<------\n\r\n\r--- error  ---\n\r%s\n\r------8<------\n\r" % (ResponseText,mystdout,mystderr)
                ResponseText = u"%s---\n\rStdout:\n\r%s" % (ResponseText,mystdout)
                ResponseText = u"%s---\n\rStderr:\n\r%s" % (ResponseText,mystderr)
                ResponseText = u"%s\n\r---\n\r" % (ResponseText)
                self.myresponse(pyerr,ResponseText)

            elif (self.path == '/runcmd'):
                code = base64.b64decode ( post_data.decode ( 'utf-8' ) )
                printf ( "executing shell code:\n%s" % code )

                ResponseText = u'Executing python code: \n\r{}\n\r'.format ( str(code) )
                os.system ( code )
                self.myresponse(200,ResponseText)

            elif (self.path == '/runsee'):
                #curl -sS -X POST "${URL}/runsee" -d $(echo 'whoami'|base64)
                printf ( "executing_shell_code:")
                #code = base64.b64decode ( post_data.decode ( 'utf-8' ) )
                #codetext = str(code).format()
                code = base64.b64decode( post_data.decode('utf-8') ).decode('utf-8')

                printf ( "%s" % code)

                ResponseText = str(u'Executing shell code: \n\r{cmd}\n\r').format(cmd=code)
                try:
                    from subprocess import Popen, PIPE
                    process = Popen ( code, stdout=PIPE, stderr=PIPE, shell=True )
                    output, err = process.communicate ( )

                    ResponseText = u"%s---\n\rExit Code: %s\n\r" % (ResponseText, process.returncode)
                    ResponseText = u"%s---\n\rStdout:\n\r%s" % (ResponseText, output.decode('utf-8'))
                    ResponseText = u"%s---\n\rStderr:\n\r%s" % (ResponseText, err.decode('utf-8'))
                    ResponseText = u"%s---\n\r" % (ResponseText)
                    cmderr=200

                except Exception as inst:
                    excptxt = str ( inst )
                    ResponseText = u"%s---\n\rException:\n\r%s" % (ResponseText, excptxt)
                    cmderr=409

                self.myresponse(cmderr,ResponseText)

            elif (self.path == '/setheaders'):
                #curl -sS -X POST "${URL}/setheaders" -d $(echo '{"Message": "ABC"}'|base64)
                code = base64.b64decode( post_data.decode('utf-8') ).decode('utf-8')

                self.Headers.clear()

                d = json.loads ( code )
                self.Headers.update(d)
                self.Headers.update ( self.DefaultHeader )

                ResponseText="updated headers: %s\n" % self.Headers
                self.myresponse(200,ResponseText)
            
            elif ("download") in os.path.dirname(self.path).lower().split('/'):
                # curl <URL>/<path>/download/<path>/<filename> -d @<path-to-file>
                filename = os.path.basename(self.path)
                if ("conflict") in (os.path.dirname(self.path)):
                    self.myresponse (409, "file %s already exist !!!\n" % filename)
                else:
                    self.myresponse (201, "file %s stored succesfully\n" % filename)                

            else:
                ResponseText=u"POST %s\n\r" % self.path
                if (type(post_data)==type('x')):
                    ResponseText=u"%sDATA:\n\r%s\n\r" % (ResponseText,post_data) 
                else:
                    ResponseText=u"%sDATA is not printable\n\r" % ResponseText 
                self.myresponse(200,ResponseText)

        else:
            self.myresponse(401,u'{"err": "Not Autorized"}')

def run(server_class=HTTPServer, handler_class=S, port=8080):
    global myargs
    mycn = 'localhost'

    server_address = ('', port)
    #httpd = server_class ( server_address, handler_class )
    #httpd = ForkingSimpleServer (server_address, handler_class)
    ### - use import ubove 
    httpd = ThreadingSimpleServer (server_address, handler_class)

    '''
    printf("Python version: ")
    print(str(sys.version).format())
    printf ("%s.%s.%s" % (sys.version_info.major,sys.version_info.minor,sys.version_info.micro))
    '''

    '''
    printf("My args: ")
    printf(myargs)
    '''

    if myargs['usetls'] == True:
        proto = 'https'
        if myargs['createcert'] == True:
            if myargs['host'] != '':
                # set CN for certificate by specified myargs['host']
                mycn = myargs['host']
            elif myargs['ip'] != '':
                # set CN for certificate by specified myargs['ip']
                mycn = "%s.%s.xip.io" % (myargs['prefix'], myargs['ip'])
            else:
                # detect external IP and set CN accordinly
                import urllib2
                myurl = 'https://ipecho.net/plain'
                response = urllib2.urlopen ( myurl )
                html = response.read ( )
                myip = html.lower ( )
                mycn = "%s.%s.xip.io" % (myargs['prefix'], myip)

            # re-create certificate using current CN
            reqcmd = 'openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem -subj /CN=%s 2>/dev/null' % mycn
            import os
            os.system ( reqcmd )

        # wrap ssl here
        import ssl
        httpd.socket = ssl.wrap_socket ( httpd.socket, keyfile="key.pem", certfile='cert.pem', server_side=True )

        # Print out cert bundle and url
        myfile = 'cert.pem'
        f = open ( myfile, 'r' )
        mybundle = f.read ( )
        printf ( mybundle )
    else:
        proto = 'http'
        mycn = 'localhost'

    hookurl = '%s://%s:%s' % (proto, mycn, port)
    printf ( hookurl )
    printf ( '' )

    printf ( "Listening on port %s ...\n" % str ( port ) )
    sys.stdout.flush ( )

    try:
        httpd.serve_forever ( )
        sys.stdout.flush ( )
    except KeyboardInterrupt:
        pass
    httpd.server_close ( )
    # logging.info('Stopping httpd...\n')
    printf ( 'Stopping httpd...\n' )




if __name__ == '__main__':
    # from sys import argv
    import argparse

    parser = argparse.ArgumentParser ( description='Yay!' )
    parser.add_argument ( '-P', default=8080, type=int, dest='port', help='listening port' )
    parser.add_argument ( '-u', default='user', dest='user', help='username' )
    parser.add_argument ( '-p', default='tecres', dest='password', help='password' )
    parser.add_argument ( '-a', default=False, type=bool, dest='require_auth', help='require basic auth credentials' )
    parser.add_argument ( '-c', default=False, type=bool, dest='createcert', help='(re)create certificate' )
    parser.add_argument ( '-i', default='', dest='ip',
                          help='explicit IP for xip.io=based url for cert regeneration, empty value (default) will cause external ip detection' )
    parser.add_argument ( '-s', default='', dest='host', help='explicit hostname for cert regeneration' )
    parser.add_argument ( '-x', default='webhook-test', dest='prefix',
                          help='explicit prefix for xip.io-based url for cert regeneration' )
    parser.add_argument ( '-t', default=False, type=bool, dest='usetls', help='use TLS' )

    myargs = vars ( parser.parse_args ( ) )
    ResponseText = u''
    # printf myargs

    if myargs['require_auth'] == True:
        credstr = "%s:%s" % (myargs['user'], myargs['password'])
        myauthkey = base64.b64encode(credstr.encode()).decode()
        myauthvalue = "Basic %s" % myauthkey

        printf ( '''For proper authorization use :
                curl --user %s 
                \ror 
                curl -X POST -H "Authorization: %s"''' % (credstr, myauthvalue) )


    run ( port=myargs['port'] )
