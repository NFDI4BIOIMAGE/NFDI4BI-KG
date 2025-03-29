# Imports
import pandas
import rdflib
from rdflib import Graph, URIRef,  Literal
from rdflib import RDF, FOAF, RDFS
import pandas
from SPARQLWrapper import SPARQLWrapper, JSON

# Namespaces
dast = rdflib.Namespace("http://purl.nfdi4bi.org/rdf/dast/")
dastp = rdflib.Namespace("http://purl.nfdi4bi.org/rdf/dast#")
WD = rdflib.Namespace("http://www.wikidata.org/entity/")
WDT = rdflib.Namespace("http://www.wikidata.org/prop/direct/")

# Functions
def load_spreadsheet(path=None):
    """ Load spreadsheet at path into a pandas DataFrame.

    :param path: The filepath or URL of the spreadsheet to load.
    :type  path: str

    """

    sheets = pandas.read_excel('/home/grotec/GerBI-Cloud/NFDI4BIOIMAGE Consortium/DaSt Team/Data Stewardship_documentation.xlsx', sheet_name=None, engine='openpyxl')

    return sheets

def clean_dasts(sheets):
    dasts = sheets['Expertise & assignment of reque']
    
    dasts.columns = dasts.loc[6]

    return dasts.drop(axis=0, labels=range(6))

def dast_names(dasts_df):
    all_names = set(
        [nm for nm in dasts_df.iloc[:8,0].dropna().values]
    )

    return all_names

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    return sparql.query().convert()

def get_wikidata_id(name):
    query = f"""PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX wd: <http://www.wikidata.org/entity/>

      select ?person ?personLabel where {{
        service wikibase:label {{bd:serviceParam wikibase:language "en" .}}
          ?person wdt:P31 wd:Q5;
                  wdt:P1344 | ^wdt:P710 wd:Q113500855;
                  rdfs:label ?name .
          filter(regex(?name, "{name}"))
    }}
    limit 1
    """


    endpoint_url = "https://query.wikidata.org/sparql"
    results = get_results(endpoint_url, query)

    if len(results["results"]["bindings"]) > 0:
        return URIRef(results["results"]["bindings"][0]['person']['value'])
    
    return None

def dast2rdf(dast_names):

    graph = Graph()
    graph.bind("wdt", str(WDT))
    graph.bind("wd", str(WD))
    graph.bind("", str(dast))
    graph.bind("this", str(dastp))
    graph.base = dast

    for name in sorted(dast_names):

        first_last = " ".join(name.split(" ")[:-1])
        subj = dast.term(f"DataSteward/{first_last.replace(' ', '_')}")

        graph.add((subj, RDF.type, FOAF.Person)) # Is a person.
        graph.add((subj, WDT.P31, WD.Q5))        # Is a human (wikidata)
        graph.add((subj, RDF.type, dast.term("DataSteward")))
        graph.add((subj, WDT.P1344, WD.Q113500855))        # Participant in nfdi4bioimage
        graph.add((subj, RDFS.label, Literal(f"{first_last}^^xsd:string")))

        wikidata_uri = get_wikidata_id(first_last)

        if wikidata_uri is not None:
            graph.add((subj, RDFS.seeAlso, wikidata_uri))
    return graph

def main():
  sheets = load_spreadsheet()
  dasts = clean_dasts(sheets)
  all_names_set = dast_names(dasts)

  graph = dast2rdf(all_names_set)

  graph.serialize("data_stewards--20250328.ttl")

if __name__ == "__main__":
    main()
