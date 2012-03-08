# coding=utf-8
from datetime import timedelta
from zope.cachedescriptors.property import Lazy
from Products.XWFCore.XWFUtils import curr_time as now, \
    timedelta_to_string
from gs.group.member.canpost.rules import BaseRule
from gs.group.member.base.utils import user_admin_of_group, \
    user_participation_coach_of_group
from Products.GSSearch.queries import MessageQuery

class PostingLimit(BaseRule):
    u'''Each grop has a maximum posting rate. This rule ensures that
    the members do not exceed the posting rate. The group administrators
    and the participation coach are excempt from this rule.'''
    weight=50
    
    @Lazy
    def messageQuery(self):
        da = self.group.zsqlalchemy
        retval = MessageQuery(self.group, da)
        return retval

    @property
    def oldMessagePostDate(self):
        offset = self.mailingList.getValueFor('senderlimit') - 1
        if offset < 0:
            offset = 0
            # This is actually a hack to get around a problem of people
            #   setting the sender limit to 0
        tokens = createObject('groupserver.SearchTextTokens', '')
        posts = self.messageQuery.post_search_keyword(tokens, 
                    self.siteInfo.id, [self.groupInfo.id], 
                    [self.userInfo.id], 1, offset)
        assert len(posts) == 1
        retval = posts[0]['date']
        assert isinstance(retval, datetime)        
        return retval

    def check(self):
        if not self.s['checked']:
            if user_participation_coach_of_group(self.userInfo, self.groupInfo):
                self.s['canPost'] = True
                self.s['status'] = u'a participation coach.'
                self.s['statusNum'] = 0
            elif user_admin_of_group(self.userInfo, self.groupInfo):
                self.s['canPost'] = True
                self.s['status'] = u'a group administrator.'
                self.s['statusNum'] = 0
            else:
                interval = self.mailingList.getValueFor('senderinterval')
                n = now()
                td = timedelta(seconds=interval)
                count = self.messageQuery.num_posts_after_date(
                                    self.siteInfo.id, self.groupInfo.id, 
                                    self.userInfo.id, n - td)
                if (count >= self.mailingList.getValueFor('senderlimit')):
                    self.s['canPost'] = False
                    canPostDate = self.oldMessagePostDate + td
                    prettyDate = munge_date(self.group, canPostDate, 
                                            user=self.userInfo.user)
                    prettyDelta = timedelta_to_string(canPostDate - n)
                    self.s['status'] = u'over the posting limit. You '\
                        u'can post again at %s (in %s).' % \
                        (prettyDate, prettyDelta)
                    self.s['statusNum'] = self.weight
                else:
                    self.s['canPost'] = True
                    self.s['status'] = u'under the posting limit.'
                    self.s['statusNum'] = 0
            self.s['checked'] = True

        assert self.s['checked']                
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int

