# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.member.canpost.rules import BaseRule
from gs.group.member.base.utils import user_member_of_group

class NotAnonymous(BaseRule):
    u'''Only people with profiles on this site can post to the group.'''
    weight=20
            
    def check(self):
        if not self.s['checked']:
            if self.userInfo.anonymous:
                self.s['canPost'] = False
                self.s['status'] = u'anonymous.'
                self.s['statusNum'] = self.weight
            else:
                self.s['canPost'] = True
                self.s['status'] = u'have a profile.'
                self.s['statusNum'] = 0
                
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int

class IsMember(BaseRule):
    u'''Only members of this group can post.'''
    weight=30
            
    def check(self):
        if not self.__checked:
            if user_member_of_group(self.userInfo, self.groupInfo):
                self.s['canPost'] = True
                self.s['status'] = u'a member.'
                self.s['statusNum'] = 0
            else:
                self.s['canPost'] = False
                self.s['status'] = u'not a member.'
                self.s['statusNum'] = self.weight
                
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int


