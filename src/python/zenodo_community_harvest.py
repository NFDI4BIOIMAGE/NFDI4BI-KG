from oaipmh_scythe import Scythe
from rdflib import Graph, BNode, Literal, URIRef, DC, FOAF, XSD, RDF, RDFS, Namespace

SIO = Namespace('http://semanticscience.org/resource/')
ZND = Namespace('https://zenodo.org/')
zenodo = Namespace('https://zenodo.org/ns/')

def add_persons(graph, person_list, property_term):
  for c in person_list:
      bn = BNode()
      name_str = c.split(", ")
      if len(name_str) > 1:
        last = name_str[0]
        first = ", ".join(name_str[1:])
        graph.add((bn, FOAF.firstName, Literal(first)))
        graph.add((bn, FOAF.lastName, Literal(last)))
      else:
        graph.add((bn, FOAF.name, Literal(name_str)))

      graph.add((subject, property_term, bn))

  return graph

g = Graph(bind_namespaces='rdflib')
g.bind("sio", SIO)
g.bind("znd", ZND)
g.bind("zenodo", zenodo)

n4bi = URIRef("https://kg.nfdi4bioimage.de")
n4bicomm = URIRef("https://zenodo.org/communities/nfdi4bioimage")

g.add((n4bi, zenodo.community, n4bicomm))
g.add((n4bicomm, RDF.type, SIO.SIO_001064))
g.add((n4bicomm, DC.identifier, Literal('user-nfdi4bioimage')))
g.add((n4bicomm, SIO.SIO_000296, Literal('https://zenodo.org/communities/nfdi4bioimage')))

with Scythe("https://zenodo.org/oai2d") as scythe:
  records = scythe.list_records(set_='user-nfdi4bioimage')


for rec0 in records:

  creator = rec0.metadata.get('creator', [])
  date = rec0.metadata.get('date', [])
  description = rec0.metadata.get('description', [])
  identifier = rec0.metadata.get('identifier', [])
  publisher = rec0.metadata.get('publisher', [])
  relation = rec0.metadata.get('relation', [])
  rights = rec0.metadata.get('rights', [])
  subjects = rec0.metadata.get('subject', [])
  title = rec0.metadata.get('title', [])
  tpe = rec0.metadata.get('type', [])

  subject = URIRef(rec0.metadata['identifier'][0])

  g.add((n4bicomm, SIO.SIO_000088, subject))

  g = add_persons(g, contributor, DC.contributor)
  g = add_persons(g, creator, DC.creator)
  g.add((subject, DC.publisher, Literal(publisher)))
  g.add((subject, DC.date, Literal(date, datatype=XSD.date)))
  g.add((subject, DC.description, Literal(description)))

  for right in rights:
      g.add((subject, DC.rights, Literal(right)))

  for sbjct in subjects:
      g.add((subject, DC.subject, Literal(sbjct)))

  for t in title:
      g.add((subject, DC.title, Literal(t)))

  for rel in relation:
      g.add((subject, DC.relation, URIRef(rel)))

  for id in identifier:
      g.add((subject, DC.identifier, URIRef(id)))

  for tp in tpe:
      g.add((subject, DC.type, Literal(tp)))


g.serialize("/home/grotec/Repositories/NFDI4BI-KG/N4BI_zenodo_community.n3")
