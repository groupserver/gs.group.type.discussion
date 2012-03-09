# coding=utf-8
from urllib import urlencode
from zope.cachedescriptors.property import Lazy
from Products.GSGroup.joining import GSGroupJoining # --=mpj17=-- ?
from Products.GSGroupMember.groupmembership import JoinableGroupsForSite,\
    InvitationGroupsForSite
from gs.group.member.canpost import RuleViewlet
from canpostrules import NotAnonymous, IsMember, WorkingEmail
from postinglimitcanpostrule import PostingLimit
from requiredpropertiescanpostrule import RequiredSiteProperties, \
    RequiredGroupProperties

class Anonymous(RuleViewlet):
    weight = NotAnonymous.weight

    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval

    @Lazy
    def loginUrl(self):
        d = {'came_from': self.request.URL}
        retval = '/login.html?%s' % urlencode(d)
        assert retval
        return retval

    @Lazy
    def signupUrl(self):
        d = {   'form.came_from': self.request.URL,
                'form.groupId': self.groupInfo.id}
        retval = '/request_registration.html?%s' % urlencode(d)
        return retval
        
    @Lazy
    def joinability(self):
        return GSGroupJoining(self.groupInfo.groupObj).joinability

class NotAMember(RuleViewlet):
    weight = IsMember.weight
    
    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval
        
    @Lazy
    def canJoin(self):
        joinableGroups = JoinableGroupsForSite(self.loggedInUser.user)
        retval = self.groupInfo.id in joinableGroups
        assert type(retval) == bool
        return retval

    @Lazy
    def canInvite(self):
        invitationGroups = InvitationGroupsForSite(self.loggedInUser.user,
                                               self.groupInfo.groupObj)
        retval = (self.groupInfo.id in invitationGroups) and \
          not self.canJoin
        assert type(retval) == bool
        return retval

class NoWorkingEmail(RuleViewlet):
    weight = WorkingEmail.weight
    
    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval

class PostingLimitHit(RuleViewlet):
    weight = PostingLimit.weight
    
    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval

class NoSiteProperties(RuleViewlet):
    weight = RequiredSiteProperties.weight
    
    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval
        
class NoGroupProperties(RuleViewlet):
    weight = RequiredGroupProperties.weight
    
    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval

