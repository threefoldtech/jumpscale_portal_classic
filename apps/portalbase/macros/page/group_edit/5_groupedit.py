from JumpscalePortalClassic.portal.docgenerator.popup import Popup


def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    groupid = args.getTag('id')
    group = j.portal.tools.models.system.Group.get(groupid)
    if not group:
        params.result = ('group with id %s not found' % groupid, args.doc)
        return params

    popup = Popup(id='group_edit', header='Change Group', clearForm=False,
                  submit_url='/restmachine/system/usermanager/editGroup')

    options = list()
    popup.addText('Enter description', 'description', value=group.description)
    for user in j.portal.tools.models.system.User.find({}):
        available = user['id'] in [u['id'] for u in j.portal.tools.models.system.User.find({'groups': group['name']})]
        options.append((user['name'], user['name'], available))

    popup.addCheckboxes('Select Users', 'users', options)
    popup.addHiddenField('name', group.name)
    popup.write_html(page)

    return params
