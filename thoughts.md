# what is the most code efficient way to structure a crud project with django?

## do not separate backend and frontend

## use django forms vs pydantic validation on functions and then custom form building

django forms are easy to use and can be easily customized but there is some boilerplate code maybe?
what is the boilerplate code? just class and meta there is no code that is not required.

what is the advantage of pydantic validated functions?
first the code is as readable as possible and can be tested easily. but it needs a class wrapper 
around it or a function wrapper to overwrite the default form generation. which then looks pretty
much like django forms.

- how to make pydantic validation autogenerate custom forms:
  - overwrite for example goal_id with a custom select field
  - overwrite for example list[goal_id] with a custom select multiple field

## make the urls as small as possible

there ofc will be one url for every view but for the forms that post data, maybe
all except one url can be avoided. which means this url will render the form and 
accept the post data. but if is a creation form vs an update or delete form there 
is a big difference in the form initializing, for example one time a instance will
be passed the other time not. success urls are also different every time, plus 
they should not be moved into the form layer, becase this form layer should be
indpendent of the view layer.

### the split from the command layer to django forms to pydantic validation

basically the django flow is like this

user -> hits the view -> view renders the form -> form is displayed to the user
user -> fills out the form -> form is submitted to the same form -> form is validated
user -> clicks the cancel button -> is redirected to the cancel url specified in the view
 
here is the flow which is annoying:

on query:
view -> form

ob submit:
view                      -> form
success_url                  ok function to save for example
cancel_url                   
form kwargs like instance

the django layer flow is like this:

user -> hits the view -> frontend renders a form -> form is displayed to the user
user -> fills out the form -> form is submitted to the command layer -> data is validated
user -> clicks the cancel button -> is redirected to the cancel url specified in the frontend

the command layer flow:

on query:
frontend build form -> display form
success_url and everything is on the frontend

on submit:
command layer

how about a flow that uses pydantic validation in custom forms which again use django form
widgets for rendering the form. then the form is build by the endpoint with the post data on submit
but on query the form is build by the form query endpoint and stuffed with data from ??? where.

how about django forms and just stuffing them with the request, can then all urls be avoided?
all other injections can be done from settings.

okay how about getting the instance from the url?

is there a good way to seperate the get from the post? meaning i want to get the instance select form on get
but on post just the id is submitted. but getting the instance select on get is not possible because the
form just know the id.

### success url

should be used in the frontend and the request like ?success_url=...
backend will give it back as context from the forms view.

### cancel url

should be used into the frontend and the request like ?cancel_url=...

### user into form

the user should be passed into the form automatically by the form view. and it
instance form should not be used.

## use htmx on the frontend for higher interactivity

if possible avoid any javascript on the frontend if it is required use it only for the most basic
stuff. for form submit and stuff like that htmx should be used.

## use html components in models

this is something custom that needs to be built somehow. 
but once this is ready in the template the model can basically render itself.
