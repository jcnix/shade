function showSubcommentForm(par, user_url)
{
    /* ensure there is only one subcomment form at a time. */
    old_form = document.getElementById("subcomment");
    if(old_form) {
        content = old_form.parentElement;
        content.removeChild(old_form);
    }

    csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    if(!csrf_token)
        return;

    p = document.getElementById(par);
    form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", "/profile/"+user_url+"/comment/"+par+"/reply/");
    form.setAttribute("id", "subcomment");
    csrf = document.createElement('input');
    csrf.setAttribute('type', 'hidden');
    csrf.setAttribute('name', 'csrfmiddlewaretoken');
    csrf.setAttribute('value', csrf_token);
    textbox = document.createElement("textarea");
    textbox.setAttribute("name", "post");
    textbox.setAttribute("rows", "7");
    textbox.setAttribute("cols", "80");
    submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    submit.setAttribute("value", "Submit");
    br = document.createElement("br");
    form.appendChild(csrf);
    form.appendChild(textbox);
    form.appendChild(br);
    form.appendChild(submit);
    p.appendChild(form);
}

