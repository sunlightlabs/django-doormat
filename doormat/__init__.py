
def clean_domain(domain):
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def clean_path(path):
    path = path.lower()
    if not path.startswith("/"):
        path = "/%s" % path
    return path