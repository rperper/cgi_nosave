import os, resource, datetime 
from datetime import datetime
from datetime import timedelta
from datetime import time
from time import ctime

def application(environ, start_response):
   entryTime = ctime(None)
   start_time = datetime.now()

   rm = environ['REQUEST_METHOD']
   size = environ['CONTENT_LENGTH']
   remain = int(size)
   blockSize = 262144
   data = ''
   index = 0
   header = True 
   while (remain):
      toRead = remain;      
      if (toRead > blockSize):
         toRead = blockSize
      block = environ['wsgi.input'].read(toRead)
      if (header):
          EOL = block.find("\r\n")
          signature = block[0:EOL]
          params = ''
          EOL += 2
          newEOL = block[EOL:].find("\r\n")
          params = block[EOL:EOL+newEOL]
          filepos = params.find('filename="')
          filepos += 10
          filename = params[filepos:filepos+params[filepos:].find('"')]
          fullfilename = os.getcwd() + "/upload/" + filename
          output = open(fullfilename,"wb")
          EOL += newEOL + 2
          while (newEOL > 0):
              newEOL = block[EOL:].find("\r\n")
              if (newEOL > 0):
                  EOL += newEOL + 2
          if (newEOL == 0):
              EOL += 2 # Get past the final one
          header = False
          EOD = block[EOL:].find(signature)
          if (EOD > 0):
              output.write(block[EOL:EOL + EOD - 2])
          else:
              output.write(block[EOL:])
      else:
          if (toRead < blockSize):
              EOD = block.find(signature)
              if (EOD > 0):
                  output.write(block[:EOD - 2])
          else:
              output.write(block)
      remain = remain - toRead
      
   end_time = datetime.now()
   total_time = end_time - start_time
   str_time = str(total_time.total_seconds())
   completionTime = ctime(None)
   output.close()
   start_response('200 OK', [('Content-Type', 'text/plain')])
   message = 'Initial query: ' + rm + ' Size: ' + size + ' Entry time: ' + entryTime + ' Completion time: ' + completionTime + ' Total time: ' + str_time + ' seconds ' + ' Block size: ' + str(blockSize) + ' bytes, filename: ' + fullfilename + '\n'
   return [message]
