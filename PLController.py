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
		subprocess.call(["hugin", panorama])
	
	@objc.IBAction
	def openInFinder_(self, sender):
		directory = self.selectedObject(self.selectedArrayController(), 'panorama_name')
		NSLog(u"directory : %s" % directory)
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
		panorama_files = re.compile('(?P<pto>[\S]+)\.pto$', re.I)
		for root, dirs, files in os.walk(top):
			m = panorama_directory.search(root.replace('\\', '/'))
			if m is not None:
				panorama_name = m.group('panorama_name') + '.pto'
				if panorama_name in files:
					if m.group('panorama_name') + '.tif' in files or m.group('panorama_name') + '_fused.tif' in files:
						c.append(p(root, panorama_name, m.group('panorama_name') + '.tif'))
						continue
				derived_panorama_files = re.compile('(?P<pto>' + m.group('panorama_name') + '.*)\.pto$', re.I)
				found = False
				for file in files:
					m2 = panorama_files.search(file)
					m3 = derived_panorama_files.search(file)
					if m3 is not None:
						if m3.group('pto') + '.tif' in files or m3.group('pto') + '_fused.tif' in files:
							c.append(p(root, file, m3.group('pto') + '.tif'))
							od.append(p(root, m.group('panorama_name'), None))
						found = True
					elif m2 is not None and not found:
						if m2.group('pto') + '.tif' in files or m2.group('pto') + '_fused.tif' in files:
							c.append(p(root, file, m2.group('pto') + '.tif'))
							od.append(p(root, m.group('panorama_name'), None))
						else:
							ns.append(p(root, file, None))
						found = True
				if not found:
					np.append(p(root, None, None))
		return c, ns, od, np
