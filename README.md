# Ciqual API

## The [CIQUAL](https://ciqual.anses.fr/) project 

The French food composition database is run by CIQUAL in the Observatory of Food, unit of ANSES (the French agency for food, environmental and occupational health safety).

The main tasks consist in:

- input and management of a reference database on food composition,
- contribution to risk assessment in nutrition, within the French agency for food, environmental and occupational health safety,
- communication and dissemination of food composition data to administrations, researchers, nutritionists, food companies and consumers.

## Install application

```bash
pyenv virtualenv ciqual-api
pyenv activate ciqual-api
pip install -r requirements
```

## Launch project

```bash
# create an admin user
flask initdb admin
# import the xml data into an SQLite database
flask initdb importxml
# run the API
flask run
```

## The API

### Endpoints

```python
# food
get('/api/foods')
get('/api/foods/<id>')
get('/search/food/<string:local>/<string:name>')

# group
get('/api/groups')
get('/api/groups/<id>')

# sub group
get('/api/sgroup')
get('/api/sgroup/<id>')

# sub sub group
get('/api/ssgroup')
get('/api/ssgroup/<id>')
```
