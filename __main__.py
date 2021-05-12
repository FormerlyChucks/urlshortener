from flask import Flask, request, render_template, redirect
import yaml, uuid, os

directory = os.path.dirname(os.path.abspath(__file__))
yamlfile = os.path.join(directory, 'db.yml')
app = Flask(__name__,static_url_path='')
protocols = ['https','http']
with open(yamlfile) as db:
    config = yaml.safe_load(db)

def dump_it(data):
    with open(yamlfile,'w') as cf:
        yaml.dump(data,cf)
    return 'dumped!'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',total=config['totalurls'])

@app.route('/create', methods=['POST'])
def create():
    url = request.form.get('url')
    total = config['totalurls']
    if url != None:
        if url.split('://')[0] in protocols:
            _id = str(uuid.uuid4()).split('-')[0]
            config[_id] = {'url':url}
            config['totalurls']+=1
            dump_it(data=config)
            return render_template('index.html',total=total,new_url=f'{request.url_root}l/{_id}')
        else:
            return render_template('index.html',total=total,error='You must supply a valid URL!')
    else:
        return render_template('index.html',total=total,error='No URL was provided!')

@app.route('/l/<uid>/')
def uid(uid):
    if config.get(uid) != None:
        to_redirect = config[uid]['url']
        return redirect(to_redirect)
    else:
        return config.get(uid)

if __name__ == '__main__':
	app.run()
