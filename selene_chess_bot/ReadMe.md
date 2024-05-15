
NOTE:

If you got this error when doing python manage.py shell:

---------------------------------------------------------------------------
BUG:

IPython\terminal\interactiveshell.py", line 813, in prompt_for_code
    text = self.pt_app.prompt(
        ^^^^^^^^^^^^^^^^^^^
TypeError: PromptSession.prompt() got an unexpected keyword argument 'inputhook'

If you suspect this is an IPython 8.18.0 bug, please report it at:
    https://github.com/ipython/ipython/issues
or send an email to the mailing list at ipython-dev@python.org

You can print a more detailed traceback right now with "%tb", or use "%debug"
to interactively debug it.

Extra-detailed tracebacks for bug-reporting purposes can be enabled via:
    %config Application.verbose_crash=True

---------------------------------------------------------------------------

Is probably because, mayby, somebody (like me) is using Shiny for
Python, and, you maybe are asking yourself?

"What the hell is Shiny for Python?"

Glad you asked! Shiny for Python is a an interactive web application
framework for Python, that allows you to create web applications using
only Python, and, the best part is that you don't need to know HTML,
CSS or JavaScript, because Shiny for Python does all the work for you.

Such a nice tool, right? Yes!
it uses Flask, now, you know what Flask is, right? Well, we are using
Django as well, yes, yes, yes, in the same project, what a nice
combination?

Well, to solve the issue, go to the site packages folder, localize this
file:

IPython\terminal\interactiveshell.py

and on the lie 813, you will see this:

text = self.pt_app.prompt(
    default=default,
    inputhook=self._inputhook,
    **self._extra_prompt_options(),
)

add a try to it like this:

try:
    text = self.pt_app.prompt(
        default=default,
        inputhook=self._inputhook,
        **self._extra_prompt_options(),
    )
except TypeError:
    # optional, print(insult_to_me)
    text = self.pt_app.prompt(
        default=default,
        **self._extra_prompt_options(),
    )

Of course this is a momentary solution, I'll figure out a better way to
solve this issue, but for now, this is the way to go.
