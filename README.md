### A web-app for annoying people who annoy you.

### By exploiting carrier specific SMS gateways and lots of spoof email accounts, it becomes relatively trivial to spam like mad.

### You should not be using this for evil purposes, it's merely an education experiment.

### Tech Stack
- Django
- Python
- jQuery (core and ui)
- Bootstrap

### Patterns
- Command / Strategy
  - I wrote the command module and accompanying front-end module
    to simplify communication between the front-end and back-end.
    Rather than following the ever-so-popular REST-api with model
    bound endpoints, we instead opt for issuing commands to a single
    endpoint. This provides a great deal of flexibility and is quite
    convenient from a developer perspective. I've yet to hear strong
    arguments against it, save for maybe lack of a self-documenting API.

