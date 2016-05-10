import os
import sys
import argparse
import json
import pkg_resources
from flask_swagger import swagger
from swagger_json_to_markdown import swagger_json_to_markdown

parser = argparse.ArgumentParser()
parser.add_argument('app', help='the flask app to swaggerify')
parser.add_argument('--template', help='template spec to start with, before any other options or processing')
parser.add_argument('--out-dir', default=None, help='the directory to output to')
parser.add_argument('--definitions', default=None, help='json definitions file')
parser.add_argument('--host', default=None)
parser.add_argument('--base-path', default=None)
parser.add_argument('--version', default=None, help='Specify a spec version')
parser.add_argument('--as-markdown', default=False, help='Output as markdown')

args = parser.parse_args()

if "." in args.app:
    args.app = (args.app.split("."))[0]

sys.path.append(os.getcwd())

if os.path.sep in args.app:
    app_split = args.app.rsplit(os.path.sep)
    args.app = app_split[1]
    if os.path.isfile(args.app):
        sys.path.append(app_split[0])
    else:
        sys.path.append("{}/{}".format(os.getcwd(), app_split[0]))

def run():
    app = pkg_resources.EntryPoint.parse("x=%s" % args.app).load(False).app

    # load the base template
    template = None
    if args.template is not None:
        with open(args.template, 'r') as f:
            template = json.loads(f.read())

        # overwrite template with specified arguments
        if args.definitions is not None:
            with open(args.definitions, 'r') as f:
                rawdefs = json.loads(f.read())
                if 'definitions' in rawdefs:
                    rawdefs = rawdefs['definitions']
                for d in rawdefs.keys():
                    template['definitions'][d] = rawdefs[d]

    spec = swagger(app, template=template)
    if args.host is not None:
        spec['host'] = args.host
    if args.base_path is not None:
        spec['basePath'] = args.base_path
    if args.version is not None:
        spec['info']['version'] = args.version
    if args.as_markdown:
        if args.out_dir is None:
            print swagger_json_to_markdown(spec)
        else:
            with open("%s/swagger.md" % args.out_dir, 'w') as f:
                f.write(swagger_json_to_markdown(spec))
                f.close
    else:
        if args.out_dir is None:
            print(json.dumps(spec, indent=4))
        else:
            with open("%s/swagger.json" % args.out_dir, 'w') as f:
                f.write(json.dumps(spec, indent=4))
                f.close()

if __name__ == '__main__':
    run()
