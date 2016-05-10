import json


def swagger_json_to_markdown(swagger_json):
    paths = swagger_json["paths"]
    defs = swagger_json["definitions"]
    spec_list = []
    for path_name in paths:
        spec_list.append("{}".format(path_name))
        spec_list.append("{}\n".format("="*len(path_name)))

        path = paths[path_name]
        for operation_name in path:
            spec_list.append("{}".format(operation_name))
            spec_list.append("{}\n".format("-"*len(operation_name)))

            operation = path[operation_name]
            desc = "{} {}".format(operation["summary"], operation["description"])
            if desc.strip():
                spec_list.append("Description:\n")
                spec_list.append("    {}\n".format(desc.strip()))
            if "parameters" in operation:
                spec_list.append("Parameters:\n")
                for parameter in operation["parameters"]:
                    spec_list.append("      {} ({} parameter)\n".format(parameter["name"], parameter["in"]))
            if "responses" in operation:
                spec_list.append("Responses:\n")
                for response_code in operation["responses"]:
                    if "description" in operation["responses"][response_code]:
                        spec_list.append("    {}: {}\n".format(response_code, operation["responses"][response_code]["description"]))
                    else:
                        spec_list.append("    {}\n".format(response_code))

    spec_str = ""
    for line in spec_list:
        spec_str += line + "\n"

    return spec_str
