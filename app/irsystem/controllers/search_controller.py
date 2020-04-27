from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import search_drinks
from app.irsystem.models.database import query_embeddings

project_name = "Pick Your Poison"
net_id = """
Collin Montag (cm759),
Derek Cheng (dsc252),
DB Lee (dl654),
Dana Luong (dl697),
Ishneet Sachar (iks23)
"""

@irsystem.route('/descriptors', methods=['GET'])
def serve_desc():
	descriptors = sorted([e.word for e in query_embeddings()])
	descriptors = [d.replace('_', ' ') for d in descriptors]
	return render_template('desc_list.html', descriptors=descriptors)

@irsystem.route('/', methods=['GET'])
def search():

	# FOR TESTING PURPOSES #
	if request.args.get('test'):
		return render_template('test.html')

	drink_type = request.args.get('type')
	descriptors = request.args.get('descriptors')
	
	if drink_type and descriptors:
		desc_lst = [d.strip().lower().replace(' ', '_') for d in descriptors.split(',')]
		print("User searched for a {} with descriptors: {}".format(drink_type, descriptors))

		if drink_type == 'anything':
			drink_type = None
		results = search_drinks(desc_lst, dtype=drink_type, k=10)

		if results is not None:

			# for drink in results:
			# 	print(drink[0].name)
			# 	print(drink[0].description)
			# 	print(drink[0].price)
			# 	print(drink[0].origin)
			# 	print(drink[0].type)

			return render_template('results.html', results=results)

	descriptors = [e.word.replace('_', ' ') for e in query_embeddings()]

	return render_template('search.html', descriptors=descriptors)
