from jumpscale import j
from JumpscalePortalClassic.portal.auth import auth

class system_errorconditionhandler(j.tools.code.classGetBase()):

    """
    errorcondition handling

    """

    def __init__(self):

        self._te = {}
        self.actorname = "errorconditionhandler"
        self.appname = "system"

    def describeCategory(self, category, language, description, resolution_user, resolution_ops, **args):
        """
        describe the errorcondition category (type)
        describe it as well as the possible solution
        is sorted per language
        param:category in dot notation e.g. pmachine.memfull
        param:language language id e.g. UK,US,NL,FR  (
        param:description describe this errorcondition category
        param:resolution_user describe this errorcondition solution that the user can do himself
        param:resolution_ops describe this errorcondition solution that the operator can do himself to try and recover from the situation
        result bool

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method describeCategory")

    def delete(self, eco, **kwargs):
        """
       delete alert
        """
        if j.portal.tools.models.system.Errorcondition.exists(eco):
            eco_obj = j.portal.tools.models.system.Errorcondition.get(eco)
            eco_obj.delete()
            return True
        return False


    @auth(['level1', 'level2', 'level3'])
    def purge(self, age, **kwargs):
        start = int(j.data.time.getEpochAgo(age))
        return j.portal.tools.models.system.Errorcondition.objects(epoch__lt=start).delete()