Introduction
============

This product provides code to support discussion groups, which are the most
common type of group in GroupServer_. The complex `posting rules`_ for a
discussion group are implemented by this product. The discussion group code
is enabled by changing the `marker interface`_.

Posting Rules
=============

The core User Can Post system [#CanPost]_ provides one rule: is the person
blocked from posting. A discussion group provides six additional rules,
with their associated viewlets_.

Has a Profile:
  Checks to see if the person posting has a profile. The other way to
  look at this is the person is not anonymous.
  
Member:
  Checks to see if the person posting is a group member.
  
Working Email Address:
  Checks to see if the person posting has a verified email address. This
  prevents spamming, because you know that whoever posts has a working
  address.
  
Posting Limit:
  Each group has a maximum *posting rate* [#RateLimit]_. This rule 
  ensures that no-one exceeds the rate.
  
Required Site Properties:
  This rules ensures everyone has completed sign-up.
  
Required Group Properties:
  Each group can have some properties that are required for *just* the
  group [#GroupProperties]_. This rule ensures that each member has the
  properties set.

Marker Interface
================

A group is turned into a discussion group by changing the marker interface
for the group folder to ``IGSDiscussionGroup``. This marker interface has
the following inheritance tree::

  gs.group.base.interfaces.IGSGroupMarker
      △
      │
  gs.group.type.discussion.interfaces.IGSDiscussionGroup

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.type.discussion
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

..  [#CanPost] See the ``gs.group.member.canpost`` product for more
    information:
    <https://source.iopen.net/groupserver/gs.group.member.canpost/>
..  [#RateLimit] See the ``gs.group.messages.ratelimit`` product for
    more information:
    <https://source.iopen.net/groupserver/gs.group.messages.ratelimit/>
..  [#GroupProperties] There is no interface for the administrator to
    set the required group-properties. However, they can be set in the
    ZMI: add the property IDs to the ``required_properties`` attribute
    of the **mailing list.**
.. _GroupServer: http://groupserver.org
.. _viewlets: http://docs.zope.org/zope.viewlet/
