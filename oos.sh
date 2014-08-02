#!/bin/bash

# failover for openoffice server

while :
do
/usr/bin/soffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --norestore --nofirstwizard --nologo --headless
done

