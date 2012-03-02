# coding=utf-8
from zope.app.apidoc import interface
from zope.cachedescriptors.property import Lazy
from Products.XWFCore.XWFUtils import comma_comma_and
from Products.GSProfile import interfaces as profileinterfaces
from gs.group.member.canpost.rules import BaseRule

class RequiredSiteProperties(BaseRule):
    u'''Every member must have the properties that are required by the
    site.'''
    weight = 60
    
    @Lazy
    def siteProperties(self):
        '''Whole-heartly nicked from the GSProfile code, the site-wide
        user properties rely on a bit of voodoo: the schemas themselves
        are defined in the file-system, but which schema to use is stored
        in the "GlobalConfiguration" instance.
        '''
        site_root = self.group.site_root()
        assert hasattr(site_root, 'GlobalConfiguration')
        config = site_root.GlobalConfiguration
        ifName = config.getProperty('profileInterface', 'IGSCoreProfile')
        # --=mpj17=-- Sometimes profileInterface is set to ''
        ifName = (ifName and ifName) or 'IGSCoreProfile'

        assert hasattr(profileinterfaces, ifName), \
                'Interface "%s" not found.' % ifName
        profileInterface = getattr(profileinterfaces, ifName)
        retval = interface.getFieldsInOrder(profileInterface)
        return retval
    
    @Lazy
    def requiredSiteProperties(self):
        retval = [n for n, a in self.siteProperties if a.required]
        assert type(retval) == list
        return retval
    
    @Lazy
    def unsetRequiredProperties(self):
        retval = [p for p in self.requiredSiteProperties
                  if not(self.userInfo.get_property(p, None))]
        return retval
    
    def check(self):
        if not self.s['checked']:
            if self.unsetRequiredProperties:
                self.s['canPost'] = False
                fields = [a.title for n, a in self.siteProperties 
                      if n in unsetRequiredProps]
                f = comma_comma_and(fields)
                attr = (len(fields) == 1 and u'attribute') or u'attributes'
                isare = (len(fields) == 1 and u'is') or u'are'
                self.s['status'] = u'the %s that %s required by the '\
                    u'site (%s) %s not set' %\
                    (attr, isare, f, isare)
                self.s['statusNum'] = weight
            else:
                self.s['canPost'] = True
                self.s['status'] = u'properties that are required by '\
                    u'the site are set.'
                self.s['statusNum'] = 0
            self.s['checked'] = True

        assert self.s['checked']                
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int

class RequiredGroupProperties(RequiredSiteProperties):
    u'''Every member must have the properties that are required by the
    group.'''
    weight = 70

    @Lazy
    def requiredGroupProperties(self):
        '''Required group properties are stored on the mailing-list 
        instance for the group. They are checked against the site-wide
        user properties, to ensure that it is *possible* to have the
        user-profile attribute filled.
        '''
        groupProps = self.mailingList.getProperty('required_properties', [])
        siteProps = [n for n, _a in self.siteProperties]
        retval = []
        for prop in groupProps:
            if prop in siteProps:
                retval.append(prop)
        assert type(retval) == list
        return retval
        
    @Lazy
    def unsetRequiredProperties(self):
        retval = [p for p in self.requiredGroupProperties
                  if not(self.userInfo.get_property(p, None))]
        return retval
       
    def check(self):
        if not self.s['checked']:
            if self.unsetRequiredProperties:
                self.s['canPost'] = False
                fields = [a.title for n, a in self.siteProperties 
                      if n in unsetRequiredProps]
                f = comma_comma_and(fields)
                attr = (len(fields) == 1 and u'attribute') or u'attributes'
                isare = (len(fields) == 1 and u'is') or u'are'
                self.s['status'] = u'the %s that %s required by the '\
                    u'group (%s) %s not set' %\
                    (attr, isare, f, isare)
                self.s['statusNum'] = weight
            else:
                self.s['canPost'] = True
                self.s['status'] = u'properties that are required by '\
                    u'the group are set.'
                self.s['statusNum'] = 0
            self.s['checked'] = True

        assert self.s['checked']                
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int


