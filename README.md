<div align="center">
<h2>PRIX's REST API</h2>
</div>

<!-- #### Key Features:

- Inventory Costs - Add and view an ingredient's purchase quantity and price.
- Recipe Costs - View a recipe's total cost
  - Ingredient Cost - View a breakdown of an ingredient's cost for the amount used in a recipe.
- Recipe Sale Prices - Add and view sales prices per recipe batch and serving.
- Recipe Profits - View the profits of a recipe per batch and serving. -->

#### To Run

1. Clone the PRIX API repo to your machine
2. Cd into prix-api
3. Execute <code>python -m venv PrixEnv</code>
4. Execute <code>source ./PrixEnv/bin/activate</code>
5. Execute <code>pip install -r requirements.txt</code>
6. In **settings.py** add 'prixapi' to the 'INSTALLED APPS' list

\*Be sure to [visit the PRIX-client repo](https://github.com/tannerb9/PRIX-client) to set up the client-side app.

#### Tech Used

- Python
- Django REST Framework

#### ERD

<img src="prixapi/static/PRIX-ERD.png" width="100%" height="auto">

#### Contributors

Tanner Brainard
