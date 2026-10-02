from oaipmh_scythe import Scythe
from bs4 import BeautifulSoup
from rdflib import Graph, Namespace, URIRef, Literal, BNode, FOAF, DC, XSD, RDF, RDFS

import logging
logging.basicConfig(level=logging.WARNING)

def parse_person(graph, person):

    orcid = person.find('nameIdentifier', attrs={'nameIdentifierScheme':'ORCID'})

    # Parse given name
    given_name = person.find('givenName')
    if given_name is not None:
        given_name = given_name.string
    else:
        given_name = ""

    # Parse family name
    family_name = person.find('familyName')
    if family_name is not None:
        family_name  = family_name.string
    else:
        family_name = ""
    name = given_name + " " + family_name

    if name == " ": name = "NN"

    if orcid is None:
        try:
            person_uri = next(graph.subjects(predicate=RDFS.label, object=Literal(name)))
        except StopIteration:
            person_uri = BNode()

        except:
            raise
    else:
        person_uri = ORCID[orcid.string]
        graph.add((person_uri, DCITE.identifier, Literal(person_uri, datatype=XSD.anyURI)))
        
    graph.add((person_uri, RDF.type, FOAF.Person))
    graph.add((person_uri, RDFS.label, Literal(name)))
    graph.add((person_uri, DCITE.givenName, Literal(given_name)))
    graph.add((person_uri, DCITE.familyName, Literal(family_name)))

    # Get affiliations.
    # Skip nfdi4bioimage because it's not an affiliation in the legal sense.
    affiliations = (aff for aff in person.find_all('affiliation') if not aff.get('affiliationIdentifier', "").split('/')[-1] == '01vnkaz16')
    for affiliation in affiliations:
        graph, affiliation_ref = parse_institution(graph, affiliation)
        graph.add((person_uri, DCITE.affiliation, affiliation_ref))

    return graph, person_uri

def parse_institution(graph, institution):
    """ Parse identifier and name of (academic) institution """

    identifier = institution.get('affiliationIdentifier', None)

    # If no identifier, return blank node with only the name.
    if identifier is None:

        # Identify institution by name string.
        predicate = RDFS.label
        object = Literal(institution.string)

        # First see if this institution is already in the graph
        try:
            bn = next(graph.subjects(predicate=predicate, object=object))
        except StopIteration:  # not found, create it
            bn = BNode()

            graph.add((bn, RDFS.label, Literal(institution.string)))
            graph.add((bn, RDF.type, OBI['0000245']))

        except:
            raise

        return graph, bn

    # If we have an id, get its scheme, too.
    identifier_scheme = institution.get('affiliationIdentifierScheme')

    # Handle ROR
    if identifier_scheme == "ROR":
        ror_uri = URIRef(identifier)
        graph.add((ror_uri, RDF.type, OBI['0000245']))
        graph.add((ror_uri, RDFS.label, Literal(institution.string)))
        graph.add((ror_uri, DCITE.identifier, Literal(identifier, datatype=XSD.anyURI)))

        return graph, ror_uri

    # If not a ROR, return blank node with name and id as string.
    # But first check if institution with this identifier already exists
    try:
        bn = next(graph.subjects(predicate=DCITE.identifier, object=Literal(identifier)))
    except StopIteration:
        bn = BNode()
        graph.add((bn, RDFS.label, Literal(institution.string)))
        graph.add((bn, DCITE.identifier, Literal(identifier)))
        graph.add((bn, RDF.type, OBI['0000245']))

    except:
        raise

    return graph, bn

def parse_date(date):
    date_type = date.get('dateType')

    return DCITE[date_type], Literal(date.string, datatype=XSD.date)

def parse_relation(relation):
    rel_id_tpe = relation.get('relatedIdentifierType')
    rel_tpe = relation.get('relationType')

    if rel_id_tpe == "URL":
        return DCITE[rel_tpe], URIRef(relation.string)
    else:
        return DCITE[rel_tpe], ns_dict[rel_id_tpe.lower()][relation.string]

# Init graph.
graph = Graph(bind_namespaces='rdflib')

# Namespaces and prefixes.
ns_dict = dict([
    ("datacite", DCITE := Namespace("https://schema.datacite.org/meta/kernel-4.6/metadata.xsd#")),
                ("nfdicore", NFDI  := Namespace("https://nfdi.fiz-karlsruhe.de/ontology/")),
                ("orcid"   , ORCID := Namespace("https://orcid.org/")),
                ("ror"     , ROR   := Namespace("https://ror.org/")),
                ("doi"     , DOI   := Namespace("https://doi.org/")),
                ("obi"     , OBI   := Namespace("http://purl.obolibrary.org/obo/OBI_")),
                ("t4fs"    , T4FS  := Namespace("http://purl.obolibrary.org/obo/T4FS_")),
                ("sio"     , SIO   := Namespace("http://semanticscience.org/resource/")),
])

for prefix, ns in ns_dict.items():
    graph.bind(prefix, ns)

# Add core information about NFDI4BIOIMAGE.
n4bi = URIRef("https://nfdi4bioimage.de/rdf/node")
n4bicomm = URIRef("https://zenodo.org/communities/nfdi4bioimage")

graph.add((n4bi     , NFDI.NFDI_0000195, n4bicomm))                                                   # We have a collection aka zenodo community.
graph.add((n4bicomm , DC.identifier,     Literal('nfdi4bioimage')))                                   # Our collection has an identifier ...
graph.add((n4bicomm , NFDI.NFDI_0001008, Literal('https://zenodo.org/communities/nfdi4bioimage')))    # ... and a website.

# Harvest the zenodo OAI-PMH API endpoint.
with Scythe("https://zenodo.org/oai2d") as scythe:
  records = scythe.list_records(set_='user-nfdi4bioimage', metadata_prefix='oai_datacite')


# `records` is a list of xml strings.
# Loop over all records.
for i, rec0 in enumerate(records):

  # Get a proper navigable xml object.
  xml_root = BeautifulSoup(str(rec0), 'xml').find('resource')

  # Get the record's DOI.
  doi = xml_root.find('identifier', attrs={"identifierType":"DOI"})

  # The record's DOI is the subject for most of the triples to be constructed.
  subj = URIRef("https://doi.org/"+doi.string)

  # Add record as part of community.
  graph.add((n4bicomm, SIO.SIO_000088, subj))

  # Get creators and contributors.
  title = xml_root.find('title')
  description = xml_root.find('description')
  resource_type = xml_root.find('resourceType')
  subjects = xml_root.find_all('subject')
  rights = xml_root.find_all('rights')

  creators = xml_root.find_all('creator')
  contributors = xml_root.find_all('contributor')
  affiliations = xml_root.find_all('affiliation')
  relations = xml_root.find_all('relatedIdentifier')
  dates = xml_root.find_all('date')

  graph.add((subj, RDF.type, T4FS['0000113']))
  graph.add((subj, DCITE.title, Literal(title.string)))

  if description is not None:
      graph.add((subj, DCITE.description, Literal(description.string)))

  if resource_type is not None:
      graph.add((subj, DCITE.resourceType, Literal(resource_type.string)))

  for subject in subjects:
      graph.add((subj, DCITE['subject'], Literal(subject.string)))

  for right in rights:
      graph.add((subj, DCITE['right'], Literal(right.string)))

  for creator in creators:
      graph, person = parse_person(graph, creator)
      graph.add((subj, DCITE.creator, person))

  for contributor in contributors:
      graph, person = parse_person(graph, contributor)
      graph.add((subj, DCITE.contributor, person))

  for date in dates:
      try:
          property, val = parse_date(date)
          graph.add((subj, property, val))
      except ValueError:
          logging.warning("Could not convert string %s to xsd:date literal.", str(date))
          pass
      except:
          raise

  for relation in relations:
      property, val = parse_relation(relation)
      graph.add((subj, property, val))

graph.serialize('/home/grotec/org/repos/NFDI4BI-KG/RDF_dumps/n4bi_zenodo_community.n3')

print(len(graph))
