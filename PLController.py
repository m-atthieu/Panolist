#
#  PLController.py
#  Panolist
#
#  Created by Matthieu DESILE on 11/28/2010.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

import objc, os, re, subprocess
from Foundation import *
from AppKit import *

# helper
def p(dirname, ptofile, imagefile):
	return { 'panorama_name': dirname, 'pto': ptofile, 'img': imagefile }

class PLController(NSObject):
	# application objects
	completedPanoramasTableView = objc.IBOutlet()
	completedPanoramas = objc.ivar()
	completedArrayController = objc.IBOutlet()
	
	notStitchedPanoramasTableView = objc.IBOutlet()
	notStitchedPanoramas = objc.ivar()
	notStitchedArrayController = objc.IBOutlet()
	
	notPresentPanoramasTableView = objc.IBOutlet()
	notPresentPanoramas = objc.ivar()
	notPresentArrayController = objc.IBOutlet()
	
	otherDoneTableView = objc.IBOutlet()
	otherDonePanoramas = objc.ivar()
	otherDoneArrayController = objc.IBOutlet()
	
	tabView = objc.IBOutlet()
	rootPath = objc.IBOutlet()

	@objc.IBAction
	def refreshRootPath_(self, sender):
		c, ns, od, np = self.panoramalist(self.rootPath.stringValue())
		self._.completedPanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in c]
		self._.notStitchedPanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in ns]
		self._.notPresentPanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in np]
		self._.otherDonePanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in od]
		self.tabView.tabViewItemAtIndex_(0).setLabel_(u"Completed (%d)" % len(c))
		self.tabView.tabViewItemAtIndex_(1).setLabel_(u"Not Stitched (%d)" % len(ns))
		self.tabView.tabViewItemAtIndex_(2).setLabel_(u"Nothing Done (%d)" % len(np))
		self.tabView.tabViewItemAtIndex_(3).setLabel_(u"Other Done (%d)" % len(od))

	@objc.IBAction
	def openWithHugin_(self, sender):
		panorama = self.selectedObject(self.selectedArrayController(), 'pto')
		directory = self.selectedObject(self.selectedArrayController(), 'panorama_name') 
		panorama = directory + '/' + panorama
		NSLog(u"pano = %s" % panorama)
		subprocess.call(["/Applications/Hugin.app/Contents/MacOS/Hugin", panorama])
	
	@objc.IBAction
	def openInFinder_(self, sender):
		directory = self.selectedObject(self.selectedArrayController(), 'panorama_name')
		ws = NSWorkspace.sharedWorkspace()
		ws.openFile_(directory)

	def selectedArrayController(self):
		# cela va dependre du tableau qui est selectionne
		index = self.tabView.indexOfTabViewItem_(self.tabView.selectedTabViewItem())
		if index == 0:
			# completed
			return self.completedArrayController
		elif index == 1:
			# not stitched
			return self.notStitchedArrayController
		elif index == 2:
			# nothing
			return self.notPresentArrayController
		elif index == 3:
			# other panorama done
			return self.otherDoneArrayController
		else:
			return None

	def selectedObject(self, arrayController, key):
		selectedObjects = arrayController.selectedObjects()
		if len(selectedObjects) == 0:
			NSLog(u"No selected object")
			return None
		row = selectedObjects[0]
		if not key is None and (not row.has_key(key) or row[key] is None):
			NSLog(u'Required key is not present')
			return None
		return row[key]

	def panoramalist(self, top):
		c = []  # complete panoramas
		ns = [] # not stitched panoramas
		np = [] # nothing done
		od = [] # another pto has been stitched
		panorama_directory = re.compile("\d{4}/\d{2}/\d{2}/(?P<panorama_name>[\w][\S]+)$", re.I)
		pto_re = re.compile('(?P<pto>[\S]+)\.pto$', re.I)
		for root, dirs, files in os.walk(top):
			m = panorama_directory.search(root.replace('\\', '/'))
			if m is not None:
				pto_files = filter(pto_re.search, files)
				if len(pto_files) > 0:
					found = False
					for pto_file in pto_files:
						if not found:
							pto = pto_re.search(pto_file)
							output_re_str = '(?P<out>(' + pto.group('pto') + '|' + m.group('panorama_name') + ').*\.(tif|jpg))$'
							output_re = re.compile(output_re_str)
							output_files = filter(output_re.search, files)
							if len(output_files) > 0:
								output = output_re.search(output_files[0])
								c.append(p(root, pto.group('pto'), output.group('out')))
								found = True
					if not found:
						ns.append(p(root, pto_files[0], None))
				else:
					np.append(p(root, None, None))
		return c, ns, od, np
