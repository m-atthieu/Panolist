#
#  PLController.py
#  Panolist
#
#  Created by Matthieu DESILE on 11/28/2010.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

import objc, os, re
from Foundation import *

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
	
	rootPath = objc.IBOutlet()

	@objc.IBAction
	def refreshRootPath_(self, sender):
		c, ns, np = self.panoramalist(self.rootPath.stringValue())
		self._.completedPanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in c]
		self._.notStitchedPanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in ns]
		self._.notPresentPanoramas = [NSDictionary.dictionaryWithDictionary_(x) for x in np]
		NSLog("refreshing ")

	def panoramalist(self, top):
		c = []
		ns = []
		np = []
		#panorama_directory = re.compile("[/\]\d{4}[/\\]\d{2}[/\\]\d{2}[/\\]{1}(?P<panorama>[\S])+$", re.I)
		panorama_directory = re.compile("\d{4}/\d{2}/\d{2}/(?P<panorama_name>[\w][\S]+)$", re.I)
		panorama_files = re.compile('[\w][\S]+\.pto', re.I)
		for root, dirs, files in os.walk(top):
			m = panorama_directory.search(root.replace('\\', '/'))
			if m is not None:
				panorama_name = m.group('panorama_name') + '.pto'
				if panorama_name in files:
					if m.group('panorama_name') + '.tif' in files:
						c.append(p(root, panorama_name, m.group('panorama_name') + '.tif'))
					elif m.group('panorama_name') + '.jpg' in files:
						c.append(p(root, panorama_name, m.group('panorama_name') + '.jpg'))
					else:
						ns.append(p(root, panorama_name, None))
				else:
					found = False
					for file in files:
						if panorama_files.search(file):
							found = True
							
					if not found:
						np.append(p(root, None, None))
		return c, ns, np