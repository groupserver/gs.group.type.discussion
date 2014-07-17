# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from gs.group.type.set import SetABC


class SetDiscussionGroup(SetABC):
    'Set a group folder to be a discussion group'
    name = 'Discussion group'
    typeId = 'gs-group-type-discussion-set'
    weight = 10
    show = True

    def set(self):
        '''Add the marker-interface to make the group into a discussion
        group.'''
        iFaces = ['gs.group.type.discussion.interfaces.IGSDiscussionGroup']
        self.add_marker_interfaces(self.group, iFaces)
