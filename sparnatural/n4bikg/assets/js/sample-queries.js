var queries = [
  {
    label_en: "Institutions participating in NFDI4BIOIMAGE",
      query: {
          "distinct": true,
          "variables": [
              {
                  "termType": "Variable",
                  "value": "NFDIConsortium"
              },
              {
                  "termType": "Variable",
                  "value": "ResearchOrganization"
              }
          ],
          "order": null,
          "branches": [
              {
                  "line": {
                      "s": "NFDIConsortium",
                      "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config#hasParticipantOrganization",
                      "o": "ResearchOrganization",
                      "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/NFDIConsortium",
                      "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ResearchOrganization",
                      "criterias": []
                  }
              }
          ],
          "limit": 1000
},
  },
    {
        label_en: "Institutions with affiliated researchers",
        query: {
  "distinct": true,
  "variables": [
    {
      "termType": "Variable",
      "value": "ResearchOrganization"
    },
    {
      "termType": "Variable",
      "value": "Researcher"
    }
  ],
  "order": null,
  "branches": [
    {
      "line": {
        "s": "NFDIConsortium",
        "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config#hasParticipantOrganization",
        "o": "ResearchOrganization",
        "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/NFDIConsortium",
        "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ResearchOrganization",
        "criterias": []
      },
      "children": [
        {
          "line": {
            "s": "ResearchOrganization",
            "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/affiliate",
            "o": "Researcher",
            "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ResearchOrganization",
            "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/Researcher",
            "criterias": []
          }
        }
      ]
    }
  ],
  "limit": 1000
}
    },
    {
        label_en: "Zenodo records in NFDI4BIOIMAGE community with Creators",
        query: {
  "distinct": true,
  "variables": [
      {
          "termType": "Variable",
          "value": "ZenodoRecord"
      },
{
      "termType": "Variable",
      "value": "Z_Text"
    },
        {
      "termType": "Variable",
      "value": "ResearchOrganization"
    }
  ],
  "order": null,
  "branches": [
    {
      "line": {
        "s": "ZenodoRecord",
        "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ZenodoRecord_21",
        "o": "Researcher",
        "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ZenodoRecord",
        "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/Researcher",
        "criterias": []
      },
      "children": [
        {
          "line": {
            "s": "Researcher",
            "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/affiliation",
            "o": "ResearchOrganization",
            "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/Researcher",
            "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ResearchOrganization",
            "criterias": []
          }
        },
        {
          "line": {
            "s": "Researcher",
            "p": "http://www.w3.org/2000/01/rdf-schema#label",
            "o": "Z_Text",
            "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/Researcher",
            "oType": "http://special/Z_Text",
            "criterias": []
          }
        }
      ]
    }
  ],
  "limit": 1000
}
    },
    {
        label_en : "NFDI4BIOIMAGE OMERO Images with thumbnail and viewer links.",
        query: {
  "distinct": true,
  "variables": [
    {
      "termType": "Variable",
      "value": "OMEROServer"
    },
    {
      "termType": "Variable",
      "value": "Thumbnail"
    },
    {
      "termType": "Variable",
      "value": "OMEROImageView"
    },
    {
      "termType": "Variable",
      "value": "OME_Image"
    }
  ],
  "order": null,
  "branches": [
    {
      "line": {
        "s": "OMEROServer",
        "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ome_image",
        "o": "OME_Image",
        "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/OMEROServer",
        "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/OME_Image",
        "criterias": []
      },
      "children": [
        {
          "line": {
            "s": "OME_Image",
            "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/thumbnail",
            "o": "Thumbnail",
            "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/OME_Image",
            "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/Thumbnail",
            "criterias": []
          }
        },
        {
          "line": {
            "s": "OME_Image",
            "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/ome_detail",
            "o": "OMEROImageView",
            "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/OME_Image",
            "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/OMEROImageView",
            "criterias": []
          }
        }
      ]
    }
  ],
  "limit": 1000
}
    },
    {
        label_en: "OMEROs with SPARQL endpoint",
        query: {
            "distinct": true,
            "variables": [
                {
                    "termType": "Variable",
                    "value": "OMEROServer"
                },
                {
                    "termType": "Variable",
                    "value": "SparqlServiceShape"
                }
            ],
            "order": null,
            "branches": [
                {
                    "line": {
                        "s": "OMEROServer",
                        "p": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/sparql_service",
                        "o": "SparqlServiceShape",
                        "sType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/OMEROServer",
                        "oType": "http://kg.nfdi4bioimage.de/n4bikg/sparnat-config/SparqlServiceShape",
                        "criterias": []
                    }
                }
            ],
            "limit": 1000
}
    }
];
