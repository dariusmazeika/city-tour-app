bind = "0.0.0.0:8000"
workers = 2
loglevel = "info"

secure_scheme_headers = {"X-FORWARDED-PROTOCOL": "ssl", "X-FORWARDED-PROTO": "https", "X-FORWARDED-SSL": "on"}
