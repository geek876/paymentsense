""" python3 -m venv venv
source venv/bin/activate
python -m pip install Flask==1.1.1
python -m pip install requests
python -m pip freeze > requirements.txt """


from flask import Flask, render_template
import requests 

app = Flask(__name__)

url = 'https://reqres.in/api/products'

@app.route('/')
def products():
  resp = requests.get(url=url)
  products = resp.json()['data']
  for page in range(2, resp.json()['total_pages']+1): 
    products.extend(requests.get(url=url+'?page='+str(page)).json()['data'])
  return render_template("products.html", products=products)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080, threaded=True)
