### What
- A web-app for annoying people who annoy you.

### Why
- It's mostly an educational experiment and a cloud-y version of a desktop app I wrote a while ago.

### Where
- It's not public yet, but will probably be hosted off my vps at some ninja domain.

### How
- By exploiting carrier specific SMS gateways and lots of spoof email accounts, it becomes relatively trivial to spam like mad.

### Disclaimer
- You should not be using this for evil purposes.

### Tech Stack
- Django
- Python
- jQuery (core and ui)
- Bootstrap
- Redis

### Tasking
- To make this actually usable by a fair number of people, it
  is crucial to have a proper tasking system set up. For this
  I have opted to Redis, and django-rq.
- Since mass amounts of emails in close proximity tend to be
  rate limited by the services we'll be using (google, yahoo, etc.)
  consideration must be taken to prevent the accounts being blocked.
- We will construct a queue for each email address that can
  send messages, and though we will throttle the rate of each
  queue, we can run many queues in parallel (one for each address)
  and thus still complete a large number of messages in a short
  amount of time.
    
### Patterns
- This project makes use of a reusable django app that I wrote
  recently for more seamless communication between server and
  client. You can view that here: [django-commands](https://github.com/RutledgePaulV/django-commands)
- This app also makes use of a set of python utilities that I
  wrote that make some things easier when working with django.
  You can view that here: [django-toolkit](https://github.com/RutledgePaulV/django-toolkit)