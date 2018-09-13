Why fluteline?
==============

PyPI is full of projects with "pipe" in their name, and flutes are, uh... similar?

More seriously, I couldn't find a simple solution for producers, consumer-producers, consumers workflow, that is easy to integrate with other libraries. So I created my own.

Use fluteline if:

* Your problem is IO bound. Every fluteline node runs in a thread.
* Your nodes have work to do in the background. Otherwise, just a chain of generator will suffice.
