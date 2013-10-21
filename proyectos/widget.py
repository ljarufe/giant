'''
Created on 06/08/2010

@author: mauricio
'''
from django import forms
from django.forms import widgets

class markitup(widgets.Textarea):
    class Media:
        js = (
              'http://www.giant.aqpnet.com/media/js/jquery-1.3.2.js',
              'http://www.giant.aqpnet.com/media/markitup/markitup/jquery.markitup.js',
              'http://www.giant.aqpnet.com/media/markitup/markitup/sets/html/set.js',
              )
        css = {
               'screen':(
                         'http://www.giant.aqpnet.com/media/markitup/markitup/skins/simple/style.css',
                         'http://www.giant.aqpnet.com/media/markitup/markitup/sets/html/style.css',
                         )
               }
