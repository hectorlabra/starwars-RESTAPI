from flask import jsonify, url_for


class APIException(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def has_no_empty_params(rule):
    defaults = rule.defaults or ()
    arguments = rule.arguments or ()
    return len(defaults) >= len(arguments)


def generate_sitemap(app):
    links = ['/admin/']

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule) and "/admin/" not in url_for(rule.endpoint):
            links.append(url_for(rule.endpoint, **(rule.defaults or {})))

    links_html = "".join(
        [f"<li><a href='{link}'>{link}</a></li>" for link in links])

    return f"""
        <div style="text-align: center;">
            <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
            <h1>Rigo welcomes you to your API!!</h1>
            <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
            <p>Start working on your project by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
            <p>Remember to specify a real endpoint path like:</p>
            <ul style="text-align: left;">
                {links_html}
            </ul>
        </div>
    """
