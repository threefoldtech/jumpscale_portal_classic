def main(j, args, params, tags, tasklet):
    page = args.page
    from JumpscalePortalClassic.portal.docgenerator.form import Form
    import yaml

    query_params = args.requestContext.params
    header = args.getTag('header')
    action_url = args.getTag('actionurl')

    def _showexample():
        page.addMessage("""Actions must be in yaml form.
eg:
- display: Start
  action: /restmachine/cloudbroker/machine/start
  input:
  - reason
  - spacename
  - name: accesstype
    type: dropdown
    label: ACL
    values:
     - label: Admin
       value: ARCXDU
     - label: Write
       value: RCX
     - label: Read
       value: R

  data:
   machineId: $$id
   accountName: $$accountname

- display: Stop
  action: /restmachine/cloudbroker/machine/stop?machineId=$$id&reason=ops&accountName=$$accountname&spaceName=$$spacename
}}
""")
        params.result = page
        return params

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])

    if not content:
        return _showexample()

    actions = yaml.load(content, Loader=yaml.loader.BaseLoader)
    if actions == content:
        return _showexample()

    if not isinstance(actions, list):
        actions = [actions]

    for actiondata in actions:
        submit_url = actiondata['action']
        display = actiondata['display']
        inputs = actiondata.get('input', '')
        navigateback = j.data.text.getBool(actiondata.get('navigateback', False))
        reload = j.data.text.getBool(actiondata.get('reload', True))
        hide = j.data.text.getBool(actiondata.get('hide', False))
        data = actiondata.get('data', {})
        showresponse = j.data.text.getBool(actiondata.get('showresponse', False))
        hideon = actiondata.get('hideon', [])
        if hideon:
            hideon_input = actiondata.get('hideonInput', '')
            if hideon_input in hideon:
                continue

    form = Form(id='form',
                header=header,
                submit_url=submit_url,
                submit_method="post",
                navigateback=navigateback,
                reload_on_success=reload,
                showresponse=showresponse,
                clearForm=False)

    if inputs:
        for var in inputs:

            if isinstance(var, str):
                form.addText(var, var)
            else:
                if var['type'] in ('dropdown', 'radio'):
                    label = var['label']
                    name = var['name']
                    options = list()
                    for value in var['values']:
                        options.append((value['label'], value['value']))
                    if var['type'] == 'dropdown':
                        form.addDropdown(label, name, options)
                    elif var['type'] == 'radio':
                        form.addRadio(label, name, options)
                elif var['type'] in ('text', 'password', 'number'):
                    label = var['label']
                    name = var['name']
                    default = var.get('default', '')
                    required = var.get('required', False)
                    form.addText(label, name, type=var['type'], value=default, required=required)
                elif var['type'] == 'hidden':
                    form.addHiddenField(var['name'], var['value'])
                elif var['type'] == 'textarea':
                    label = var['label']
                    name = var['name']
                    required = var.get('required', False)
                    form.addTextArea(label, name, required=required)
                elif var['type'] == 'code':
                    label = var['label']
                    name = var['name']
                    required = var.get('required', False)
                    lang = var.get('language', 'yaml')
                    form.addCodeBlock(code="", template=lang, page=page)

    form.addButton(type='submit', value=display)

    form.write_html(page)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
