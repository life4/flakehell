from collections import defaultdict


def discover(app, argv):
    plugins_codes = defaultdict(list)

    app.initialize(argv)
    for check_type, checks in app.check_plugins.to_dictionary().items():
        for check in checks:
            plugins_codes[(check_type, check['plugin_name'])].append(check['name'])

    for (check_type, name), codes in plugins_codes.items():
        yield dict(
            type=check_type,
            name=name,
            codes=codes,
        )
