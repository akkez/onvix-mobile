echo "Installing requirements"
pip install -r /app/requirements.txt

if [ ! -f /app/config/app.cfg ]; then
    echo "Creating config"
    python3 -c \
"import os; 
f = open('/app/config/app.cfg', 'w'); 
f.write('DEBUG = True\nSECRET_KEY = {}\n'.format(os.urandom(30))); 
f.close()"
fi