#! /usr/bin/env python

import argparse
import os
import json
from TemplateHelper import TemplateHelper
from biop3.Workspace.WorkspaceClient import Workspace

desc1 = '''
NAME
      Build_Model_Template -- build a Model Template object from source files

SYNOPSIS
'''

desc2 = '''
DESCRIPTION
'''

desc3 = '''
EXAMPLES
      Build a Model Template object:
      > Build_Model_Template.py compounds.tsv reactions.tsv
      
SEE ALSO
      Build_Biochem.py

AUTHORS
      Mike Mundy 
'''

if __name__ == "__main__":
    # Parse options.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, prog='Build_Model_Template', epilog=desc3)
    parser.add_argument('id', help='ID of Model Template object', action='store')
    parser.add_argument('templatedir', help='path to directory containing source files', action='store')
    parser.add_argument('ref', help='reference to workspace location to store Model Template object', action='store')
    parser.add_argument('--biochemref', help='reference to Biochemistry object in workspace', action='store', default='')
    parser.add_argument('--compoundfile', help='path to master compounds file', action='store', default='../Biochemistry/compounds.master.tsv')
    parser.add_argument('--reactionfile', help='path to master reactions file', action='store', default='../Biochemistry/reactions.master.tsv')
    parser.add_argument('--name', help='name of object', action='store', default=None)
    parser.add_argument('--type', help='type of model', action='store', default='GenomeScale')
    parser.add_argument('--domain', help='domain of organisms', action='store', default='Bacteria')
    parser.add_argument('--wsurl', help='URL of workspace server', action='store', dest='wsurl', default='http://p3.theseed.org/services/Workspace')
    usage = parser.format_usage()
    parser.description = desc1 + '      ' + usage + desc2
    parser.usage = argparse.SUPPRESS
    args = parser.parse_args()

    # Create a helper object.
    helper = TemplateHelper(args.compoundfile, args.reactionfile)

    # The following fields are required in a Model Template object.
    template = dict()
    template['id'] = args.id
    if args.name is not None:
        template['name'] = args.name
    else:
        template['name'] = args.id
    template['modelType'] = args.type
    template['domain'] = args.domain
    template['biochemistry_ref'] = args.biochemref
    template['pathways'] = list() # Always an empty for now

    # Need to support these fields
    template['roles'] = list()
    template['complexes'] = list()

    # Order is important so references can be made between sections of the Model Template.
    
    # Add the template compartments.
    compartmentsFile = os.path.join(args.templatedir, 'Compartments.tsv')
    template['compartments'] = helper.readCompartmentsFile(compartmentsFile, includeLinenum=False)

    # Add the template biomasses.
    biomassFile = os.path.join(args.templatedir, 'Biomasses.tsv')
    biomassCompoundsFile = os.path.join(args.templatedir, 'BiomassCompounds.tsv')
    template['biomasses'] = helper.readBiomassesFile(biomassFile, biomassCompoundsFile, includeLinenum=False)

    # Add the template reactions.
    reactionsFile = os.path.join(args.templatedir, 'Reactions.tsv')
    template['reactions'] = helper.readReactionsFile(reactionsFile, includeLinenum=False)

    # Add the template compounds (constructed from reagents in reactions).
    template['compounds'] = list()
    for key in helper.compounds:
        template['compounds'].append(helper.compounds[key])

    # Add the template comp compounds (constructed from reagents in reactions).
    template['compcompounds'] = list()
    for key in helper.compCompounds:
        template['compcompounds'].append(helper.compCompounds[key])

    # Save a local copy for easy reference.
    filename = os.path.join(args.templatedir, args.id+'.json')
    json.dump(template, open(filename, 'w'), indent=4)
    
    # Save the Model Template typed object to the specified workspace path. An existing typed object
    # is overwritten with the updated data.
    wsClient = Workspace(args.wsurl)
    output = wsClient.create( { 'objects': [ [ args.ref, 'modeltemplate', {}, template ] ], 'overwrite': 1 });
