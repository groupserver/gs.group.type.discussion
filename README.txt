.. sectnum::

Introduction
============

This product provides core code to support discussion groups, which are
the most common type of group. For the most part, a discussion group —
marked by the interface 
``gs.group.type.discussion.interfaces.IGSDiscussionGroup`` — is exactly 
the same as any other type of group. However, the `posting rules`_ are 
far more complex.

Posting Rules
=============

The core User Can Post system [#CanPost]_ provides one rule: is the 
person blocked from posting. A discussion group provides an additional 
eight rules, with their associated viewlets.

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

..  [#CanPost] See the ``gs.group.member.canpost`` product for more
    information.
..  [#RateLimit] See the ``gs.group.messages.ratelimit`` product for
    more information.
..  [#GroupProperties] There is no interface for the administrator to
    set the required group-properties. However, they can be set in the
    ZMI: add the property IDs to the ``required_properties`` attribute
    of the **mailing list.**

