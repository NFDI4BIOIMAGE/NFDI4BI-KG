import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'dast2rdf')))
print(sys.path)
from dast2rdf import *

sheets = load_spreadsheet()

assert "Helpdesk & TA Duties" in sheets.keys()

sheets = load_spreadsheet()
dasts = clean_dasts(sheets)
all_names_set = dast_names(dasts)

assert len(all_names_set) == 8

assert get_wikidata_id("Ada Lovelace") is None
assert get_wikidata_id("Mohsen Ahmadi") == URIRef("http://www.wikidata.org/entity/Q91349605")


names = ["Jens Wendt"]
graph = dast2rdf(names)

assert len(graph) == 6
